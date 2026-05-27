# Aura

Aura is a lightweight heartbeat receiver used as a fake SIEM target for
autonomous workflow validation.

It answers one question:

```text
Is the sensor still alive?
```

Aura is intentionally small. It receives UDP heartbeats, tracks current sensor
state in a CSV file, and exposes a simple status command. It does not store
history, run analytics, provide a dashboard, or create tickets.

## Components

- **Aura receiver**: runs on the fake SIEM host, such as Phaeton.
- **Aura sensor**: runs only on remote test systems that should report in.

The receiver does not need the sensor service installed locally unless the
receiver host is also being used as a test sensor.

## Protocol

Sensors send a tiny UDP heartbeat:

```text
sensor01|alive
```

The receiver updates only sensors already listed in `config/sensors.csv`.
Unknown sensors are ignored.

## Configuration

Receiver defaults are in `config/receiver.conf`:

```text
bind_host=0.0.0.0
bind_port=5150
timeout_seconds=90
sensors_csv=config/sensors.csv
```

Sensor defaults are in `config/sensor.conf`:

```text
name=sensor01
receiver_host=127.0.0.1
receiver_port=5150
interval_seconds=30
```

For remote sensors, set `receiver_host` to the receiver host IP address.

Current state is stored in `config/sensors.csv`:

```csv
name,ip,port,last_contact,status
sensor01,127.0.0.1,5150,,UNKNOWN
```

## Install Receiver On Phaeton

```bash
cd /opt/apps/aura
sudo cp systemd/aura.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now aura.service
```

Check the receiver service:

```bash
systemctl --no-pager status aura.service
```

Check sensor state:

```bash
sudo python3 /opt/apps/aura/receiver/aura.py status
```

If `/usr/local/bin/aurastatus` is installed on the receiver, use:

```bash
aurastatus
```

## Install Sensor On A Remote Test Host

Edit `config/sensor.conf` on the remote host:

```text
name=sensor01
receiver_host=<phaeton-ip>
receiver_port=5150
interval_seconds=30
```

Install and start the sensor service:

```bash
cd /opt/apps/aura
sudo cp systemd/aura-sensor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now aura-sensor.service
```

Check the sensor service:

```bash
systemctl --no-pager status aura-sensor.service
```

## Local Foreground Test

Run the receiver:

```bash
python3 receiver/aura.py run
```

Run the sensor in another terminal:

```bash
python3 sensor/aura_sensor.py run
```

Then check status:

```bash
python3 receiver/aura.py status
```

Status values:

- `UNKNOWN`: no heartbeat has been received yet.
- `UP`: a heartbeat was received within the timeout window.
- `DOWN`: no heartbeat was received within `timeout_seconds`.

## Design Boundaries

Aura is only a beacon receiver and state tracker. Future ticketing, SIEM
ingestion, remediation, and AI workflows should remain external integrations.
