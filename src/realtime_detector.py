import joblib
import random
import pandas as pd
import time
from rl_agent import choose_action, update_q_table, get_reward

# Load trained model
model = joblib.load("shieldai_model.pkl")

print("ShieldAI Real-Time Detector Started...\n")

while True:

    # 80% normal traffic
    if random.random() < 0.8:
        sample = {
            "packet_size": random.randint(40, 800),
            "port": random.choice([80, 443]),
            "protocol": random.choice([0, 1]),  # 0 = TCP, 1 = UDP
            "request_rate": random.randint(1, 100),
            "flag_count": random.randint(0, 3),
            "byte_rate": random.randint(100, 2000),
            "connection_duration": random.randint(50, 500),
            "src_entropy": random.uniform(1, 4)
        }

    # 20% simulated attack traffic
    else:
        attack_type = random.choice(["DDOS", "PORT_SCAN", "BRUTE_FORCE"])

        if attack_type == "DDOS":
            sample = {
                "packet_size": random.randint(1200, 1500),
                "port": 80,
                "protocol": 0,
                "request_rate": random.randint(800, 1000),
                "flag_count": random.randint(6, 10),
                "byte_rate": random.randint(7000, 10000),
                "connection_duration": random.randint(1, 20),
                "src_entropy": random.uniform(6, 8)
            }

        elif attack_type == "PORT_SCAN":
            sample = {
                "packet_size": random.randint(900, 1200),
                "port": random.randint(20, 1024),
                "protocol": 0,
                "request_rate": random.randint(500, 800),
                "flag_count": random.randint(5, 9),
                "byte_rate": random.randint(4000, 8000),
                "connection_duration": random.randint(10, 40),
                "src_entropy": random.uniform(5, 7)
            }

        else:  # BRUTE_FORCE
            sample = {
                "packet_size": random.randint(700, 1200),
                "port": 22,
                "protocol": 0,
                "request_rate": random.randint(400, 900),
                "flag_count": random.randint(5, 10),
                "byte_rate": random.randint(3000, 9000),
                "connection_duration": random.randint(5, 30),
                "src_entropy": random.uniform(5, 8)
            }

    # Convert to dataframe
    df = pd.DataFrame([sample])

    # Predict attack
    prediction = model.predict(df)[0]

    # Determine threat level
    if prediction == "NORMAL":
        threat = "LOW"
    elif prediction == "PORT_SCAN":
        threat = "MEDIUM"
    elif prediction == "BRUTE_FORCE":
        threat = "HIGH"
    else:
        threat = "CRITICAL"

    # RL agent chooses action
    action, state_index, action_index = choose_action(threat)

    # get reward
    reward = get_reward(action, threat)

    # update Q-table
    update_q_table(state_index, action_index, reward)

    print(f"[ALERT] {prediction} detected → Action: {action}")

    time.sleep(2)