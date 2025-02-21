from machine import Pin, SPI
import time
from petersen_graph import petersen_graph
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


'''ペテルセングラフを描画'''
petersen_graph(spi, cs, dc)


"""ボタンによる再描画"""
button = Pin(21, Pin.IN, Pin.PULL_DOWN)
try:
    while True:
        if button.value() == 1:
            # clear
            ili9341_clear(spi, cs, dc)
            # draw petersen graph
            petersen_graph(spi, cs, dc)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("プログラムを終了")