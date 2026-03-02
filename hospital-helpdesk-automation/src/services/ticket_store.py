"""
Ticket Store Service
In-memory ticket management with CRUD operations.
In production, replace with a database (PostgreSQL/SQLite).
"""

import uuid
from datetime import datetime
from typing import Optional
from src.models.ticket import Ticket, TicketCreate, TicketStatus
from src.services.classifier import classify_ticket, auto_assign, get_sla_minutes
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# In-memory store (replace with DB in production)
_tickets: dict[str, Ticket] = {}


def create_ticket(data: TicketCreate) -> Ticket:
    """Create a new ticket with auto-classification and routing."""
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow()

    category, priority = classify_ticket(data)
    assigned_to = auto_assign(category, priority)

    ticket = Ticket(
        id=ticket_id,
        title=data.title,
        description=data.description,
        department=data.department,
        reported_by=data.reported_by,
        device_id=data.device_id,
        category=category,
        priority=priority,
        status=TicketStatus.OPEN,
        assigned_to=assigned_to,
        created_at=now,
        updated_at=now
    )

    _tickets[ticket_id] = ticket
    logger.info(f"Ticket created: {ticket_id} | Priority: {priority} | Assigned: {assigned_to}")
    return ticket


def get_ticket(ticket_id: str) -> Optional[Ticket]:
    return _tickets.get(ticket_id)


def get_all_tickets(
    status: Optional[TicketStatus] = None,
    department: Optional[str] = None
) -> list[Ticket]:
    tickets = list(_tickets.values())
    if status:
        tickets = [t for t in tickets if t.status == status]
    if department:
        tickets = [t for t in tickets if t.department.lower() == department.lower()]
    return sorted(tickets, key=lambda t: t.created_at, reverse=True)


def update_ticket_status(ticket_id: str, new_status: TicketStatus) -> Optional[Ticket]:
    ticket = _tickets.get(ticket_id)
    if not ticket:
        return None

    now = datetime.utcnow()
    ticket.status = new_status
    ticket.updated_at = now

    if new_status == TicketStatus.RESOLVED:
        ticket.resolved_at = now
        delta = now - ticket.created_at
        ticket.resolution_time_minutes = int(delta.total_seconds() / 60)
        logger.info(f"Ticket {ticket_id} resolved in {ticket.resolution_time_minutes} minutes")

    return ticket


def get_stats() -> dict:
    tickets = list(_tickets.values())
    total = len(tickets)
    if total == 0:
        return {"total": 0}

    resolved = [t for t in tickets if t.resolved_at]
    avg_resolution = (
        sum(t.resolution_time_minutes for t in resolved if t.resolution_time_minutes) / len(resolved)
        if resolved else 0
    )

    return {
        "total": total,
        "open": len([t for t in tickets if t.status == TicketStatus.OPEN]),
        "in_progress": len([t for t in tickets if t.status == TicketStatus.IN_PROGRESS]),
        "resolved": len(resolved),
        "critical": len([t for t in tickets if t.priority.value == "critical"]),
        "avg_resolution_minutes": round(avg_resolution, 1),
        "by_department": _count_by_field(tickets, "department"),
        "by_category": _count_by_field(tickets, "category"),
    }


def _count_by_field(tickets: list, field: str) -> dict:
    result = {}
    for t in tickets:
        val = str(getattr(t, field).value if hasattr(getattr(t, field), 'value') else getattr(t, field))
        result[val] = result.get(val, 0) + 1
    return result
