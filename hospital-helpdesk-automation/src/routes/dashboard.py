"""
Dashboard Routes - Summary stats and analytics
"""

from fastapi import APIRouter
from src.services import ticket_store

router = APIRouter()


@router.get("/stats")
def get_stats():
    """
    Get helpdesk performance statistics.
    Tracks ticket volume, resolution time, and SLA compliance.
    """
    return ticket_store.get_stats()
