from time import sleep
from micropython import const



class Display(object):

    SWRESET = const(0x01)  # Software reset
    SLPOUT = const(0x11)  # Exit sleep mode
    DISPLAY_ON = const(0x29)  # Display on
    SET_COLUMN = const(0x2A)  # Column address set
    SET_PAGE = const(0x2B)  # Page address set
    WRITE_RAM = const(0x2C)  # Memory write
    MADCTL = const(0x36)  # Memory access control
    PIXFMT = const(0x3A)  # COLMOD: Pixel format set
    PWCTR1 = const(0xC0)  # Power control 1
    PWCTR2 = const(0xC1)  # Power control 2
    VMCTR1 = const(0xC5)  # VCOM control 1
    VMCTR2 = const(0xC7)  # VCOM control 2


    def __init__(self, spi, cs, dc, rst, width=240, height=320):

        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height

        # Initialize GPIO pins and set implementation specific methods
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)
        self.reset()

        # Send initialization commands
        self.write_cmd(self.SWRESET)  # Software reset
        sleep(.1)

        self.write_cmd(self.PWCTR1, 0x23)  # Pwr ctrl 1
        self.write_cmd(self.PWCTR2, 0x10)  # Pwr ctrl 2
        self.write_cmd(self.VMCTR1, 0x3E, 0x28)  # VCOM ctrl 1
        self.write_cmd(self.VMCTR2, 0x86)  # VCOM ctrl 2

        self.write_cmd(self.MADCTL, 0x88)  # Memory access ctrl

        self.write_cmd(self.PIXFMT, 0x55)  # COLMOD: Pixel format

        self.write_cmd(self.SLPOUT)  # Exit sleep
        sleep(.1)
        self.write_cmd(self.DISPLAY_ON)  # Display on
        sleep(.1)
        self.clear()


    # Write a block of data to display.
    def block(self, x0, y0, x1, y1, data):
        self.write_cmd(self.SET_COLUMN,
                       x0 >> 8, x0 & 0xff, x1 >> 8, x1 & 0xff)
        self.write_cmd(self.SET_PAGE,
                       y0 >> 8, y0 & 0xff, y1 >> 8, y1 & 0xff)
        self.write_cmd(self.WRITE_RAM)
        self.write_data(data)


    # Clear display.
    def clear(self, hlines=8):
        w = self.width
        h = self.height
        line = bytearray(w * 2 * hlines)
        for y in range(0, h, hlines):
            self.block(0, y, w - 1, y + hlines - 1, line)


    # Draw image from flash.
    def draw_image(self, path, x=0, y=0, w=320, h=240):
        x2 = x + w - 1
        y2 = y + h - 1
        with open(path, "rb") as f:
            chunk_height = 1024 // w
            chunk_count, remainder = divmod(h, chunk_height)
            chunk_size = chunk_height * w * 2
            chunk_y = y
            if chunk_count:
                for c in range(0, chunk_count):
                    buf = f.read(chunk_size)
                    self.block(x, chunk_y,
                               x2, chunk_y + chunk_height - 1,
                               buf)
                    chunk_y += chunk_height
            if remainder:
                buf = f.read(remainder * w * 2)
                self.block(x, chunk_y,
                           x2, chunk_y + remainder - 1,
                           buf)


    # Write command to OLED.
    def write_cmd(self, command, *args):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        # Handle any passed data
        if len(args) > 0:
            self.write_data(bytearray(args))
    

    # Write data to OLED.
    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)
    
    
    # Perform reset: Low=initialization, High=normal operation.
    def reset(self):
        self.rst(0)
        sleep(.05)
        self.rst(1)
        sleep(.05)

