import sqlite3


def init_db():
    conn = sqlite3.connect('audio_data.db')
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audio_base64 TEXT NOT NULL,
            source TEXT,
            edit_source TEXT
        )
    ''')
    conn.commit()
    conn.close()


init_db()
print("exe !!")