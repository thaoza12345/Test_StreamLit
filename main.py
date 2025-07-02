import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import datetime # Import เพิ่มเติมสำหรับจัดการเวลา

st.set_page_config(layout="wide")
st.title("📍 Cyber Threat Monitoring Dashboard")

# Load data
df = pd.read_csv("data.csv")

# === TPO - Time: แปลง timestamp ให้เป็น datetime object ===
df['timestamp'] = pd.to_datetime(df['timestamp'])
# เพิ่มคอลัมน์ hour เพื่อใช้ในการวิเคราะห์ตามช่วงเวลา
df['hour'] = df['timestamp'].dt.hour
# เพิ่มคอลัมน์ date เพื่อใช้ในการวิเคราะห์ตามวัน
df['date'] = df['timestamp'].dt.date

# === Input Filters ===
st.sidebar.header("⚙️ ตัวกรองข้อมูล") # ใช้ sidebar เพื่อความเป็นระเบียบ

# Filter 1: Keyword
keyword = st.sidebar.text_input("🔎 คำค้นหา (เช่น บาคาร่า)", "")
if keyword:
    df = df[df['search_term'].str.contains(keyword, case=False, na=False)] # เพิ่ม case=False, na=False เพื่อให้ไม่คำนึงถึงตัวพิมพ์เล็กใหญ่และจัดการค่าว่าง

# Filter 2: Time Range (ช่วงเวลา)
st.sidebar.subheader("🕒 กรองตามช่วงเวลา")
start_time = st.sidebar.slider(
    "เริ่มต้นเวลา (ชั่วโมง)",
    min_value=0, max_value=23, value=0
)
end_time = st.sidebar.slider(
    "สิ้นสุดเวลา (ชั่วโมง)",
    min_value=0, max_value=23, value=23
)
df = df[(df['hour'] >= start_time) & (df['hour'] <= end_time)]

# Filter 3: Date Range (ช่วงวันที่ - ตัวอย่าง)
# ถ้ามีข้อมูลหลายวัน จะเพิ่ม Date Input ได้
# start_date = st.sidebar.date_input("วันที่เริ่มต้น", df['date'].min())
# end_date = st.sidebar.date_input("วันที่สิ้นสุด", df['date'].max())
# df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# === Visualization ===

# Map
st.subheader("🗺️ แผนที่กิจกรรมต้องสงสัย")
# ตรวจสอบว่า df ไม่ว่างเปล่าก่อนคำนวณ mean
if not df.empty:
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)
else:
    # ถ้าไม่มีข้อมูลให้แสดงแผนที่กลางๆ หรือตำแหน่งเริ่มต้นที่กำหนดเอง
    m = folium.Map(location=[6.867, 101.250], zoom_start=13)

for _, row in df.iterrows():
    # กำหนดสี Marker ตาม search_term
    marker_color = "red" if "บาคาร่า" in row['search_term'].lower() or "พนัน" in row['search_term'].lower() else "blue" # เพิ่ม 'พนัน' และทำให้เป็น lowercase เพื่อเทียบ
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"IP: {row['ip']}<br>Term: {row['search_term']}<br>Time: {row['timestamp'].strftime('%Y-%m-%d %H:%M')}",
        icon=folium.Icon(color=marker_color)
    ).add_to(m)
st_data = st_folium(m, width=900, height=450)

# Chart 1: Bar Chart (Count of IPs per search term)
st.subheader("📊 จำนวน IP ต่อคำค้นหา")
if not df.empty:
    chart = df['search_term'].value_counts().sort_index() # sort_index() เพื่อเรียงลำดับตามชื่อคำค้น
    st.bar_chart(chart)
else:
    st.write("ไม่มีข้อมูลสำหรับการค้นหา")

# Chart 2: Timeline Chart (Count of activities per hour)
st.subheader("📈 กิจกรรมตามช่วงเวลา (ต่อชั่วโมง)")
if not df.empty:
    timeline_data = df.groupby('hour').size().reset_index(name='count')
    timeline_data = timeline_data.set_index('hour').reindex(range(24), fill_value=0) # ให้ครบ 24 ชั่วโมงแม้ไม่มีข้อมูล
    st.bar_chart(timeline_data)
else:
    st.write("ไม่มีข้อมูลกิจกรรมในช่วงเวลานี้")

# Table
st.subheader("📋 รายการกิจกรรมที่ตรวจพบ")
if not df.empty:
    st.dataframe(df[['ip', 'search_term', 'latitude', 'longitude', 'timestamp']]) # เลือกคอลัมน์ที่ต้องการแสดง
else:
    st.write("ไม่มีข้อมูลที่ตรงกับเงื่อนไขการค้นหา")

print("Hello Igot")