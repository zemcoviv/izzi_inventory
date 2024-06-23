import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id SERIAL PRIMARY KEY,
            ip VARCHAR(15),
            os VARCHAR(255),
            ports TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def save_to_db(devices):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    for device in devices:
        cur.execute("INSERT INTO devices (ip, os, ports) VALUES (%s, %s, %s)",
                    (device['ip'], device['os'], ','.join(device['ports'])))
    conn.commit()
    cur.close()
    conn.close()
