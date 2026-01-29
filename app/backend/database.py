"""
Script Name:  database.py
Description:  SQLite database management for application settings and profiles.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

import sqlite3
from .models import SettingsProfile

DB_PATH = "settings.db"

def get_connection() -> sqlite3.Connection:
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    """Initializes the database schema if it does not exist."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (name TEXT PRIMARY KEY, 
                  temperature REAL, 
                  max_output_tokens INTEGER, 
                  top_p REAL, 
                  top_k INTEGER, 
                  prompt_template TEXT, 
                  target_source TEXT)''')
    conn.commit()
    conn.close()

def get_all_profile_names() -> list[str]:
    """Retrieves a list of all setting profile names."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM profiles")
    profiles = [row[0] for row in c.fetchall()]
    conn.close()
    return profiles

def get_profile_by_name(name: str) -> SettingsProfile | None:
    """Retrieves a specific profile by name."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM profiles WHERE name=?", (name,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return SettingsProfile(
            name=row[0], 
            temperature=row[1], 
            max_output_tokens=row[2], 
            top_p=row[3], 
            top_k=row[4], 
            prompt_template=row[5], 
            target_source=row[6]
        )
    return None

def save_profile(profile: SettingsProfile) -> None:
    """Saves or updates a settings profile."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''INSERT OR REPLACE INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (profile.name, profile.temperature, profile.max_output_tokens, 
                   profile.top_p, profile.top_k, profile.prompt_template, profile.target_source))
        conn.commit()
    except Exception as e:
        conn.close()
        raise e
    conn.close()

def delete_profile(name: str) -> None:
    """Deletes a profile by name."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM profiles WHERE name=?", (name,))
    conn.commit()
    conn.close()
