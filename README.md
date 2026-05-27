# Aura

Aura is a lightweight heartbeat monitoring framework designed to validate autonomous operational workflows.

The project consists of two components:

- **Aura** — Receiver / Controller
- **Aura-Sensor** — Beacon / Heartbeat Agent

The system is intentionally minimalistic and designed as a proof-of-concept platform for future autonomous remediation and AI-driven ticketing workflows.

---

# Purpose

Aura exists to answer one simple question:

> "Is the sensor still alive?"

Aura-Sensor periodically sends heartbeat messages to the Aura receiver.

Aura tracks:
- Sensor name
- IP address
- Port
- Last contact timestamp
- Current status

No historical telemetry is stored.

No database exists.

No analytics engine exists.

This project is intentionally lightweight to validate:
- Service reliability
- Cross-platform agent deployment
- Autonomous monitoring workflows
- SIEM integration concepts
- AI-driven ticket generation and remediation

---

# Future State

The long-term objective is to integrate Aura with:
- SIEM platforms
- Autonomous ticketing systems
- AI remediation agents

Example workflow:

1. Aura-Sensor stops responding
2. Aura marks sensor as DOWN
3. SIEM detects outage
4. Ticket automatically generated
5. AI operations agent attempts service recovery
6. Sensor resumes heartbeat
7. Ticket automatically resolved

---

# Architecture

```text
+-------------------+
|   Aura-Sensor     |
|  Windows/Linux    |
| Heartbeat Beacon  |
+-------------------+
          |
          | heartbeat
          v
+-------------------+
|       Aura        |
| Receiver Service  |
| Status Tracker    |
+-------------------+
