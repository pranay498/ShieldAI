import random
import pandas as pd

rows = []

for i in range(10000):

    # 80% normal traffic
    if random.random() < 0.6:
        sample = {
            "packet_size": random.randint(40,800),
            "port": random.choice([80,443]),
            "protocol": random.choice([0,1]),
            "request_rate": random.randint(1,100),
            "flag_count": random.randint(0,3),
            "byte_rate": random.randint(100,2000),
            "connection_duration": random.randint(50,500),
            "src_entropy": random.uniform(1,4),
            "label": "NORMAL"
        }

    # 20% attack traffic
    else:
        attack = random.choice(["DDOS","PORT_SCAN","BRUTE_FORCE"])

        if attack == "DDOS":
            sample = {
                "packet_size": random.randint(1200,1500),
                "port": 80,
                "protocol": 0,
                "request_rate": random.randint(800,1000),
                "flag_count": random.randint(6,10),
                "byte_rate": random.randint(7000,10000),
                "connection_duration": random.randint(1,20),
                "src_entropy": random.uniform(6,8),
                "label": "DDOS"
            }

        elif attack == "PORT_SCAN":
            sample = {
                "packet_size": random.randint(900,1200),
                "port": random.randint(20,1024),
                "protocol": 0,
                "request_rate": random.randint(500,800),
                "flag_count": random.randint(5,9),
                "byte_rate": random.randint(4000,8000),
                "connection_duration": random.randint(10,40),
                "src_entropy": random.uniform(5,7),
                "label": "PORT_SCAN"
            }

        else:
            sample = {
                "packet_size": random.randint(700,1200),
                "port": 22,
                "protocol": 0,
                "request_rate": random.randint(400,900),
                "flag_count": random.randint(5,10),
                "byte_rate": random.randint(3000,9000),
                "connection_duration": random.randint(5,30),
                "src_entropy": random.uniform(5,8),
                "label": "BRUTE_FORCE"
            }

    rows.append(sample)

df = pd.DataFrame(rows)

df.to_csv("synthetic_network_intrusion_data.csv", index=False)

print("Dataset generated successfully")
print("Rows:", len(df))