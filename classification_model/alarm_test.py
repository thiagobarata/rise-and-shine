import os
import sys
import time
from datetime import datetime
from pymongo import MongoClient
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Ensure project root is in module search path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import classifier
import sleep_classifier

# Load environment variables
env_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path=env_path)
mongo_uri = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(mongo_uri)
db = client["rise-and-shine"]
alarms = db["alarm"]

# Timezone
la_tz = ZoneInfo("America/Los_Angeles")

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.connect("broker.hivemq.com", 1883)
mqtt_topic = "delgado/state"

# Returns the full alarm document
def get_alarm():
    return alarms.find_one({})

# Returns just the alarm time in ISO format
def get_alarm_time_iso():
    alarm = get_alarm()
    if alarm and "alarm_time" in alarm:
        return alarm["alarm_time"]
    return None

# Gets the current time in LA timezone
def get_current_la_time():
    return datetime.now(la_tz)

# Disables the alarm in the database
def disable_alarm():
    alarms.update_one({}, {"$set": {"enabled": False}})

# Main loop that polls the alarm and triggers classifier
def main_loop(poll_interval=3):
    print("Polling for alarm...")

    while True:
        alarm = get_alarm()

        if not alarm or not alarm.get("enabled", False):
            print("No enabled alarm found.")
        else:
            # Parse and convert time
            alarm_time_utc = datetime.fromisoformat(alarm["alarm_time"].replace("Z", "+00:00"))
            alarm_time_la = alarm_time_utc.astimezone(la_tz)
            now_la = get_current_la_time()

            print(f"Now (LA): {now_la.strftime('%Y-%m-%d %H:%M:%S')} | Alarm: {alarm_time_la.strftime('%Y-%m-%d %H:%M:%S')}")

            if now_la >= alarm_time_la:
                print("Alarm time reached. Publishing 'asleep' and starting classification...")
                mqtt_client.publish(mqtt_topic, "asleep")

                sleep_classifier.classify_from_video()

                mqtt_client.publish(mqtt_topic, "awake")
                print("Published 'awake'. Disabling alarm.")
                disable_alarm()
                print("Alarm disabled.")

        time.sleep(poll_interval)

if __name__ == "__main__":
    print("Current alarm time (ISO):", get_alarm_time_iso())
    print("Current LA time:", get_current_la_time().strftime("%Y-%m-%d %H:%M:%S"))
    main_loop()
