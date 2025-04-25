import os
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import streamlit as st
import time

# Get database connection parameters from environment variables
DB_HOST = os.environ.get('PGHOST', 'localhost')
DB_PORT = os.environ.get('PGPORT', '5432')
DB_NAME = os.environ.get('PGDATABASE', 'postgres')
DB_USER = os.environ.get('PGUSER', 'postgres')
DB_PASSWORD = os.environ.get('PGPASSWORD', '')

def get_connection():
    """Get a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return None

def init_database():
    """Initialize the database with required tables."""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # Create strawberry_readings table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS strawberry_readings (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                variety VARCHAR(50) NOT NULL,
                time_of_day VARCHAR(20) NOT NULL,
                ph NUMERIC(4,2) NOT NULL,
                ec_ms_cm NUMERIC(4,2) NOT NULL,
                humidity_pct NUMERIC(5,2) NOT NULL,
                water_temp_c NUMERIC(4,2) NOT NULL,
                air_temp_c NUMERIC(4,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create user_systems table to store user system settings
            cur.execute("""
            CREATE TABLE IF NOT EXISTS user_systems (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL,
                system_name VARCHAR(100) NOT NULL,
                variety VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create alerts table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100) NOT NULL,
                system_id INTEGER REFERENCES user_systems(id),
                alert_type VARCHAR(50) NOT NULL,
                parameter VARCHAR(50) NOT NULL,
                value NUMERIC(5,2) NOT NULL,
                threshold NUMERIC(5,2) NOT NULL,
                message TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP
            )
            """)
            
            conn.commit()
            
            return True
    except Exception as e:
        st.error(f"Error initializing database: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def import_csv_to_database(csv_path):
    """Import CSV data to the PostgreSQL database."""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        df = pd.read_csv(csv_path)
        
        # Convert column names to match database schema
        df.columns = [
            'date', 'variety', 'time_of_day', 'ph', 
            'ec_ms_cm', 'humidity_pct', 'water_temp_c', 'air_temp_c'
        ]
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Insert data into the database
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                cur.execute("""
                INSERT INTO strawberry_readings 
                (date, variety, time_of_day, ph, ec_ms_cm, humidity_pct, water_temp_c, air_temp_c)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['date'], row['variety'], row['time_of_day'], 
                    row['ph'], row['ec_ms_cm'], row['humidity_pct'], 
                    row['water_temp_c'], row['air_temp_c']
                ))
            
            conn.commit()
            
        return True
    except Exception as e:
        st.error(f"Error importing CSV to database: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_latest_readings():
    """Get the latest readings for each variety from the database."""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
            WITH latest_dates AS (
                SELECT variety, MAX(date) as latest_date
                FROM strawberry_readings
                GROUP BY variety
            )
            SELECT sr.*
            FROM strawberry_readings sr
            JOIN latest_dates ld 
                ON sr.variety = ld.variety 
                AND sr.date = ld.latest_date
            WHERE sr.time_of_day = 'Evening'
            ORDER BY sr.variety
            """)
            
            results = cur.fetchall()
            
            if results:
                return pd.DataFrame(results)
            else:
                return None
    except Exception as e:
        st.error(f"Error retrieving latest readings: {str(e)}")
        return None
    finally:
        conn.close()

def get_readings_for_variety(variety, start_date, end_date):
    """Get readings for a specific variety within a date range."""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
            SELECT * FROM strawberry_readings
            WHERE date BETWEEN %s AND %s
            """
            
            params = [start_date, end_date]
            
            if variety != "All":
                query += " AND variety = %s"
                params.append(variety)
                
            query += " ORDER BY date, time_of_day"
            
            cur.execute(query, params)
            results = cur.fetchall()
            
            if results:
                return pd.DataFrame(results)
            else:
                return None
    except Exception as e:
        st.error(f"Error retrieving readings for variety: {str(e)}")
        return None
    finally:
        conn.close()

def add_user_system(user_id, system_name, variety):
    """Add a new system for a user."""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO user_systems 
            (user_id, system_name, variety)
            VALUES (%s, %s, %s)
            RETURNING id
            """, (user_id, system_name, variety))
            
            system_id = cur.fetchone()[0]
            conn.commit()
            
            return system_id
    except Exception as e:
        st.error(f"Error adding user system: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_user_systems(user_id):
    """Get all systems for a user."""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
            SELECT * FROM user_systems
            WHERE user_id = %s
            ORDER BY system_name
            """, (user_id,))
            
            results = cur.fetchall()
            
            if results:
                return pd.DataFrame(results)
            else:
                return pd.DataFrame(columns=['id', 'user_id', 'system_name', 'variety', 'created_at', 'updated_at'])
    except Exception as e:
        st.error(f"Error retrieving user systems: {str(e)}")
        return None
    finally:
        conn.close()

def add_alert(user_id, system_id, alert_type, parameter, value, threshold, message):
    """Add a new alert for a user's system."""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO alerts 
            (user_id, system_id, alert_type, parameter, value, threshold, message)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """, (user_id, system_id, alert_type, parameter, value, threshold, message))
            
            alert_id = cur.fetchone()[0]
            conn.commit()
            
            return alert_id
    except Exception as e:
        st.error(f"Error adding alert: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_active_alerts(user_id, system_id=None):
    """Get active alerts for a user's system."""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
            SELECT a.*, us.system_name 
            FROM alerts a
            JOIN user_systems us ON a.system_id = us.id
            WHERE a.user_id = %s AND a.is_active = TRUE
            """
            
            params = [user_id]
            
            if system_id:
                query += " AND a.system_id = %s"
                params.append(system_id)
                
            query += " ORDER BY a.created_at DESC"
            
            cur.execute(query, params)
            results = cur.fetchall()
            
            if results:
                return pd.DataFrame(results)
            else:
                return pd.DataFrame(columns=['id', 'user_id', 'system_id', 'alert_type', 'parameter', 
                                          'value', 'threshold', 'message', 'is_active', 
                                          'created_at', 'resolved_at', 'system_name'])
    except Exception as e:
        st.error(f"Error retrieving active alerts: {str(e)}")
        return None
    finally:
        conn.close()

def resolve_alert(alert_id):
    """Mark an alert as resolved."""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE alerts
            SET is_active = FALSE, resolved_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """, (alert_id,))
            
            conn.commit()
            
            return True
    except Exception as e:
        st.error(f"Error resolving alert: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()
