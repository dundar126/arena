import pygame
from general import *


class Tile(pygame.sprite.Sprite):
	def __init__(self, rect=None, wall=False):
		# Set tile sprite (either wall or grid square)
		pygame.sprite.Sprite.__init__(self)
		self.wall = wall
		if wall:
			self.image, self.rect = load_image('wall.png', -1)
		else:
			self.image, self.rect = load_image('tile.png', -1)
		if rect is not None:
			self.rect = rect
