

สร้างไฟล์ internet-led-status.sh
sudo nano /usr/local/bin/internet-led-status.sh

ให้สิทธิ์รันไฟล์
sudo chmod +x /usr/local/bin/internet-led-status.sh

สร้างไฟล์ systemd service
sudo nano /etc/systemd/system/internet-led.service

เปิดใช้งานและสั่งรันอัตโนมัติ
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable internet-led.service
sudo systemctl start internet-led.service


ตรวจสอบว่าไฟล์รันสำเร็จไหม
sudo systemctl status internet-led.service
หากทุกอย่างถูกต้องจะเห็นสถานะ Active: active (running)