import requests
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json


load_dotenv()

def fetch_events(start_time, end_time):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_time.isoformat(),
        "endtime": end_time.isoformat(),
        "minmagnitude": 1.0,
        "eventtype": "earthquake",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["features"]

def insert_events(events, cur):
    for event in events:
        cur.execute(
            "INSERT INTO raw.earthquakes_raw (raw_json) VALUES (%s)",
            (json.dumps(event),),
        )
    return len(events)

if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432"
    )
    try:
        cursor = conn.cursor()

        start_time = datetime.now() - timedelta(minutes=30)
        events = fetch_events(start_time, datetime.now())

        cnt = insert_events(events, cursor)
        conn.commit()
        print(f"Inserted: {cnt} events")
        
    finally:
        conn.close()
