# Aura Protocol

Aura uses a minimal UDP heartbeat.

```text
sensor01|alive
```

The receiver accepts only messages with two fields separated by `|`.
The second field must be `alive`.

Unknown sensor names are ignored. Sensors must exist in `config/sensors.csv`
before their heartbeats can update state.
