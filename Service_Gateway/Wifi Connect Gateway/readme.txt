sudo apt update
sudo apt install network-manager

curl -L https://github.com/balena-io/wifi-connect/raw/master/scripts/raspbian-install.sh | sed 's/\*rpi/*aarch64/' | bash

mkdir -p /home/<username your pi>/Documents/wifi-config

nano ~/Documents/wifi-config/wifi-check-connect.sh

chmod +x ~/Documents/wifi-config/wifi-check-connect.sh

bash ~/Documents/wifi-config/wifi-check-connect.sh



sudo nano /etc/systemd/system/wifi-check.service


sudo systemctl daemon-reload
sudo systemctl enable wifi-check.service
sudo systemctl start wifi-check.service


sudo systemctl status wifi-check.service