"""
Ticket data models
"""

from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional


class TicketCategory(str, Enum):
    CLINICAL = "clinical"
    NON_CLINICAL = "non_clinical"
    MEDICAL_DEVICE = "medical_device"
    NETWORK = "network"
    SOFTWARE = "software"
    HARDWARE = "hardware"


class TicketPriority(str, Enum):
    CRITICAL = "critical"      # Medical device / patient safety
    HIGH = "high"              # Clinical systems down
    MEDIUM = "medium"          # Degraded performance
    LOW = "low"                # General IT request


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    department: str
    reported_by: str
    device_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Infusion pump connectivity lost in ICU",
                "description": "Three infusion pumps in ICU Ward 3 have lost network connectivity. Nurse station cannot monitor dosage remotely.",
                "department": "ICU",
                "reported_by": "nurse_station_3",
                "device_id": "PUMP-ICU-003"
            }
        }


class Ticket(BaseModel):
    id: str
    title: str
    description: str
    department: str
    reported_by: str
    device_id: Optional[str] = None
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_time_minutes: Optional[int] = None
