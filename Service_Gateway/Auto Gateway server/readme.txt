ลำดับขั้นตอนติดตั้ง lora_pkt_fwd ให้ Autostart ด้วย systemd


สร้างไฟล์  Systemd Service ใน 
sudo nano /etc/systemd/system/



เปิดใช้งานและโหลด service
sudo systemctl daemon-reload
sudo systemctl enable lora_pkt_fwd
sudo systemctl start lora_pkt_fwd


ตรวจสอบสถานะ
systemctl status lora_pkt_fwd

ดู log แบบ realtime
journalctl -u lora_pkt_fwd -f

คำสั่งสำหรับ “หยุด” Service
sudo systemctl stop lora_pkt_fwd