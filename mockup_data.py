import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def generate_thai_coordinates():
    # Approximate bounds for Thailand
    # Latitude: 5.6 to 20.4 degrees North
    # Longitude: 97.3 to 105.6 degrees East
    lat = round(random.uniform(5.6, 20.4), 3)
    lon = round(random.uniform(97.3, 105.6), 3)
    return lat, lon

def generate_search_term():
    common_terms = ["youtube", "facebook", "google", "weather", "news", "food delivery", "travel", "online shopping"]
    gambling_terms = ["บาคาร่า", "สล็อต", "แทงบอล", "หวยออนไลน์", "คาสิโน", "เว็บพนัน"]

    # 20% chance for gambling term, 80% for common term
    if random.random() < 0.20:
        return random.choice(gambling_terms)
    else:
        return random.choice(common_terms)

def generate_timestamp(start_date, end_date):
    time_diff = end_date - start_date
    random_seconds = random.randint(0, int(time_diff.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

# --- Configuration ---
num_records = 5000 # จำนวน IP records ที่ต้องการ
start_date = datetime(2025, 6, 1, 0, 0, 0)
end_date = datetime(2025, 6, 10, 23, 59, 59)
output_filename = "data.csv"

# --- Generate Data ---
data = []
for _ in range(num_records):
    ip = generate_random_ip()
    lat, lon = generate_thai_coordinates()
    term = generate_search_term()
    timestamp = generate_timestamp(start_date, end_date)
    data.append([ip, lat, lon, term, timestamp])

df = pd.DataFrame(data, columns=['ip', 'latitude', 'longitude', 'search_term', 'timestamp'])

# --- Add some clustered gambling activity (e.g., in a specific area in the South, like Pattani/Yala/Narathiwat region) ---
# (Approximate center for Pattani/Yala/Narathiwat region)
center_lat_south = 6.8
center_lon_south = 101.2
num_south_gambling_ips = 50 # จำนวน IP ที่สุ่มให้มาอยู่ภาคใต้และเป็นเว็บพนัน

for _ in range(num_south_gambling_ips):
    ip = generate_random_ip()
    lat = round(random.uniform(center_lat_south - 0.1, center_lat_south + 0.1), 3) # สุ่ม Lat รอบๆ จุดศูนย์กลาง
    lon = round(random.uniform(center_lon_south - 0.1, center_lon_south + 0.1), 3) # สุ่ม Lon รอบๆ จุดศูนย์กลาง
    term = random.choice(["บาคาร่า", "สล็อต", "แทงบอล", "หวยออนไลน์"])
    timestamp = generate_timestamp(start_date, end_date) # สามารถจำกัดช่วงเวลาให้เป็นกลางคืนได้ด้วย
    data.append([ip, lat, lon, term, timestamp])

# Recreate DataFrame with combined data
df_combined = pd.DataFrame(data, columns=['ip', 'latitude', 'longitude', 'search_term', 'timestamp'])

# Ensure all timestamps are formatted correctly for CSV
df_combined['timestamp'] = df_combined['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

df_combined.to_csv(output_filename, index=False)

print(f"Generated {len(df_combined)} records to {output_filename}")