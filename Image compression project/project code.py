import os
from PIL import Image

list_of_images = os.listdir()
list_of_images

l = []
for i in list_of_images:
    if ".JPG" in i.upper() or ".PNG" in i.upper() or ".JPEG" in i.upper():
        l.append(i)

l
for i in range(len(l)):
    img = Image.open(l[i])
    img.save("compressed_"+l[i],quality=50,optimize=True)

