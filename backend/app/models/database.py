import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "lifebridge.db"))

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create User Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        location TEXT,
        allergies TEXT, -- JSON array
        medications TEXT, -- JSON array
        family_history TEXT, -- JSON array
        chronic_conditions TEXT, -- JSON array
        preferences TEXT -- JSON object
    )
    """)
    
    # Create Medications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dosage TEXT,
        frequency TEXT,
        reminders TEXT, -- JSON array of strings: ["08:00", "20:00"]
        compliance REAL DEFAULT 100.0
    )
    """)
    
    # Create Medication Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medication_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medication_id INTEGER,
        taken_at TEXT,
        status TEXT, -- Taken, Missed
        FOREIGN KEY (medication_id) REFERENCES medications (id)
    )
    """)
    
    # Create Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name TEXT,
        hospital_name TEXT,
        date_time TEXT,
        purpose TEXT,
        status TEXT DEFAULT 'Scheduled'
    )
    """)
    
    # Create Health Records Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        file_type TEXT,
        summary TEXT,
        upload_time TEXT,
        parsed_parameters TEXT -- JSON string
    )
    """)

    # Create Chats Table for short-term memory / session logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT, -- user, assistant, system
        message TEXT,
        timestamp TEXT
    )
    """)

    # Insert default user if not exists
    cursor.execute("SELECT user_id FROM users WHERE user_id = 'default_user'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (user_id, name, age, gender, location, allergies, medications, family_history, chronic_conditions, preferences)
        VALUES (
            'default_user', 'John Doe', 65, 'Male', 'Rural Ohio',
            '["Penicillin"]', '["Metformin", "Lisinopril"]', '["Type 2 Diabetes", "Hypertension"]', '["Type 2 Diabetes", "Chronic Hypertension"]',
            '{"language": "English", "favorite_hospitals": ["Mercy Health Clinic", "County General Hospital"]}'
        )
        """)
        # Insert some sample medications for John Doe
        cursor.execute("""
        INSERT INTO medications (name, dosage, frequency, reminders, compliance)
        VALUES ('Metformin', '500mg', 'Twice daily', '["08:00", "20:00"]', 85.0)
        """)
        cursor.execute("""
        INSERT INTO medications (name, dosage, frequency, reminders, compliance)
        VALUES ('Lisinopril', '10mg', 'Once daily', '["08:00"]', 92.0)
        """)
        # Insert some sample appointments
        cursor.execute("""
        INSERT INTO appointments (doctor_name, hospital_name, date_time, purpose)
        VALUES ('Dr. Sarah Jenkins', 'Mercy Health Clinic', '2026-07-15 10:00:00', 'Diabetes Follow-up')
        """)
    
    conn.commit()
    conn.close()

# Helper Functions for database manipulation
def get_user_profile(user_id: str = "default_user") -> Dict[str, Any]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return {}
    profile = dict(row)
    profile['allergies'] = json.loads(profile['allergies'] or '[]')
    profile['medications'] = json.loads(profile['medications'] or '[]')
    profile['family_history'] = json.loads(profile['family_history'] or '[]')
    profile['chronic_conditions'] = json.loads(profile['chronic_conditions'] or '[]')
    profile['preferences'] = json.loads(profile['preferences'] or '{"language": "English", "favorite_hospitals": []}')
    return profile

def update_user_profile(profile_data: Dict[str, Any], user_id: str = "default_user"):
    conn = get_db_connection()
    conn.execute("""
    UPDATE users SET
        name = ?, age = ?, gender = ?, location = ?,
        allergies = ?, medications = ?, family_history = ?, chronic_conditions = ?,
        preferences = ?
    WHERE user_id = ?
    """, (
        profile_data.get('name', 'John Doe'),
        profile_data.get('age'),
        profile_data.get('gender'),
        profile_data.get('location'),
        json.dumps(profile_data.get('allergies', [])),
        json.dumps(profile_data.get('medications', [])),
        json.dumps(profile_data.get('family_history', [])),
        json.dumps(profile_data.get('chronic_conditions', [])),
        json.dumps(profile_data.get('preferences', {"language": "English", "favorite_hospitals": []})),
        user_id
    ))
    conn.commit()
    conn.close()

def get_medications() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM medications").fetchall()
    conn.close()
    result = []
    for r in rows:
        m = dict(r)
        m['reminders'] = json.loads(m['reminders'] or '[]')
        result.append(m)
    return result

def add_medication(med: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO medications (name, dosage, frequency, reminders, compliance)
    VALUES (?, ?, ?, ?, ?)
    """, (
        med['name'],
        med['dosage'],
        med['frequency'],
        json.dumps(med.get('reminders', [])),
        med.get('compliance', 100.0)
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def log_medication(med_id: int, status: str, taken_at: str = None):
    conn = get_db_connection()
    if not taken_at:
        taken_at = datetime.now().isoformat()
    conn.execute("""
    INSERT INTO medication_logs (medication_id, taken_at, status)
    VALUES (?, ?, ?)
    """, (med_id, taken_at, status))
    # Update compliance score
    logs = conn.execute("SELECT status FROM medication_logs WHERE medication_id = ?", (med_id,)).fetchall()
    taken = sum(1 for log in logs if log['status'] == 'Taken')
    total = len(logs)
    compliance = (taken / total) * 100.0 if total > 0 else 100.0
    conn.execute("UPDATE medications SET compliance = ? WHERE id = ?", (compliance, med_id))
    conn.commit()
    conn.close()

def get_appointments() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM appointments ORDER BY date_time ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_appointment(app: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO appointments (doctor_name, hospital_name, date_time, purpose, status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        app['doctor_name'],
        app['hospital_name'],
        app['date_time'],
        app['purpose'],
        app.get('status', 'Scheduled')
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def delete_medication(med_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM medications WHERE id = ?", (med_id,))
    conn.execute("DELETE FROM medication_logs WHERE medication_id = ?", (med_id,))
    conn.commit()
    conn.close()

def get_health_records() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM health_records ORDER BY id DESC").fetchall()
    conn.close()
    result = []
    for r in rows:
        rec = dict(r)
        rec['parsed_parameters'] = json.loads(rec['parsed_parameters'] or '{}')
        result.append(rec)
    return result

def add_health_record(rec: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO health_records (file_name, file_type, summary, upload_time, parsed_parameters)
    VALUES (?, ?, ?, ?, ?)
    """, (
        rec['file_name'],
        rec['file_type'],
        rec['summary'],
        rec['upload_time'],
        json.dumps(rec.get('parsed_parameters', {}))
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id
