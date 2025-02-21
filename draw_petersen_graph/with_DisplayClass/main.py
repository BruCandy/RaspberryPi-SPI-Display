from machine import Pin, SPI
from ili9341 import Display
import time

spi = SPI(0, baudrate=51200000, sck=Pin(18), mosi=Pin(19))
display = Display(spi, dc=Pin(22), cs=Pin(28), rst=Pin(27))
button = Pin(21, Pin.IN, Pin.PULL_DOWN)

def draw_petersen_graph(display, color):
    
    pentagon_points = [
        (120, 46), (225, 122), (185, 245), (55, 245), (15, 122)
    ]
    
    star_points = [
        (120, 90), (177,131), (155,198), (84,198), (62, 131)
    ]
    
    for i in range(5):
        x1, y1 = pentagon_points[i]
        x2, y2 = pentagon_points[(i + 1) % 5]
        display.draw_line(x1, y1, x2, y2, color)
    
    for i in range(5):
        x1, y1 = star_points[i]
        x2, y2 = star_points[(i + 2) % 5]
        display.draw_line(x1, y1, x2, y2, color)
    
    for i in range(5):
        x1, y1 = pentagon_points[i]
        x2, y2 = star_points[i]
        display.draw_line(x1, y1, x2, y2, color)


draw_petersen_graph(display, 65535)

try:
    while True:
        if button.value() == 1:
            display.clear()
            draw_petersen_graph(display, 65535)
            time.sleep(0.3)

except KeyboardInterrupt:
    print("プログラムを終了")

