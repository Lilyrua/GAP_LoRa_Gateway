#!/bin/bash

TARGET_SSID="<WIFI_NAME>"
WIFI_PASS="<WIFI_PASS>"
HOTSPOT_NAME="Gateway-WiFi"
WIFI_CONNECT_PATH="/usr/local/sbin/wifi-connect"

# ตรวจสอบว่าเชื่อม WiFi แล้วหรือยัง
SSID_NOW=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2 || true)
if [ "$SSID_NOW" != "$TARGET_SSID" ]; then
    echo "📡 Trying to connect to $TARGET_SSID..."
    nmcli dev wifi connect "$TARGET_SSID" password "$WIFI_PASS"
fi

# รอเช็คสถานะการเชื่อมต่อ
for i in {1..5}; do
    SSID=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2 || true)
    if [ "$SSID" == "$TARGET_SSID" ]; then
        echo "✅ Connected to $SSID"
        exit 0
    fi
    echo "⏳ Waiting for WiFi connection ($i/5)..."
    sleep 3
done

# ถ้าเชื่อมไม่สำเร็จ → เปิด Hotspot
echo "⚠️ Failed to connect to $TARGET_SSID. Starting hotspot: $HOTSPOT_NAME..."
sleep 2
sudo "$WIFI_CONNECT_PATH" --portal-ssid "$HOTSPOT_NAME"
