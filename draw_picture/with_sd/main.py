from machine import Pin, SPI
from ili9341 import Display
from SDCard import SDCard
import time, os


spi = SPI(0, baudrate=51200000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(22), cs=Pin(28), rst=Pin(27))
sd = SDCard(SPI(0), cs=Pin(26))

button = Pin(21, Pin.IN, Pin.PULL_DOWN)

os.mount(sd, "/")
os.chdir("/")
images = [f for f in os.listdir("/") if f.endswith(".raw")]
index = 0
display.draw_image(images[index], 10, 5, 220, 296)

try:
    while True:
        if button.value() == 1:  
            index = (index + 1) % len(images)  
            display.draw_image(images[index], 10, 5, 220, 296)
            time.sleep(0.3)

except KeyboardInterrupt:
    print("プログラムを終了")