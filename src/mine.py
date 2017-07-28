import pygame
from general import *


class Mine(pygame.sprite.Sprite):
	def __init__(self, x, y):
		# Set mine sprite
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('mine.png', -1)
		self.damage = 25
		self.rect.x = x
		self.rect.y = y
		self.enabled = True
