"""
Ticket Routes - REST API endpoints for ticket management
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from src.models.ticket import TicketCreate, Ticket, TicketStatus
from src.services import ticket_store

router = APIRouter()


@router.post("/", response_model=Ticket, status_code=201)
def create_ticket(ticket_data: TicketCreate):
    """
    Submit a new IT service request.
    Auto-classifies category, assigns priority, and routes to appropriate team.
    """
    return ticket_store.create_ticket(ticket_data)


@router.get("/", response_model=list[Ticket])
def list_tickets(
    status: Optional[TicketStatus] = Query(None),
    department: Optional[str] = Query(None)
):
    """List all tickets with optional filters."""
    return ticket_store.get_all_tickets(status=status, department=department)


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str):
    """Get a specific ticket by ID."""
    ticket = ticket_store.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return ticket


@router.patch("/{ticket_id}/status", response_model=Ticket)
def update_status(ticket_id: str, status: TicketStatus):
    """Update the status of a ticket."""
    ticket = ticket_store.update_ticket_status(ticket_id, status)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return ticket
