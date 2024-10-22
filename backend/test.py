import sqlite3
from datetime import datetime

def add_new_field():
    conn = sqlite3.connect('audio_data.db')
    cursor = conn.cursor()
    # Add a new column 'created_at' to the existing table
    cursor.execute('''
        ALTER TABLE audio_records
        ADD COLUMN sentiment_anaylis NUMERIC
    ''')
    conn.commit()
    conn.close()

add_new_field()
print("New field added successfully!")