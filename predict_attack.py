import joblib
import random
import pandas as pd

# Load trained model
model = joblib.load("shieldai_model.pkl")

print("Model loaded successfully")

# Generate fake network traffic
sample = {
    "packet_size": random.randint(40,1500),
    "port": random.choice([21,22,25,53,80,443,8080,3306]),
    "protocol": random.choice([0,1]),  # 0 = TCP, 1 = UDP
    "request_rate": random.randint(1,1000),
    "flag_count": random.randint(0,10),
    "byte_rate": random.randint(100,10000),
    "connection_duration": random.randint(1,500),
    "src_entropy": random.uniform(0,8)
}

# Convert to dataframe
df = pd.DataFrame([sample])

# Predict
prediction = model.predict(df)

print("\nTraffic Sample:")
print(sample)

print("\nPrediction:", prediction[0])