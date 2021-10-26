'''
Given a salae logic analyzer spi file (Time [s],Packet ID,MOSI,MISO), check for 
RGB565 320x240 image. This is meant for checking from Arducam images using burst
read commands (0x3C)
'''

from matplotlib import pyplot as plt
import numpy as np
width = 320
height = 240
burstSize = 640

data = np.zeros( (width, height, 3), dtype=np.uint8)

tmppath = "" #DEFINE HERE
t = 0
b = 0
x = 0
y = 0
i = 0
file =  open(tmppath, mode ='r')
lines = file.readlines()
active = False
pixel = bytes(2)
hexbyte = bytes(1)
for line in lines:
    if (b <= 153600):
        tmp = line.split(',')
        if tmp[2] == '0x3C':
            active = True
        elif active and t < burstSize:
            tmp[3] = tmp[3].split('x')[1].rstrip()
            ti = bytes.fromhex(tmp[3])
            b+=1
            if not(b%2):
                pixel = hexbyte + ti
                i+=1
                try:
                    x = i%width
                    y = i//width
                    pix = int.from_bytes(pixel, 'big')
                    print(pixel)
                    r = ((pix >> 11) & 0x1F) * 8
                    g = ((pix >> 5) & 0x3F) * 8 
                    bl = ((pix) & 0x1F) * 8
                    data[x,y,0] = r
                    data[x,y,1] = g
                    data[x,y,2] = bl
                except Exception as e:
                    print(e)
            else:
                hexbyte = ti
        elif t >= burstSize:
            t = 0
            active = False
        line = tmp[2] + ',' + tmp[3]    
    else:
        b = 0
        i = 0
        active = False
        
plt.imshow(data)
plt.show()