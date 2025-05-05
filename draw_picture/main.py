from machine import Pin, SPI
from ili9341 import Display
import time


spi = SPI(0, baudrate=51200000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(22), cs=Pin(28), rst=Pin(27))

images = ["rabbit1.raw", "rabbit2.raw"]
index = 0  
button = Pin(21, Pin.IN, Pin.PULL_UP)

display.draw_image(images[index], 10, 5, 220, 296)

try:
    while True:
        if button.value() == 0:  
            index = (index + 1) % len(images)  
            display.draw_image(images[index], 10, 5, 220, 296)
            time.sleep(0.3)

except KeyboardInterrupt:
    print("プログラムを終了")