#!/usr/bin/env python3
"""Aura UDP heartbeat receiver."""

import argparse
import csv
import os
import signal
import socket
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "receiver.conf"
SERVICE_NAME = "aura.service"
CSV_FIELDS = ["name", "ip", "port", "last_contact", "status"]


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0)


def utc_now_text():
    return utc_now().isoformat().replace("+00:00", "Z")


def parse_timestamp(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_config(path):
    config = {
        "bind_host": "127.0.0.1",
        "bind_port": "5150",
        "timeout_seconds": "90",
        "sensors_csv": str(ROOT / "config" / "sensors.csv"),
    }
    if path.exists():
        with path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"invalid config line: {raw_line.rstrip()}")
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def load_sensors(csv_path):
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise ValueError(f"{csv_path} must have fields: {','.join(CSV_FIELDS)}")
        return list(reader)


def save_sensors(csv_path, rows):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        newline="",
        dir=str(csv_path.parent),
        delete=False,
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        temp_name = handle.name
    os.chmod(temp_name, 0o664)
    os.replace(temp_name, csv_path)


def update_heartbeat(csv_path, sensor_name, source_ip, source_port):
    rows = load_sensors(csv_path)
    updated = False
    now = utc_now_text()

    for row in rows:
        if row["name"] == sensor_name:
            row["ip"] = source_ip
            row["port"] = str(source_port)
            row["last_contact"] = now
            row["status"] = "UP"
            updated = True
            break

    if updated:
        save_sensors(csv_path, rows)
        print(f"{now} heartbeat {sensor_name} from {source_ip}:{source_port}", flush=True)
    else:
        print(f"{now} unknown sensor ignored: {sensor_name}", flush=True)


def mark_stale_sensors(csv_path, timeout_seconds):
    rows = load_sensors(csv_path)
    now = utc_now()
    changed = False

    for row in rows:
        last_contact = parse_timestamp(row.get("last_contact", ""))
        if not last_contact:
            continue
        age = (now - last_contact).total_seconds()
        if age > timeout_seconds and row.get("status") != "DOWN":
            row["status"] = "DOWN"
            changed = True
            print(f"{utc_now_text()} timeout {row['name']} marked DOWN", flush=True)

    if changed:
        save_sensors(csv_path, rows)


def parse_heartbeat(message):
    parts = message.strip().split("|")
    if len(parts) != 2:
        return None
    name, state = parts
    if not name or state != "alive":
        return None
    return name


def run_receiver(config_path):
    config = load_config(config_path)
    bind_host = config["bind_host"]
    bind_port = int(config["bind_port"])
    timeout_seconds = int(config["timeout_seconds"])
    csv_path = Path(config["sensors_csv"])
    if not csv_path.is_absolute():
        csv_path = ROOT / csv_path

    stopping = False

    def stop(_signum, _frame):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((bind_host, bind_port))
    sock.settimeout(1.0)
    print(f"{utc_now_text()} aura receiver listening on {bind_host}:{bind_port}", flush=True)

    try:
        while not stopping:
            try:
                payload, address = sock.recvfrom(1024)
            except socket.timeout:
                mark_stale_sensors(csv_path, timeout_seconds)
                continue

            try:
                message = payload.decode("utf-8")
            except UnicodeDecodeError:
                print(f"{utc_now_text()} invalid heartbeat encoding from {address[0]}", flush=True)
                continue

            sensor_name = parse_heartbeat(message)
            if not sensor_name:
                print(f"{utc_now_text()} invalid heartbeat from {address[0]}", flush=True)
                continue

            update_heartbeat(csv_path, sensor_name, address[0], address[1])
            mark_stale_sensors(csv_path, timeout_seconds)
    finally:
        sock.close()
        print(f"{utc_now_text()} aura receiver stopped", flush=True)


def print_status(config_path):
    config = load_config(config_path)
    csv_path = Path(config["sensors_csv"])
    if not csv_path.is_absolute():
        csv_path = ROOT / csv_path
    rows = load_sensors(csv_path)

    print(f"{'NAME':<20} {'IP':<15} {'PORT':<7} {'STATUS':<8} LAST_CONTACT")
    for row in rows:
        print(
            f"{row['name']:<20} {row['ip']:<15} {row['port']:<7} "
            f"{row['status']:<8} {row['last_contact']}"
        )


def systemctl(action):
    return subprocess.call(["systemctl", "--no-pager", action, SERVICE_NAME])


def main():
    parser = argparse.ArgumentParser(description="Aura receiver")
    parser.add_argument(
        "command",
        choices=["run", "start", "stop", "status", "restart"],
        help="receiver command",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="receiver config path",
    )
    args = parser.parse_args()

    if args.command == "run":
        run_receiver(args.config)
        return 0
    if args.command == "status":
        print_status(args.config)
        return 0
    return systemctl(args.command)


if __name__ == "__main__":
    sys.exit(main())
