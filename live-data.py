#! /usr/bin/env python3
import Adafruit_SSD1306
import psutil 
import netifaces as ni

from PIL import Image, ImageDraw, ImageFont

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
padding = -2
top = padding
bottom = height-padding
x = 0

#CPU Temp
f = open("/sys/class/thermal/thermal_zone0/temp", "r")
t = f.readline()
t = float(t)
t = round(t/1000,1)
#CPU Status
cpu = psutil.cpu_percent(interval=1)
cpu = round(cpu)
#RAM
memory = psutil.virtual_memory()
memory = memory[1]
memory = round(memory / 1024 / 1024)
#IP Address eth0
ip = ni.ifaddresses('eth0')[2][0]['addr']
# Alert Status
if t > 50:
    ALERT = "CPU TEMP ALERT"
else:
    ALERT = "NOMINAL"
draw.text((x, top),       "CPU Temp is "+str(t)+"C",  font=ImageFont.load_default(), fill=255)
draw.text((x, top+8),    "CPU usage is "+str(cpu)+"%", font=ImageFont.load_default(), fill=255)
draw.text((x, top+16),     ALERT, font=ImageFont.load_default(), fill=255)
draw.text((x, top+25),    str(memory)+"MB Free",  font=ImageFont.load_default(), fill=255)
draw.text((x, top+33),    "eth0:"+ip,  font=ImageFont.load_default(), fill=255)
disp.image(image)
disp.display()
