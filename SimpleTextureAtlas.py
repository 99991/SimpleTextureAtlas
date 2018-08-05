from PIL import Image

def pack_images(images, atlas_width, atlas_height):
    # idea based on http://blackpawn.com/texts/lightmaps/
    
    def rect_area(rect):
        x,y,w,h = rect
        
        return w*h

    def image_area(image_index):
        image = images[image_index]
        
        return image.width*image.height
    
    # Packing works better if we start with large images,
    # therefore images are sorted by area.
    image_indices = sorted(range(len(images)), key=image_area, reverse=True)

    # empty rectangles in which images should be placed
    empty_rects = set([(0, 0, atlas_width, atlas_height)])
    
    # final image positions in atlas
    offsets = [None]*len(images)

    for image_index in image_indices:
        image = images[image_index]
        
        width  = image.width
        height = image.height
        
        def cost(rect):
            x,y,w,h = rect
            
            # if image does not fit in rect
            if w < width or h < height:
                return float("inf")
            
            # prefer rects with smaller area
            return w*h
        
        # find best fitting rectangle for image
        rect = min(empty_rects, key=cost)
        
        # the atlas is full if no rectangle is a good fit
        if cost(rect) == float("inf"):
            raise Exception("Atlas full")
        
        empty_rects.remove(rect)
        
        x,y,w,h = rect
        
        # either split rectangle horizontally
        top = (x, y + height, w, h - height)
        bot = (x + width, y, w - width, height)
        # or vertically
        left = (x, y + height, width, h - height)
        right = (x + width, y, w - width, h)
        
        assert(top[0] + top[2] <= atlas_width)
        assert(top[1] + top[3] <= atlas_height)
        assert(bot[0] + bot[2] <= atlas_width)
        assert(bot[1] + bot[3] <= atlas_height)
        assert(rect_area(top) + rect_area(bot) + width*height == w*h)
        
        assert(left[0] + left[2] <= atlas_width)
        assert(left[1] + left[3] <= atlas_height)
        assert(right[0] + right[2] <= atlas_width)
        assert(right[1] + right[3] <= atlas_height)
        assert(rect_area(left) + rect_area(right) + width*height == w*h)
        
        # keep the split with the larger rectangle
        if max(rect_area(top), rect_area(bot)) > max(rect_area(left), rect_area(right)):
            empty_rects.add(top)
            empty_rects.add(bot)
        else:
            empty_rects.add(left)
            empty_rects.add(right)
        
        offsets[image_index] = (x, y)
    
    return offsets

def make_atlas(
    images,
    atlas_width=1,
    atlas_height=1,
    background_color=(0,0,0,0)
):
    # While images don't fit into atlas, increase atlas size.
    while True:
        try:
            offsets = pack_images(images, atlas_width, atlas_height)
            break
        except Exception:
            if atlas_width <= atlas_height:
                atlas_width *= 2
            else:
                atlas_height *= 2

    atlas = Image.new('RGBA', (atlas_width, atlas_height), background_color)

    for (x, y), image in zip(offsets, images):
        atlas.paste(image, (x, y))

    return atlas, offsets
