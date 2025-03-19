import streamlit as st
import pandas as pd
import os
import csv
import datetime

MOOD_FILE = "mood_log.csv"

def load_mood_data():
    if not os.path.exists(MOOD_FILE):
        return pd.DataFrame(columns=["Date", "Mood"])
    
    # Check if the CSV file has the correct header
    with open(MOOD_FILE, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # Read the first line
        
    if header == ["Date", "Mood"]:
        df = pd.read_csv(MOOD_FILE)
    else:
        # Read data without header and assign column names
        df = pd.read_csv(MOOD_FILE, header=None, names=["Date", "Mood"])
    
    return df

def save_mood_data(date, mood):
    file_exists = os.path.exists(MOOD_FILE)
    with open(MOOD_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Mood"])  # Write header if file is new
        writer.writerow([date, mood])

today_date = datetime.date.today()

st.subheader("How are you feeling Today")
mood = st.selectbox("Select Your Mood", ["Happy", "Sad", "Angry", "Neutral"])

if st.button("Log Mood"):
    save_mood_data(today_date, mood)
    st.success("Mood Logged Successfully!")

data = load_mood_data()

if not data.empty:
    st.subheader("Mood Trends Over Time")
    data["Date"] = pd.to_datetime(data["Date"])
    mood_count = data.groupby("Mood").count()["Date"]
    st.bar_chart(mood_count)