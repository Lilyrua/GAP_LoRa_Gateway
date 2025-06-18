sudo nano /etc/systemd/system/pi-boot-led.service


sudo systemctl daemon-reload
sudo systemctl restart pi-boot-led.service
sudo systemctl enable pi-boot-led.service