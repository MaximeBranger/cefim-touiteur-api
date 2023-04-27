import base64
import random
import qrcode
from PIL import Image 

class Avatar:
    def __init__(self, username, size):
        self.username = username
        self.size = int(size)

    def get(self):
        image = qrcode.make(self.username, border=1)

        # image = Image.new( mode = "RGB", size = (self.size, self.size) )
        # pixels = image.load()
        # for x in range(image.size[0]):
        #     for y in range(image.size[1]):
        #         pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return image
