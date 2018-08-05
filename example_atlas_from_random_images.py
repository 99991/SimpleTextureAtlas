from SimpleTextureAtlas import make_atlas
from PIL import Image
import random

# In this example, random images are created and packed into an atlas.

def make_images(n_images):
    images = []

    for _ in range(n_images):
        # random color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        # random size
        height = random.randint(20, 50)
        width = random.randint(20, 50)
        
        # image of random size and color
        image = Image.new('RGB', (width, height), (r, g, b))
        
        images.append(image)

    return images

# make random images
images = make_images(500)

# pack them into atlas
atlas, offsets = make_atlas(images)

# print info
for i in range(len(images)):
    x,y = offsets[i]
    image = images[i]
    
    print("place image %d of size %dx%d at (%d, %d)"
        %(i, image.width, image.height, x, y))

atlas.show()
