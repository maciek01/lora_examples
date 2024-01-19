#!/usr/bin/python3

import time

import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


from datetime import datetime
import adafruit_rfm9x
import busio
from digitalio import DigitalInOut, Direction, Pull
import board


# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)


# First define some constants to allow easy resizing of shapes.
width = disp.width
height = disp.height
padding = -2
top = padding
bottom = height - padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 0

image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)



CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
#rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 903.9)
rfm9x.tx_power = 23

prev_packet = None

while True:

	packet = None
	# check for packet rx
	packet = rfm9x.receive(with_header=True)
	if packet is not None:
		try:
			prev_packet = packet
			packet_text = str(prev_packet, "utf-8")

			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			#print("Current Time =", current_time)

			#print(packet_text)


			# Draw a black filled box to clear the image.
			draw.rectangle((0, 0, width, height), outline=0, fill=0)

			#cmd = "hostname -I | cut -d' ' -f1"
			#IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
			#cmd = 'cut -f 1 -d " " /proc/loadavg'
			#CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")


			draw.text((x, top + 0), "IP: ", font=font, fill=255)
			draw.text((x, top + 8), "CPU load: ", font=font, fill=255)
			draw.text((x, top + 16), "LORA: " + packet_text, font=font, fill=255)
			draw.text((x, top + 25), "Time: " + current_time, font=font, fill=255)

			# Display image.
			disp.image(image)
			disp.show()

		except Exception as err:
			print(Exception, err)

	if not btnA.value:
		# Send Button A
		# Draw a black filled box to clear the image.
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		button_a_data = bytes("Button A!","utf-8")
		rfm9x.send(button_a_data)
		draw.text((x, top + 0), "Sent Button A", font=font, fill=255)
		disp.image(image)
		disp.show()

	if not btnB.value:
		# Send Button B
		# Draw a black filled box to clear the image.
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		button_b_data = bytes("Button B!","utf-8")
		rfm9x.send(button_b_data)
		draw.text((x, top + 0), "Sent Button B", font=font, fill=255)
		disp.image(image)
		disp.show()

	if not btnC.value:
		# Send Button C
		# Draw a black filled box to clear the image.
		draw.rectangle((0, 0, width, height), outline=0, fill=0)
		button_c_data = bytes("Button C!","utf-8")
		rfm9x.send(button_c_data)
		draw.text((x, top + 0), "Sent Button C", font=font, fill=255)
		disp.image(image)
		disp.show()

	time.sleep(0.5)





