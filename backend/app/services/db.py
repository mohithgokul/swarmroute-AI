import psycopg2
import json
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost:5432/postgres")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
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
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name='shipments'
    """)
    columns = [row[0] for row in cursor.fetchall()]
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
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name='routes'
    """)
    route_columns = [row[0] for row in cursor.fetchall()]
    if "route_type" not in route_columns:
        cursor.execute("ALTER TABLE routes ADD COLUMN route_type TEXT DEFAULT 'Primary'")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS risk_logs (
            log_id SERIAL PRIMARY KEY,
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
    conn = get_db_connection()
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute('INSERT INTO users VALUES (%s, %s)', (email, password))
        conn.commit()
        success = True
    except psycopg2.IntegrityError:
        pass
    except Exception as e:
        print("Registration err:", e)
    finally:
        conn.close()
    return success

def get_user(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT email, password FROM users WHERE email = %s', (email,))
    row = cursor.fetchone()
    conn.close()
    return {"email": row[0], "password": row[1]} if row else None

def save_shipment(shipment_id, user_email, source, destination, mode, status="Pending"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO shipments (shipment_id, user_email, source, destination, mode, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (shipment_id) DO UPDATE SET
            user_email = EXCLUDED.user_email,
            source = EXCLUDED.source,
            destination = EXCLUDED.destination,
            mode = EXCLUDED.mode,
            status = EXCLUDED.status
    ''', (shipment_id, user_email, json.dumps(source), json.dumps(destination), mode, status))
    conn.commit()
    conn.close()

def save_routes(routes_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    for r in routes_data:
        cursor.execute('''
            INSERT INTO routes (route_id, shipment_id, path, distance, risk, time_hours, cost, route_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (route_id) DO UPDATE SET
                shipment_id = EXCLUDED.shipment_id,
                path = EXCLUDED.path,
                distance = EXCLUDED.distance,
                risk = EXCLUDED.risk,
                time_hours = EXCLUDED.time_hours,
                cost = EXCLUDED.cost,
                route_type = EXCLUDED.route_type
        ''', (r['route_id'], r.get('shipment_id', ''), json.dumps(r.get('path', [])), r.get('distance', 0), r.get('risk', 0), r.get('time_hours', 1), r.get('cost', 100), r.get('type', 'Primary')))
    conn.commit()
    conn.close()

def log_risk(shipment_id, timestamp, risk_score, event, explanation):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO risk_logs (shipment_id, timestamp, risk_score, event, explanation)
        VALUES (%s, %s, %s, %s, %s)
    ''', (shipment_id, timestamp, risk_score, event, explanation))
    conn.commit()
    conn.close()

try:
    init_db()
except Exception as e:
    print(f"PostgreSQL initialization failed. This is expected during Docker build without env vars. error: {e}")
