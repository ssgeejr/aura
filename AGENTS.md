# AGENTS.md

# Aura Autonomous Agent Instructions

## Project

Aura

---

# Purpose

Aura is a lightweight heartbeat monitoring framework designed to validate autonomous operational workflows.

The project consists of:

- Aura (Receiver)
- Aura-Sensor (Beacon)

This software is intentionally minimalistic.

The current objective is ONLY:
- detect whether a sensor is alive
- track current state
- support autonomous ticketing validation

This is NOT:
- a SIEM
- an EDR
- a telemetry platform
- a logging framework
- a monitoring dashboard

Do not introduce unnecessary complexity.

---

# Operational Philosophy

Aura must remain:

- lightweight
- deterministic
- easy to debug
- dependency minimal
- cross-platform
- service-oriented

If a proposed feature increases complexity significantly, it should be rejected unless explicitly approved.

---

# Architecture Rules

## Receiver (Aura)

Responsibilities:
- receive heartbeats
- track sensor state
- update last contact time
- determine UP/DOWN state
- expose service status

Aura MUST NOT:
- store historical telemetry
- use databases
- implement dashboards
- perform analytics
- perform vulnerability scanning
- collect system metrics

---

## Sensor (Aura-Sensor)

Responsibilities:
- send heartbeat messages
- run quietly as a service
- support Linux and Windows
- consume minimal CPU/memory

Aura-Sensor MUST NOT:
- perform scanning
- perform monitoring
- collect telemetry
- implement persistence logic outside service management
- store large local logs

---

# Configuration Rules

The configuration format must remain:
- human readable
- flat-file based
- dependency minimal

Preferred format:
- CSV

Required fields:

| Field | Description |
|---|---|
| name | Sensor identifier |
| ip | Sensor IP |
| port | Sensor listening port |
| last_contact | Last heartbeat timestamp |
| status | UP/DOWN/UNKNOWN |

Example:

```csv
name,ip,port,last_contact,status
sensor01,192.168.1.50,5150,2026-05-27T08:00:00Z,UP
```

No database integrations are permitted.

---

# Service Requirements

Both components must support:

```bash
start
stop
status
restart
```

Linux:
- systemd preferred

Windows:
- native Windows Service support preferred

---

# Coding Standards

## Language

Primary language:
- Python 3

Avoid:
- unnecessary frameworks
- heavy abstractions
- enterprise architecture patterns

Preferred:
- standard library
- simple threading
- straightforward socket handling
- readable code

---

# Logging

Logging should remain minimal.

Acceptable:
- startup messages
- shutdown messages
- heartbeat receipt
- sensor timeout events
- fatal errors

Avoid:
- verbose debug spam
- telemetry collection
- excessive disk writes

---

# Network Behavior

Heartbeat traffic should remain extremely small.

Preferred model:
- simple TCP or UDP heartbeat

Example:

```text
sensor01|alive
```

---

# Failure Philosophy

Aura should:
- fail simply
- fail visibly
- recover cleanly

Avoid:
- hidden retry storms
- complex queueing systems
- automatic backoff frameworks

Operational simplicity is preferred over feature richness.

---

# Future State

Future integrations may include:
- SIEM ingestion
- automated ticket creation
- AI remediation agents
- autonomous restart workflows

However:

Future integrations MUST remain external to Aura itself whenever possible.

Aura should remain:
- a beacon
- a receiver
- a state tracker

Nothing more.

---

# Repository Expectations

Expected repository structure:

```text
/aura
    /receiver
    /sensor
    /config
    /docs
```

---

# Security Expectations

Aura is internal infrastructure software.

Do not:
- expose management interfaces publicly
- implement remote code execution features
- add embedded scripting engines
- introduce plugin execution systems

Keep attack surface minimal.

---

# Agent Guidance

When modifying Aura:

Prefer:
- simplicity
- readability
- deterministic behavior
- operational reliability

Reject:
- unnecessary abstractions
- premature optimization
- enterprise bloat
- unnecessary dependencies

