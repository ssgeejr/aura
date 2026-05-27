#!/usr/bin/env python3
"""Aura UDP heartbeat sensor."""

import argparse
import signal
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "sensor.conf"
SERVICE_NAME = "aura-sensor.service"


def utc_now_text():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_config(path):
    config = {
        "name": "sensor01",
        "receiver_host": "127.0.0.1",
        "receiver_port": "5150",
        "interval_seconds": "30",
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


def run_sensor(config_path):
    config = load_config(config_path)
    name = config["name"]
    receiver_host = config["receiver_host"]
    receiver_port = int(config["receiver_port"])
    interval_seconds = int(config["interval_seconds"])
    message = f"{name}|alive".encode("utf-8")
    stopping = False

    def stop(_signum, _frame):
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(
        f"{utc_now_text()} aura sensor {name} sending to {receiver_host}:{receiver_port}",
        flush=True,
    )

    try:
        while not stopping:
            try:
                sock.sendto(message, (receiver_host, receiver_port))
            except OSError as exc:
                print(f"{utc_now_text()} heartbeat send failed: {exc}", flush=True)
            end = time.monotonic() + interval_seconds
            while not stopping and time.monotonic() < end:
                time.sleep(0.2)
    finally:
        sock.close()
        print(f"{utc_now_text()} aura sensor stopped", flush=True)


def systemctl(action):
    return subprocess.call(["systemctl", "--no-pager", action, SERVICE_NAME])


def main():
    parser = argparse.ArgumentParser(description="Aura sensor")
    parser.add_argument(
        "command",
        choices=["run", "start", "stop", "status", "restart"],
        help="sensor command",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="sensor config path",
    )
    args = parser.parse_args()

    if args.command == "run":
        run_sensor(args.config)
        return 0
    return systemctl(args.command)


if __name__ == "__main__":
    sys.exit(main())
