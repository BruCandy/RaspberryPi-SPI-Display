from machine import Pin, SPI
import time
from square import draw_square
from ili9341_init import ili9341_init
from ili9341_clear import ili9341_clear



spi = SPI(0, baudrate=51200000, sck=Pin(18), mosi=Pin(19))
cs = Pin(28, Pin.OUT, value=1)
dc = Pin(22, Pin.OUT, value=0)
rst = Pin(27, Pin.OUT, value=1)


'''ili9341初期化'''
#reset
rst(0)
time.sleep(.05)
rst(1)
time.sleep(.05)

# Send initialization commands
ili9341_init(spi, cs, dc)

# clear
ili9341_clear(spi, cs, dc)


'''正方形を描画'''
draw_square(spi, cs, dc)

