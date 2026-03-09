from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        # Add a 20px padding
        p = 20
        bbox = (max(0, bbox[0]-p), max(0, bbox[1]-p), min(im.size[0], bbox[2]+p), min(im.size[1], bbox[3]+p))
        return im.crop(bbox)
    return im

im = Image.open('assets/rag-original.png')
trimmed = trim(im)
trimmed.save('test_trimmed.png')
print("Saved testing trim")
