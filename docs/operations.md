# Aura Operations

Aura is designed to run under systemd with the receiver on the fake SIEM host
and sensors on remote test systems.

## Receiver Host

Install and start the receiver:

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

Check current sensor state:

```bash
sudo python3 /opt/apps/aura/receiver/aura.py status
```

If `/usr/local/bin/aurastatus` exists:

```bash
aurastatus
```

The receiver listens on UDP `0.0.0.0:5150` by default.

## Remote Sensor Host

Set the receiver address in `config/sensor.conf`:

```text
receiver_host=<receiver-ip>
receiver_port=5150
```

Install and start the sensor:

```bash
cd /opt/apps/aura
sudo cp systemd/aura-sensor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now aura-sensor.service
```

Check the remote sensor service:

```bash
systemctl --no-pager status aura-sensor.service
```

## Manual Test

Run the receiver and sensor in separate terminals:

```bash
python3 receiver/aura.py run
python3 sensor/aura_sensor.py run
```

Then check state:

```bash
python3 receiver/aura.py status
```
