from SimpleTextureAtlas import make_atlas
from PIL import Image
import os

def list_files(directory):
    for path in os.listdir(directory):
        path = os.path.join(directory, path)
        
        if os.path.isfile(path):
            yield path
        
        if os.path.isdir(path):
            for new_path in list_files(path):
                yield new_path

def pad(image, padding):
    size = (image.width + 2*padding, image.height + 2*padding)
    padded_image = Image.new("RGBA", size, (0,0,0,0))
    padded_image.paste(image, (padding, padding))
    return padded_image

# find paths of all files in directory
paths = list(list_files("example_images"))

# load images from paths
images = [Image.open(path) for path in paths]

# optional
if False:
    # crop images by removing zero-valued pixels
    images = [image.crop(image.getbbox()) for image in images]

# optional
if False:
    # add padding to images
    padding = 5
    images = [pad(image, padding) for image in images]
else:
    padding = 0

# make atlas from images
atlas, offsets = make_atlas(images)

# print info
for i in range(len(images)):
    x,y = offsets[i]
    image = images[i]
    
    x += padding
    y += padding
    
    print('place image "%s" of size %dx%d at (%d, %d)'
        %(paths[i], image.width, image.height, x, y))

atlas.show()
#atlas.save("atlas.png")
