from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class Location(BaseModel):
    city: str
    country: str
    lat: Optional[float] = None
    lon: Optional[float] = None

class ShipmentInput(BaseModel):
    user_email: str = Field(description="Email of user requesting shipment")
    source: Location
    destination: Location
    mode: str = Field(description="Mode of transport: road, air, sea, rail")
    shipment_type: str = Field(description="Fragile, bulk, standard, etc.")
    departure_time: datetime
    deadline: datetime

class Option(BaseModel):
    mode: str
    cost: float
    time_hours: float
    risk_score: float
    recommendation: str

class RouteResult(BaseModel):
    shipment_id: str
    classification: str
    activated_agents: List[str]
    best_route_description: str
    composite_risk_score: float
    transport_options: List[Option]
    routes: List[dict] = Field(default_factory=list)
    status: str
