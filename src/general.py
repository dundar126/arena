import os
import pygame
from pygame.locals import *


# Load images with support for transparency
def load_image(name, colorkey=None):
	path = os.path.join('data')
	path = os.path.join(path, name)
	try:
		image = pygame.image.load(path)
	except:
		print('ERROR: could not locate image: ', path)
		raise SystemExit
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()


# Draw to screen with variable alpha
def blit_with_alpha(screen, image, location, opacity):
		x, y = location
		img = pygame.Surface((image.get_width(), image.get_height())).convert()
		img.blit(screen, (-x, -y))
		img.blit(image, (0, 0))
		img.set_alpha(opacity)
		screen.blit(img, location)