
Demoes:
-receiving simple lora message and dosplaying on LCD
-sending simple lora message upon a button press

hardware: Raspi Zero W, Adafruit RFM95 bonnet


Install steps:


sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install adafruit-circuitpython-ssd1306


in the current directory:

sudo cp loraRx.service /lib/systemd/system/loraRx.service
sudo chmod 644  /lib/systemd/system/loraRx.service

mkdir -p ~/bin
#cp loraRx.py ~/bin/loraRx.py
ln -s $PWD/loraRx.py ~/bin/loraRx.py


sudo systemctl daemon-reload
sudo systemctl enable loraRx.service
sudo systemctl start loraRx.service

