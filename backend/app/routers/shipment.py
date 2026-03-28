from fastapi import APIRouter
from app.models.shipment import ShipmentInput, RouteResult
from app.agents import swarm
import sqlite3
import json
import math
from app.services.db import DB_FILE

router = APIRouter()

@router.get("/")
def get_shipments(user_email: str = ""):
    """Fetches user-specific real database shipments and reconstructs geometric routes"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if user_email:
        cursor.execute('SELECT shipment_id, source, destination, mode, status FROM shipments WHERE user_email = ? ORDER BY shipment_id DESC', (user_email,))
    else:
        cursor.execute('SELECT shipment_id, source, destination, mode, status FROM shipments ORDER BY shipment_id DESC')
    rows = cursor.fetchall()
    
    results = []
    for r in rows:
        shipment_id = r[0]
        src = json.loads(r[1])
        dest = json.loads(r[2])
        
        # Pull associated Routes back out of DB
        cursor.execute('SELECT route_id, route_type, distance, time_hours, cost, risk, path FROM routes WHERE shipment_id = ? ORDER BY cost ASC', (shipment_id,))
        route_rows = cursor.fetchall()
        
        parsed_routes = []
        for idx, rr in enumerate(route_rows):
            time_h = rr[3]
            str_time = f"{math.floor(time_h)}h {round((time_h % 1) * 60)}m"
            
            parsed_routes.append({
                "id": rr[0],
                "name": rr[1],
                "time": str_time,
                "cost": f"${round(rr[4])}",
                "risk": round(rr[5] * 100) if rr[5] < 1.0 else round(rr[5]), # Safeguard for older arrays
                "active": idx == 0,
                "waypoints": [],
                "path": json.loads(rr[6]) if rr[6] else []
            })
            
        # Defaults if legacy rows lacked route injection
        if not parsed_routes:
            parsed_routes = [{
                "id": "legacy-0",
                "name": "Fallback Route",
                "time": "24h 0m",
                "cost": "$5000",
                "risk": 10,
                "active": True,
                "waypoints": [],
                "path": []
            }]
            
        state_src = f"{src.get('state')}, " if src.get('state') and src.get('state') != 'Unknown' else ""
        state_dest = f"{dest.get('state')}, " if dest.get('state') and dest.get('state') != 'Unknown' else ""
        
        results.append({
            "id": shipment_id,
            "source": f"{src.get('city', '')}, {state_src}{src.get('country', '')}",
            "destination": f"{dest.get('city', '')}, {state_dest}{dest.get('country', '')}",
            "transportMode": r[3],
            "status": 'in-transit',
            "riskScore": parsed_routes[0]["risk"],
            "progress": 5, # Basic dynamic mock
            "eta": "Live Tracking...",
            "routes": parsed_routes,
            "sourceCoords": [src.get('lat', 40.0), src.get('lon', -70.0)],
            "destCoords": [dest.get('lat', 50.0), dest.get('lon', 2.0)],
            "activeRouteIndex": 0
        })
    conn.close()
    return {"shipments": results}

@router.post("/", response_model=RouteResult)
async def create_shipment(shipment: ShipmentInput):
    result = swarm.process_shipment(shipment)
    return RouteResult(**result)

from app.models.shipment import IntelligentShipmentInput

@router.post("/intelligent", response_model=RouteResult)
async def create_intelligent_shipment(data: IntelligentShipmentInput):
    from app.services.ai import plan_shipment_context
    from datetime import datetime
    from app.models.shipment import Location, ShipmentInput

    parsed = plan_shipment_context(
        data.source_query, 
        data.destination_query, 
        data.departure_time, 
        data.deadline, 
        data.mode
    )
    
    try:
        dep_time = datetime.fromisoformat(data.departure_time.replace('Z', '+00:00'))
        deadline = datetime.fromisoformat(data.deadline.replace('Z', '+00:00'))
    except Exception:
        dep_time = datetime.now()
        deadline = datetime.now()

    shipment = ShipmentInput(
        user_email=data.user_email,
        source=Location(**parsed["source"]),
        destination=Location(**parsed["destination"]),
        mode=data.mode,
        shipment_type=data.shipment_type,
        departure_time=dep_time,
        deadline=deadline
    )
    
    result = swarm.process_shipment(shipment)
    
    # Attach parsed locations back for the frontend to use
    result["source_parsed"] = parsed["source"]
    result["destination_parsed"] = parsed["destination"]
    
    return RouteResult(**result)
