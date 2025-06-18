#!/bin/bash

LED_GPIO=26   #(เปลี่ยนได้ถ้าคุณใช้ GPIO อื่น)

# ฟังก์ชัน: เช็คว่ามีอินเทอร์เน็ตไหม
is_connected() {
    ping -q -c 1 -W 1 8.8.8.8 > /dev/null
    return $?
}

while true; do
    if is_connected; then
        echo "✅ Internet connected"
        sudo gpioset gpiochip0 $LED_GPIO=1
    else
        echo "❌ Internet disconnected"
        sudo gpioset gpiochip0 $LED_GPIO=0
    fi
    sleep 5  # เช็คทุก 5 วินาที
done