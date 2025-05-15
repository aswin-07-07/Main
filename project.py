import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sqlite3
import json
import time
import random
from datetime import datetime
from cryptography.fernet import Fernet

# ===== Encryption Setup =====
# Replace this with your own secure Fernet key
key = b'your-generated-key-here'
cipher = Fernet(key)

# ===== SQLite Setup =====
conn = sqlite3.connect("energy_logs.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        encrypted_data TEXT,
        timestamp TEXT
    )
""")
conn.commit()

# ===== MQTT Setup =====
broker = "broker.hivemq.com"
data_topic = "energy_system/data"
control_topic_prefix = "energy_system/control/"

# ===== Simulate Energy Data =====
def generate_energy_data():
    return {
        "device_id": "AC Unit 01",
        "voltage": round(random.uniform(210, 240), 2),
        "current": round(random.uniform(0.5, 1.0), 2),
        "power_factor": round(random.uniform(0.8, 1.0), 2),
        "timestamp": datetime.now().isoformat()
    }

# ===== Encrypt & Log Data =====
def log_data(device_id, data):
    encrypted = cipher.encrypt(json.dumps(data).encode()).decode()
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO energy_logs (device_id, encrypted_data, timestamp) VALUES (?, ?, ?)", 
                   (device_id, encrypted, timestamp))
    conn.commit()
    print(f"[LOGGED] {device_id} at {timestamp}")

# ===== Optimization Engine =====
def analyze_data(data):
    alerts = []
    if data['power_factor'] < 0.9:
        alerts.append(f"Low power factor for {data['device_id']}.")

    if data['current'] < 0.5:
        alerts.append(f"{data['device_id']} appears idle. Recommending shutdown.")
        send_control_command(data['device_id'], "turn_off")

    for alert in alerts:
        print(f"[ALERT] {alert}")

# ===== Send Control Command =====
def send_control_command(device_id, action):
    command = {"action": action}
    topic = control_topic_prefix + device_id
    publish.single(topic, json.dumps(command), hostname=broker)
    print(f"[COMMAND SENT] {device_id}: {action}")

# ===== MQTT Callbacks =====
def on_connect(client, userdata, flags, rc):
    print("[CONNECTED] Subscribed to data topic.")
    client.subscribe(data_topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        print(f"[RECEIVED] {data}")
        analyze_data(data)
        log_data(data['device_id'], data)
    except Exception as e:
        print("[ERROR]", e)

# ===== Start MQTT Listener =====
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker)
client.loop_start()

# ===== Simulate and Publish Data Every 5 Seconds =====
try:
    while True:
        energy_data = generate_energy_data()
        payload = json.dumps(energy_data)
        publish.single(data_topic, payload, hostname=broker)
        print(f"[PUBLISHED] {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n[SHUTDOWN]")
    client.loop_stop()
    conn.close()
