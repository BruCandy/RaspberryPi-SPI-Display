'''ペテルセングラフの描画'''
SET_COLUMN = const(0x2A)  # Column address set
SET_PAGE = const(0x2B)  # Page address set
WRITE_RAM = const(0x2C)  # Memory write

pentagon_points = [
    (120, 46), (225, 122), (185, 245), (55, 245), (15, 122)
]
    
star_points = [
    (120, 90), (177,131), (155,198), (84,198), (62, 131)
]

color = 65535
def petersen_graph(spi, cs, dc):
    # 正五角形の描画
    i = 0
    while i < 5:
        x1, y1 = pentagon_points[i]
        x2, y2 = pentagon_points[(i + 1) % 5]


        # horizontal line
        if i == 2:
            x1, x2 = x2, x1
            line = color.to_bytes(2, 'big') * (x2 - x1 + 1)
 
            dc(0)
            cs(0)
            spi.write(bytearray([SET_COLUMN]))
            cs(1)

            dc(1)
            cs(0)
            spi.write(bytearray([x1 >> 8, x1 & 0xff, x2 >> 8, x2 & 0xff]))
            cs(1)


            dc(0)
            cs(0)
            spi.write(bytearray([SET_PAGE]))
            cs(1)

            dc(1)
            cs(0)
            spi.write(bytearray([y1 >> 8, y1 & 0xff, y1 >> 8, y1 & 0xff]))
            cs(1)   


            dc(0)
            cs(0)
            spi.write(bytearray([WRITE_RAM]))
            cs(1)


            dc(1)
            cs(0)
            spi.write(bytearray(line))
            cs(1)   

    

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
        x = x1
        while x <= x2:
            # Had to reverse HW ????
            if not is_steep:
                dc(0)
                cs(0)
                spi.write(bytearray([SET_COLUMN]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([x >> 8, x & 0xff, x >> 8, x & 0xff]))
                cs(1)


                dc(0)
                cs(0)
                spi.write(bytearray([SET_PAGE]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([y >> 8, y & 0xff, y >> 8, y & 0xff]))
                cs(1)   


                dc(0)
                cs(0)
                spi.write(bytearray([WRITE_RAM]))
                cs(1)


                dc(1)
                cs(0)
                spi.write(color.to_bytes(2, 'big'))
                cs(1)   


            else:
                dc(0)
                cs(0)
                spi.write(bytearray([SET_COLUMN]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([y >> 8, y & 0xff, y >> 8, y & 0xff]))
                cs(1)


                dc(0)
                cs(0)
                spi.write(bytearray([SET_PAGE]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([x >> 8, x & 0xff, x >> 8, x & 0xff]))
                cs(1)   


                dc(0)
                cs(0)
                spi.write(bytearray([WRITE_RAM]))
                cs(1)


                dc(1)
                cs(0)
                spi.write(color.to_bytes(2, 'big'))
                cs(1)   

            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

            x += 1 
    
        i += 1


    # 星の描画
    i = 0
    while i < 5:
        x1, y1 = star_points[i]
        x2, y2 = star_points[(i + 2) % 5]


        # horizontal line
        if i == 4:
            line = color.to_bytes(2, 'big') * (x2 - x1 + 1)
 
            dc(0)
            cs(0)
            spi.write(bytearray([SET_COLUMN]))
            cs(1)

            dc(1)
            cs(0)
            spi.write(bytearray([x1 >> 8, x1 & 0xff, x2 >> 8, x2 & 0xff]))
            cs(1)


            dc(0)
            cs(0)
            spi.write(bytearray([SET_PAGE]))
            cs(1)

            dc(1)
            cs(0)
            spi.write(bytearray([y1 >> 8, y1 & 0xff, y1 >> 8, y1 & 0xff]))
            cs(1)   


            dc(0)
            cs(0)
            spi.write(bytearray([WRITE_RAM]))
            cs(1)


            dc(1)
            cs(0)
            spi.write(bytearray(line))
            cs(1)   

    

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
        x = x1
        while x <= x2:
            # Had to reverse HW ????
            if not is_steep:
                dc(0)
                cs(0)
                spi.write(bytearray([SET_COLUMN]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([x >> 8, x & 0xff, x >> 8, x & 0xff]))
                cs(1)


                dc(0)
                cs(0)
                spi.write(bytearray([SET_PAGE]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([y >> 8, y & 0xff, y >> 8, y & 0xff]))
                cs(1)   


                dc(0)
                cs(0)
                spi.write(bytearray([WRITE_RAM]))
                cs(1)


                dc(1)
                cs(0)
                spi.write(color.to_bytes(2, 'big'))
                cs(1)   


            else:
                dc(0)
                cs(0)
                spi.write(bytearray([SET_COLUMN]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([y >> 8, y & 0xff, y >> 8, y & 0xff]))
                cs(1)


                dc(0)
                cs(0)
                spi.write(bytearray([SET_PAGE]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([x >> 8, x & 0xff, x >> 8, x & 0xff]))
                cs(1)   


                dc(0)
                cs(0)
                spi.write(bytearray([WRITE_RAM]))
                cs(1)


                dc(1)
                cs(0)
                spi.write(color.to_bytes(2, 'big'))
                cs(1)   

            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

            x += 1 
    

        i += 1


    # 正五角形と星の各頂点をつなげる
    i = 0
    while i < 5:
        x1, y1 = pentagon_points[i]
        x2, y2 = star_points[i]


        # vertical line
        if i == 0:
            line = color.to_bytes(2, 'big') * (y2 - y1 + 1)
 
            dc(0)
            cs(0)
            spi.write(bytearray([SET_COLUMN]))
            cs(1)

            dc(1)
            cs(0)
            spi.write(bytearray([x1 >> 8, x1 & 0xff, x1 >> 8, x1 & 0xff]))
            cs(1)


            dc(0)
            cs(0)
            spi.write(bytearray([SET_PAGE]))
            cs(1)

            dc(1)
            cs(0)
            spi.write(bytearray([y1 >> 8, y1 & 0xff, y2 >> 8, y2 & 0xff]))
            cs(1)   


            dc(0)
            cs(0)
            spi.write(bytearray([WRITE_RAM]))
            cs(1)


            dc(1)
            cs(0)
            spi.write(bytearray(line))
            cs(1)   

    

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
        x = x1
        while x <= x2:
            # Had to reverse HW ????
            if not is_steep:
                dc(0)
                cs(0)
                spi.write(bytearray([SET_COLUMN]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([x >> 8, x & 0xff, x >> 8, x & 0xff]))
                cs(1)


                dc(0)
                cs(0)
                spi.write(bytearray([SET_PAGE]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([y >> 8, y & 0xff, y >> 8, y & 0xff]))
                cs(1)   


                dc(0)
                cs(0)
                spi.write(bytearray([WRITE_RAM]))
                cs(1)


                dc(1)
                cs(0)
                spi.write(color.to_bytes(2, 'big'))
                cs(1)   


            else:
                dc(0)
                cs(0)
                spi.write(bytearray([SET_COLUMN]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([y >> 8, y & 0xff, y >> 8, y & 0xff]))
                cs(1)


                dc(0)
                cs(0)
                spi.write(bytearray([SET_PAGE]))
                cs(1)

                dc(1)
                cs(0)
                spi.write(bytearray([x >> 8, x & 0xff, x >> 8, x & 0xff]))
                cs(1)   


                dc(0)
                cs(0)
                spi.write(bytearray([WRITE_RAM]))
                cs(1)


                dc(1)
                cs(0)
                spi.write(color.to_bytes(2, 'big'))
                cs(1)   

            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

            x += 1 
    

        i += 1