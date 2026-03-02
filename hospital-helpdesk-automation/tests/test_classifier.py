"""
Unit tests for ticket classification and routing logic.
"""

import pytest
from src.models.ticket import TicketCreate, TicketCategory, TicketPriority
from src.services.classifier import classify_ticket, auto_assign, get_sla_minutes


def make_ticket(title, description, department, device_id=None):
    return TicketCreate(
        title=title,
        description=description,
        department=department,
        reported_by="test_user",
        device_id=device_id
    )


class TestClassification:

    def test_medical_device_ticket(self):
        ticket = make_ticket(
            "Infusion pump offline",
            "Infusion pump not connecting to network in ICU",
            "ICU",
            device_id="PUMP-001"
        )
        category, priority = classify_ticket(ticket)
        assert category == TicketCategory.MEDICAL_DEVICE
        assert priority == TicketPriority.CRITICAL

    def test_clinical_ticket_in_icu(self):
        ticket = make_ticket(
            "EHR system down",
            "Clinical EHR system not loading for doctors in ICU",
            "ICU"
        )
        category, priority = classify_ticket(ticket)
        assert priority == TicketPriority.CRITICAL

    def test_non_clinical_low_priority(self):
        ticket = make_ticket(
            "Email not working",
            "Cannot access email on my laptop in HR department",
            "HR"
        )
        category, priority = classify_ticket(ticket)
        assert category in [TicketCategory.NON_CLINICAL, TicketCategory.SOFTWARE, TicketCategory.HARDWARE]
        assert priority == TicketPriority.LOW

    def test_network_issue_non_critical_dept(self):
        ticket = make_ticket(
            "WiFi connectivity issue",
            "WiFi not working in admin block",
            "Admin"
        )
        category, priority = classify_ticket(ticket)
        assert category == TicketCategory.NETWORK


class TestAutoAssign:

    def test_medical_device_assigned_to_biomedical(self):
        team = auto_assign(TicketCategory.MEDICAL_DEVICE, TicketPriority.CRITICAL)
        assert team == "biomedical-engineering-team"

    def test_clinical_assigned_to_clinical_it(self):
        team = auto_assign(TicketCategory.CLINICAL, TicketPriority.HIGH)
        assert team == "clinical-it-team"

    def test_network_assigned_to_network_ops(self):
        team = auto_assign(TicketCategory.NETWORK, TicketPriority.MEDIUM)
        assert team == "network-ops-team"


class TestSLA:

    def test_critical_sla_is_15_minutes(self):
        assert get_sla_minutes(TicketPriority.CRITICAL) == 15

    def test_low_sla_is_24_hours(self):
        assert get_sla_minutes(TicketPriority.LOW) == 1440
