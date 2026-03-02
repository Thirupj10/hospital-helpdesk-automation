"""
Hospital IT Helpdesk Automation System
Stryker Corporation - IT Service Delivery Internship
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import tickets, dashboard, devices
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Hospital IT Helpdesk Automation System",
    description="Automated IT service request management for hospital departments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(devices.router, prefix="/api/devices", tags=["Devices"])


@app.get("/")
def root():
    return {
        "message": "Hospital IT Helpdesk Automation System",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
