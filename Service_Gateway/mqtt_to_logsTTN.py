import paho.mqtt.client as mqtt  
import json
from datetime import datetime
import pytz
import os

# === CONFIG ===

BROKER = "as1.cloud.thethings.industries"
PORT = 1883
USERNAME = "test2-app@mootunlesyslab"
PASSWORD = "NNSXS.CZGZQNSZOBUJYB4AGDVMCRZ26RBXMDDXPH457IY.UTHV3QNMVH5LFYSRR6HJU2OIHWNHGT3IIF3JPAZU42MSDOU6PAXA"
TOPIC_UPLINK = "v3/test2-app@mootunlesyslab/devices/+/up"
TOPIC_DOWNLINK = "v3/test2-app@mootunlesyslab/devices/+/events/down/ack"
LOG_DIR = "mqtt_logs"

os.makedirs(LOG_DIR, exist_ok=True)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        if "up" in msg.topic:
            device_id = payload["end_device_ids"]["device_id"]
            timestamp = payload["received_at"]
            timestamp_fixed = timestamp[:26] + "Z"
            dt_utc = datetime.strptime(timestamp_fixed, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
            dt_bangkok = dt_utc.astimezone(pytz.timezone("Asia/Bangkok"))
            date_str = dt_bangkok.strftime("%Y-%m-%d")

            data = {
                "device_id": device_id,
                "timestamp": dt_bangkok.isoformat(),
                "type": "uplink"
            }

            # RSSI
            try:
                rx_metadata = payload["uplink_message"].get("rx_metadata", [])
                rssi_list = []
                for meta in rx_metadata:
                    gw_id = meta.get("gateway_ids", {}).get("gateway_id", "unknown")
                    rssi = meta.get("rssi")
                    if rssi is not None:
                        rssi_list.append({"gateway_id": gw_id, "rssi": rssi})
                data["rssi_list"] = rssi_list
            except Exception as e:
                print("ไม่สามารถดึง rssi:", e)

            # Data Rate
            try:
                settings = payload["uplink_message"].get("settings", {})
                dr_info = settings.get("data_rate", {}).get("lora", {})
                if dr_info:
                    data["data_rate"] = {
                        "spreading_factor": dr_info.get("spreading_factor"),
                        "bandwidth": dr_info.get("bandwidth")
                    }
            except Exception as e:
                print("ไม่สามารถดึง data rate:", e)

            # Payload Raw (Base64)
            frm_payload = payload["uplink_message"].get("frm_payload")
            if frm_payload:
                data["frm_payload_base64"] = frm_payload

            # Decoded Payload
            decoded_payload = payload["uplink_message"].get("decoded_payload")
            if decoded_payload:
                data["decoded_payload"] = decoded_payload

        elif "down/ack" in msg.topic:
            device_id = payload["end_device_ids"]["device_id"]
            timestamp = payload["received_at"]
            timestamp_fixed = timestamp[:26] + "Z"
            dt_utc = datetime.strptime(timestamp_fixed, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
            dt_bangkok = dt_utc.astimezone(pytz.timezone("Asia/Bangkok"))
            date_str = dt_bangkok.strftime("%Y-%m-%d")

            data = {
                "device_id": device_id,
                "timestamp": dt_bangkok.isoformat(),
                "type": "downlink_ack"
            }

            # ข้อมูลเสริม
            data["info"] = payload.get("correlation_ids", [])

            # Payload Raw (Base64)
            frm_payload = payload.get("downlink_ack", {}).get("frm_payload")
            if frm_payload:
                data["frm_payload_base64"] = frm_payload

        else:
            return

        print(json.dumps(data, indent=2, ensure_ascii=False))

        filename = f"{device_id}_{date_str}.json"
        filepath = os.path.join(LOG_DIR, filename)

        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    except Exception as e:
        print("Error:", e)

# === Setup MQTT ===
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.subscribe(TOPIC_UPLINK)
client.subscribe(TOPIC_DOWNLINK)

print("Listening for MQTT messages from TTN (uplink + downlink ack)...")

client.loop_forever()
