"""
Device Routes - Medical device IT issue tracking
"""

from fastapi import APIRouter, HTTPException
from src.services import ticket_store
from src.models.ticket import TicketCategory

router = APIRouter()


@router.get("/issues")
def get_device_issues():
    """Get all open tickets related to medical devices."""
    all_tickets = ticket_store.get_all_tickets()
    device_tickets = [
        t for t in all_tickets
        if t.category == TicketCategory.MEDICAL_DEVICE
    ]
    return {
        "total_device_issues": len(device_tickets),
        "tickets": device_tickets
    }


@router.get("/{device_id}/history")
def get_device_history(device_id: str):
    """Get ticket history for a specific medical device."""
    all_tickets = ticket_store.get_all_tickets()
    device_tickets = [t for t in all_tickets if t.device_id == device_id]
    if not device_tickets:
        raise HTTPException(status_code=404, detail=f"No tickets found for device {device_id}")
    return {"device_id": device_id, "tickets": device_tickets}
