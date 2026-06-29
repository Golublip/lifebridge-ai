import sqlite3
import json
from typing import List, Dict, Any
from datetime import datetime
from app.models.database import get_db_connection

class ShortTermMemory:
    """
    Manages session-level details, active planning state, and temporary tool outputs
    """
    def __init__(self, session_id: str = "default_session"):
        self.session_id = session_id

    def add_message(self, role: str, message: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO chats (session_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
        """, (self.session_id, role, message, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def get_chat_history(self, limit: int = 15) -> List[Dict[str, str]]:
        conn = get_db_connection()
        rows = conn.execute("""
        SELECT role, message, timestamp FROM chats
        WHERE session_id = ?
        ORDER BY id DESC LIMIT ?
        """, (self.session_id, limit)).fetchall()
        conn.close()
        
        # Reverse to get chronological order
        history = [{"role": r["role"], "content": r["message"]} for r in reversed(rows)]
        return history

    def clear_session(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM chats WHERE session_id = ?", (self.session_id,))
        conn.commit()
        conn.close()
