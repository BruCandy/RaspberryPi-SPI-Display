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
        
        
    def draw_hline(self, x, y, w, color):
        line = color.to_bytes(2, 'big') * w
        self.block(x, y, x + w - 1, y, line)
    
    
    def draw_vline(self, x, y, h, color):
        line = color.to_bytes(2, 'big') * h
        self.block(x, y, x, y + h - 1, line)
        
        
    def draw_line(self, x1, y1, x2, y2, color):
        # Check for horizontal line
        if y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            self.draw_hline(x1, y1, x2 - x1 + 1, color)
            return
        # Check for vertical line
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            self.draw_vline(x1, y1, y2 - y1 + 1, color)
            return
        # Changes in x, y
        dx = x2 - x1
        dy = y2 - y1
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        # Swap start and end points if necessary
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
        # Calculate error
        error = dx >> 1
        ystep = 1 if y1 < y2 else -1
        y = y1
        for x in range(x1, x2 + 1):
            # Had to reverse HW ????
            if not is_steep:
                self.draw_pixel(x, y, color)
            else:
                self.draw_pixel(y, x, color)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
                
                
    def draw_pixel(self, x, y, color):
        self.block(x, y, x, y, color.to_bytes(2, 'big'))


    # Clear display.
    def clear(self, hlines=8):
        w = self.width
        h = self.height
        line = bytearray(w * 2 * hlines)
        for y in range(0, h, hlines):
            self.block(0, y, w - 1, y + hlines - 1, line)


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


