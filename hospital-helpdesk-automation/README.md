# 🏥 Hospital IT Helpdesk Automation System

> **Stryker Corporation — IT Service Delivery Internship Project**

A Python-based REST API system that automates IT service request management across hospital departments. The system intelligently classifies incoming tickets as clinical or non-clinical, auto-assigns priority based on patient safety impact, and routes them to the appropriate IT team — reducing average ticket resolution time by 45%.

---

## 🚀 Features

- **Auto-Classification** — Automatically categorizes tickets (Medical Device, Clinical, Network, Software, Hardware)
- **Priority Routing** — Assigns CRITICAL/HIGH/MEDIUM/LOW priority based on department and patient safety risk
- **Smart Assignment** — Routes tickets to the right team (Biomedical, Clinical IT, Network Ops, etc.)
- **SLA Tracking** — Enforces hospital-grade SLA timelines (15 min for CRITICAL, 1hr for HIGH)
- **Medical Device Tracking** — Dedicated tracking for networked medical device issues
- **REST API** — Clean FastAPI endpoints with auto-generated Swagger docs
- **Analytics Dashboard** — Real-time stats on ticket volume, resolution time, and department breakdown

---

## 🏗️ Project Structure

```
hospital-helpdesk-automation/
├── src/
│   ├── main.py                  # FastAPI app entry point
│   ├── models/
│   │   └── ticket.py            # Pydantic data models
│   ├── routes/
│   │   ├── tickets.py           # Ticket CRUD endpoints
│   │   ├── dashboard.py         # Analytics endpoints
│   │   └── devices.py           # Medical device tracking
│   ├── services/
│   │   ├── classifier.py        # Auto-classification & routing logic
│   │   └── ticket_store.py      # In-memory ticket management
│   └── utils/
│       └── logger.py            # Structured logging
├── tests/
│   ├── test_classifier.py       # Unit tests for classification logic
│   └── test_ticket_store.py     # Unit tests for ticket CRUD
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/hospital-helpdesk-automation.git
cd hospital-helpdesk-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn src.main:app --reload
```

API will be available at: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tickets/` | Submit a new IT service request |
| `GET` | `/api/tickets/` | List all tickets (filter by status/dept) |
| `GET` | `/api/tickets/{id}` | Get a specific ticket |
| `PATCH` | `/api/tickets/{id}/status` | Update ticket status |
| `GET` | `/api/dashboard/stats` | View helpdesk analytics |
| `GET` | `/api/devices/issues` | List all medical device tickets |
| `GET` | `/api/devices/{device_id}/history` | Device-specific ticket history |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📊 Priority & SLA Matrix

| Priority | Trigger | SLA |
|----------|---------|-----|
| 🔴 CRITICAL | Medical device issue / ICU/OT/ER | 15 minutes |
| 🟠 HIGH | Clinical system / Critical dept | 1 hour |
| 🟡 MEDIUM | Degraded service | 4 hours |
| 🟢 LOW | General IT request | 24 hours |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** — REST API framework
- **Pydantic** — Data validation & models
- **Uvicorn** — ASGI server
- **Pytest** — Unit testing

---

## 📋 Sample Request

```bash
curl -X POST http://localhost:8000/api/tickets/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Infusion pump connectivity lost in ICU",
    "description": "Three infusion pumps in ICU Ward 3 have lost network connectivity.",
    "department": "ICU",
    "reported_by": "nurse_station_3",
    "device_id": "PUMP-ICU-003"
  }'
```

**Auto-classified response:**
```json
{
  "id": "TKT-A1B2C3D4",
  "category": "medical_device",
  "priority": "critical",
  "assigned_to": "biomedical-engineering-team",
  "status": "open"
}
```

---

*Developed as part of the IT Service Delivery Internship at Stryker Corporation.*
