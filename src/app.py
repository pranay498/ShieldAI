from flask import Flask, render_template, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# Store data
alerts = []
blocked_ips = []
traffic_data = []
attack_types = {"DDOS": 0, "PORT_SCAN": 0, "BRUTE_FORCE": 0, "SQL_INJECTION": 0}

@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/stats")
def get_stats():
    """Get dashboard statistics"""
    total_traffic = random.randint(1000, 5000)
    detected_attacks = len(alerts)
    blocked_ips_count = len(set(blocked_ips))
    
    return jsonify({
        "total_traffic": total_traffic,
        "detected_attacks": detected_attacks,
        "blocked_ips": blocked_ips_count,
        "ai_status": "ACTIVE",
        "threat_level": "CRITICAL" if detected_attacks > 10 else "HIGH" if detected_attacks > 5 else "MEDIUM" if detected_attacks > 0 else "LOW"
    })


@app.route("/api/alerts")
def get_alerts():
    """Get live alerts"""
    attack_type = random.choice(["DDOS", "PORT_SCAN", "BRUTE_FORCE", "SQL_INJECTION", "NORMAL"])
    
    if attack_type != "NORMAL":
        source_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        alert = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "source_ip": source_ip,
            "attack_type": attack_type,
            "ai_decision": random.choice(["BLOCKED", "ISOLATED", "MONITORED"]),
            "threat_level": random.choice(["CRITICAL", "HIGH", "MEDIUM"])
        }
        alerts.append(alert)
        blocked_ips.append(source_ip)
        attack_types[attack_type] = attack_types.get(attack_type, 0) + 1
    
    # Return last 10 alerts
    return jsonify(alerts[-10:])


@app.route("/api/threats")
def get_threats():
    """Get attack distribution"""
    return jsonify(attack_types)


@app.route("/api/chart-data")
def get_chart_data():
    """Get chart data for traffic"""
    normal_traffic = random.randint(100, 500)
    attack_traffic = random.randint(0, 100) if len(alerts) > 0 else 0
    
    return jsonify({
        "normal": normal_traffic,
        "attack": attack_traffic,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })


if __name__ == "__main__":
    app.run(debug=True, port=8001)