import sqlite3
import json
import os

DB_FILE = "swarmroute.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            shipment_id TEXT PRIMARY KEY,
            user_email TEXT,
            source TEXT,
            destination TEXT,
            mode TEXT,
            status TEXT
        )
    ''')
    
    # Seamless Migration if the database was already created in last steps
    cursor.execute("PRAGMA table_info(shipments)")
    columns = [col[1] for col in cursor.fetchall()]
    if "user_email" not in columns:
        cursor.execute("ALTER TABLE shipments ADD COLUMN user_email TEXT")
        cursor.execute("UPDATE shipments SET user_email = 'operator@swarmroute.ai' WHERE user_email IS NULL")
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            route_id TEXT PRIMARY KEY,
            shipment_id TEXT,
            path TEXT,
            distance REAL,
            risk REAL,
            time_hours REAL,
            cost REAL,
            route_type TEXT
        )
    ''')
    cursor.execute("PRAGMA table_info(routes)")
    route_columns = [col[1] for col in cursor.fetchall()]
    if "route_type" not in route_columns:
        cursor.execute("ALTER TABLE routes ADD COLUMN route_type TEXT DEFAULT 'Primary'")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS risk_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_id TEXT,
            timestamp TEXT,
            risk_score REAL,
            event TEXT,
            explanation TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute('INSERT INTO users VALUES (?, ?)', (email, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()
    return success

def get_user(email):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT email, password FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    return {"email": row[0], "password": row[1]} if row else None

def save_shipment(shipment_id, user_email, source, destination, mode, status="Pending"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO shipments (shipment_id, user_email, source, destination, mode, status) VALUES (?, ?, ?, ?, ?, ?)',
                   (shipment_id, user_email, json.dumps(source), json.dumps(destination), mode, status))
    conn.commit()
    conn.close()

def save_routes(routes_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for r in routes_data:
        cursor.execute('''
            INSERT OR REPLACE INTO routes (route_id, shipment_id, path, distance, risk, time_hours, cost, route_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (r['route_id'], r.get('shipment_id', ''), json.dumps(r.get('path', [])), r.get('distance', 0), r.get('risk', 0), r.get('time_hours', 1), r.get('cost', 100), r.get('type', 'Primary')))
    conn.commit()
    conn.close()

def log_risk(shipment_id, timestamp, risk_score, event, explanation):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO risk_logs (shipment_id, timestamp, risk_score, event, explanation)
        VALUES (?, ?, ?, ?, ?)
    ''', (shipment_id, timestamp, risk_score, event, explanation))
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()
