from flask import Flask, render_template
import os
from scan import run_masscan, run_nmap
from parse import parse_masscan_output, parse_nmap_output
from db import create_db, save_to_db
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

app = Flask(__name__)

@app.route('/')
def index():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT * FROM devices")
    devices = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', devices=devices)

@app.route('/scan')
def scan():
    # Настройка путей к файлам
    masscan_output = 'masscan_output.xml'
    nmap_output = 'nmap_output.xml'

    # Сканирование сети
    run_masscan('10.0.0.0/8', masscan_output)
    devices = parse_masscan_output(masscan_output)
    
    with open('masscan_ips.txt', 'w') as f:
        for device in devices:
            f.write(device['ip'] + '\n')
    
    run_nmap('masscan_ips.txt', nmap_output)
    detailed_devices = parse_nmap_output(nmap_output)
    
    # Сохранение данных в базу
    save_to_db(detailed_devices)
    
    return 'Сканирование завершено!'

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
