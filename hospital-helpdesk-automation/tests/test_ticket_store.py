"""
Tests for ticket store CRUD operations.
"""

import pytest
from src.models.ticket import TicketCreate, TicketStatus
from src.services import ticket_store


@pytest.fixture(autouse=True)
def clear_store():
    """Clear ticket store before each test."""
    ticket_store._tickets.clear()
    yield
    ticket_store._tickets.clear()


def make_ticket_data(**kwargs):
    defaults = {
        "title": "Test printer not working",
        "description": "Printer on 2nd floor admin is not responding",
        "department": "Admin",
        "reported_by": "test_user"
    }
    defaults.update(kwargs)
    return TicketCreate(**defaults)


class TestTicketStore:

    def test_create_ticket_returns_ticket_with_id(self):
        data = make_ticket_data()
        ticket = ticket_store.create_ticket(data)
        assert ticket.id.startswith("TKT-")
        assert ticket.status == TicketStatus.OPEN
        assert ticket.assigned_to is not None

    def test_get_ticket_by_id(self):
        data = make_ticket_data()
        created = ticket_store.create_ticket(data)
        fetched = ticket_store.get_ticket(created.id)
        assert fetched is not None
        assert fetched.id == created.id

    def test_get_nonexistent_ticket_returns_none(self):
        result = ticket_store.get_ticket("TKT-INVALID")
        assert result is None

    def test_update_ticket_status_to_resolved(self):
        data = make_ticket_data()
        ticket = ticket_store.create_ticket(data)
        updated = ticket_store.update_ticket_status(ticket.id, TicketStatus.RESOLVED)
        assert updated.status == TicketStatus.RESOLVED
        assert updated.resolved_at is not None
        assert updated.resolution_time_minutes is not None

    def test_filter_tickets_by_department(self):
        ticket_store.create_ticket(make_ticket_data(department="ICU", title="ICU device issue", description="Device not working in ICU ward immediately"))
        ticket_store.create_ticket(make_ticket_data(department="Admin", title="Admin printer issue", description="Printer not working in admin office"))
        icu_tickets = ticket_store.get_all_tickets(department="ICU")
        assert len(icu_tickets) == 1
        assert icu_tickets[0].department == "ICU"

    def test_stats_returns_correct_total(self):
        ticket_store.create_ticket(make_ticket_data())
        ticket_store.create_ticket(make_ticket_data(title="Another issue", description="Another IT issue in department"))
        stats = ticket_store.get_stats()
        assert stats["total"] == 2
