"""
Ticket Classification & Auto-Routing Service

Automatically categorizes incoming IT tickets as clinical or non-clinical,
assigns priority based on patient safety impact, and routes to the
appropriate IT team.
"""

import re
from datetime import datetime
from src.models.ticket import TicketCategory, TicketPriority, TicketCreate
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Keywords for classification
MEDICAL_DEVICE_KEYWORDS = [
    "infusion pump", "ventilator", "ecg", "ekg", "monitor", "defibrillator",
    "imaging", "mri", "ct scan", "ultrasound", "pacemaker", "glucometer",
    "pulse oximeter", "blood pressure", "patient monitor", "dialysis"
]

CLINICAL_KEYWORDS = [
    "icu", "ot", "operation theatre", "emergency", "er", "ward",
    "ehr", "emr", "clinical", "patient", "nurse", "doctor", "physician",
    "pharmacy", "lab", "radiology", "pathology", "surgical"
]

NON_CLINICAL_KEYWORDS = [
    "email", "printer", "laptop", "desktop", "wifi", "internet",
    "vpn", "password", "access", "login", "hr", "finance", "admin"
]

# Department priority map
CRITICAL_DEPARTMENTS = {"ICU", "OT", "ER", "NICU", "CCU", "Emergency", "Operation Theatre"}
HIGH_PRIORITY_DEPARTMENTS = {"Radiology", "Pharmacy", "Pathology", "Labor & Delivery"}


def classify_ticket(ticket: TicketCreate) -> tuple[TicketCategory, TicketPriority]:
    """
    Classify ticket category and assign priority based on:
    - Keywords in title and description
    - Department type
    - Device involvement
    """
    text = f"{ticket.title} {ticket.description}".lower()
    department = ticket.department.strip()

    # Step 1: Determine category
    category = _determine_category(text, ticket.device_id)

    # Step 2: Determine priority
    priority = _determine_priority(category, department, text)

    logger.info(f"Ticket classified | Category: {category} | Priority: {priority} | Dept: {department}")
    return category, priority


def _determine_category(text: str, device_id: str | None) -> TicketCategory:
    if device_id or any(kw in text for kw in MEDICAL_DEVICE_KEYWORDS):
        return TicketCategory.MEDICAL_DEVICE

    if any(kw in text for kw in CLINICAL_KEYWORDS):
        return TicketCategory.CLINICAL

    if "network" in text or "connectivity" in text or "wifi" in text:
        return TicketCategory.NETWORK

    if "software" in text or "application" in text or "crash" in text:
        return TicketCategory.SOFTWARE

    if "hardware" in text or "printer" in text or "keyboard" in text:
        return TicketCategory.HARDWARE

    return TicketCategory.NON_CLINICAL


def _determine_priority(
    category: TicketCategory,
    department: str,
    text: str
) -> TicketPriority:
    # Medical devices always critical
    if category == TicketCategory.MEDICAL_DEVICE:
        return TicketPriority.CRITICAL

    # Critical departments get high priority at minimum
    if department in CRITICAL_DEPARTMENTS:
        if category == TicketCategory.CLINICAL:
            return TicketPriority.CRITICAL
        return TicketPriority.HIGH

    if department in HIGH_PRIORITY_DEPARTMENTS:
        return TicketPriority.HIGH

    if category == TicketCategory.CLINICAL:
        return TicketPriority.HIGH

    # Check urgency keywords
    urgent_keywords = ["down", "not working", "failed", "offline", "urgent", "critical", "immediately"]
    if any(kw in text for kw in urgent_keywords):
        return TicketPriority.MEDIUM

    return TicketPriority.LOW


def auto_assign(category: TicketCategory, priority: TicketPriority) -> str:
    """
    Auto-assign ticket to the right IT team based on category and priority.
    """
    assignment_map = {
        TicketCategory.MEDICAL_DEVICE: "biomedical-engineering-team",
        TicketCategory.CLINICAL: "clinical-it-team",
        TicketCategory.NETWORK: "network-ops-team",
        TicketCategory.SOFTWARE: "software-support-team",
        TicketCategory.HARDWARE: "hardware-support-team",
        TicketCategory.NON_CLINICAL: "general-it-team",
    }

    assigned = assignment_map.get(category, "general-it-team")

    # Critical tickets also notify on-call lead
    if priority == TicketPriority.CRITICAL:
        logger.warning(f"CRITICAL ticket assigned to {assigned} — on-call lead notified")

    return assigned


def get_sla_minutes(priority: TicketPriority) -> int:
    """
    Return SLA resolution time in minutes based on priority.
    Aligned with hospital IT SLA standards.
    """
    sla_map = {
        TicketPriority.CRITICAL: 15,    # 15 minutes - patient safety risk
        TicketPriority.HIGH: 60,         # 1 hour
        TicketPriority.MEDIUM: 240,      # 4 hours
        TicketPriority.LOW: 1440,        # 24 hours
    }
    return sla_map[priority]
