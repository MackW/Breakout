import os
import pygame
from pygame.locals import RLEACCEL
    
def load_image(name, colorkey=None):
    fullname = os.path.join('', 'Images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image 

def get_colorkey_hitmask(image, rect):
    colorkey=image.get_colorkey()
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x,y)) == colorkey)
    return mask

def check_collision(obj1,obj2):
    try:rect1, rect2, hm1, hm2 = obj1.rect, obj2.rect, obj1.hitmask, obj2.hitmask
    except AttributeError:return False
    rect=rect1.clip(rect2)
    if rect.width==0 or rect.height==0:
        return False
    x1,y1,x2,y2 = rect.x-rect1.x,rect.y-rect1.y,rect.x-rect2.x,rect.y-rect2.y
    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hm1[x1+x][y1+y] and hm2[x2+x][y2+y]:return True
            else:continue
    return False