Aura is intentionally small by design.
# AGENTS.md

# Aura Autonomous Agent Instructions

## Project

Aura

---

# Purpose

Aura is a lightweight heartbeat monitoring framework designed to validate autonomous operational workflows.

The project consists of:

- Aura (Receiver)
- Aura-Sensor (Beacon)

This software is intentionally minimalistic.

The current objective is ONLY:
- detect whether a sensor is alive
- track current state
- support autonomous ticketing validation

This is NOT:
- a SIEM
- an EDR
- a telemetry platform
- a logging framework
- a monitoring dashboard

Do not introduce unnecessary complexity.

---

# Operational Philosophy

Aura must remain:

- lightweight
- deterministic
- easy to debug
- dependency minimal
- cross-platform
- service-oriented

If a proposed feature increases complexity significantly, it should be rejected unless explicitly approved.

---

# Architecture Rules

## Receiver (Aura)

Responsibilities:
- receive heartbeats
- track sensor state
- update last contact time
- determine UP/DOWN state
- expose service status

Aura MUST NOT:
- store historical telemetry
- use databases
- implement dashboards
- perform analytics
- perform vulnerability scanning
- collect system metrics

---

## Sensor (Aura-Sensor)

Responsibilities:
- send heartbeat messages
- run quietly as a service
- support Linux and Windows
- consume minimal CPU/memory

Aura-Sensor MUST NOT:
- perform scanning
- perform monitoring
- collect telemetry
- implement persistence logic outside service management
- store large local logs

---

# Configuration Rules

The configuration format must remain:
- human readable
- flat-file based
- dependency minimal

Preferred format:
- CSV

Required fields:

| Field | Description |
|---|---|
| name | Sensor identifier |
| ip | Sensor IP |
| port | Sensor listening port |
| last_contact | Last heartbeat timestamp |
| status | UP/DOWN/UNKNOWN |

Example:

```csv
name,ip,port,last_contact,status
sensor01,192.168.1.50,5150,2026-05-27T08:00:00Z,UP
```

No database integrations are permitted.

---

# Service Requirements

Both components must support:

```bash
start
stop
status
restart
```

Linux:
- systemd preferred

Windows:
- native Windows Service support preferred

---

# Coding Standards

## Language

Primary language:
- Python 3

Avoid:
- unnecessary frameworks
- heavy abstractions
- enterprise architecture patterns

Preferred:
- standard library
- simple threading
- straightforward socket handling
- readable code

---

# Logging

Logging should remain minimal.

Acceptable:
- startup messages
- shutdown messages
- heartbeat receipt
- sensor timeout events
- fatal errors

Avoid:
- verbose debug spam
- telemetry collection
- excessive disk writes

---

# Network Behavior

Heartbeat traffic should remain extremely small.

Preferred model:
- simple TCP or UDP heartbeat

Example:

```text
sensor01|alive
```

---

# Failure Philosophy

Aura should:
- fail simply
- fail visibly
- recover cleanly

Avoid:
- hidden retry storms
- complex queueing systems
- automatic backoff frameworks

Operational simplicity is preferred over feature richness.

---

# Future State

Future integrations may include:
- SIEM ingestion
- automated ticket creation
- AI remediation agents
- autonomous restart workflows

However:

Future integrations MUST remain external to Aura itself whenever possible.

Aura should remain:
- a beacon
- a receiver
- a state tracker

Nothing more.

---

# Repository Expectations

Expected repository structure:

```text
/aura
    /receiver
    /sensor
    /config
    /docs
```

---

# Security Expectations

Aura is internal infrastructure software.

Do not:
- expose management interfaces publicly
- implement remote code execution features
- add embedded scripting engines
- introduce plugin execution systems

Keep attack surface minimal.

---

# Agent Guidance

When modifying Aura:

Prefer:
- simplicity
- readability
- deterministic behavior
- operational reliability

Reject:
- unnecessary abstractions
- premature optimization
- enterprise bloat
- unnecessary dependencies

Aura is intentionally small by design.

