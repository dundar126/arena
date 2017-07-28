# ARENA
# By Stephen Campbell
# A turn-based duel arena game making use of A* pathfinding, neural networks and fuzzy logic

# REQUIRES
# - NumPy
# - PyGame

import os, sys
import pygame
from pygame.locals import *

# Other game files
from player import *
from tile import *
from enemy import *

if not pygame.font:
	print('Fonts disabled')
if not pygame.mixer:
	print('Sound disabled')

# Initialise PyGame
pygame.init()
pygame.font.init()

# Constants
walls = [[2, 2], [3, 2], [6, 2], [7, 2], [2, 3], [7, 3],
		[2, 6], [2, 7], [3, 7], [7, 6], [6, 7], [7, 7]]  # Wall locations
gray = pygame.Color(75, 75, 75)
red = pygame.Color(190, 75, 75)
orange = pygame.Color(190, 125, 75)
white = pygame.Color(255, 255, 255)
font = pygame.font.SysFont("arial", 24, True)
font_large = pygame.font.SysFont("arial", 36, True)
clock = pygame.time.Clock()


# Class to handle PyGame initialisation
class Main:
	def __init__(self, width=896, height=640):
		# Basic window setup
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Arena')

	# Load game data from game code files
	def load_data(self):
		# Calculate the number of tiles that can be displayed
		self.tiles_horizontal = int(self.width/64 - 4)
		self.tiles_vertical = int(self.height/64)

		# Group for tiles
		self.tile_sprites = pygame.sprite.Group()

		# Create tiles and walls
		for x in range(self.tiles_horizontal):
			for y in range(self.tiles_vertical):
				coords = [x, y]
				if coords in walls:
					self.tile_sprites.add(Tile(pygame.Rect(x*64, y*64, 64, 64), True))
				else:
					self.tile_sprites.add(Tile(pygame.Rect(x*64, y*64, 64, 64)))

		# Player setup
		self.player = Player(self.screen)
		self.player_sprites = pygame.sprite.RenderPlain(self.player)
		self.player.rect.x += 64
		self.player.rect.y += 64
		self.player.destination_x += 64
		self.player.destination_y += 64

		# Enemy setup
		self.enemy = Enemy()
		self.enemy_sprites = pygame.sprite.RenderPlain(self.enemy)
		self.enemy.move(8, 8)
		self.enemy.train_network()

	def main_loop(self):
		# Main game loop
		while 1:
			self.screen.fill((170, 165, 160))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					if (event.key == K_d) or (event.key == K_a) or (event.key == K_w) or (event.key == K_s) or (event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP) or (event.key == K_DOWN) or (event.key == K_SPACE):
						if self.player.move(event.key, walls):
							if self.enemy.enabled:
								self.enemy.next_move(self.player, walls, [self.tiles_horizontal, self.tiles_vertical])
								if self.player.check_collision(self.enemy):
									self.player.hurt(25)

			if self.player.health <= 0:
				break
			if self.enemy.health <= 0:
				break

			self.tile_sprites.draw(self.screen)

			self.player.draw_mines()
			self.enemy.draw_mines(self.screen)

			for mine in self.player.mines:
				if pygame.sprite.collide_mask(self.enemy, mine) and mine.enabled is True:
					mine.enabled = False
					self.enemy.hurt(mine.damage)

			for mine in self.enemy.mines:
				if pygame.sprite.collide_mask(self.player, mine) and mine.enabled is True:
					mine.enabled = False
					self.player.hurt(mine.damage)

			if self.enemy.health > 0:
				self.enemy_sprites.draw(self.screen)
			else:
				self.enemy.enabled = False

			self.player_sprites.draw(self.screen)
			self.draw_player_hud()
			self.draw_enemy_health()

			self.player.tween_movement_x()
			self.player.tween_movement_y()
			self.player.animate_mine()
			self.enemy.animate_mine(self.screen)
			self.enemy.animate_heal(self.screen)
			self.enemy.tween_movement_x()
			self.enemy.tween_movement_y()

			pygame.display.flip()
			clock.tick(60)
		self.game_over()

	def game_over(self):
		print("Game over!")
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						sys.exit()
					if event.key == K_SPACE:
						main_window.load_data()
						main_window.main_loop()

			self.screen.fill((0, 0, 0))
			label = font_large.render('GAME OVER', 1, white)
			label2 = font.render('Press ESC to close or SPACE for a new game.', 1, white)

			self.screen.blit(label, (self.screen.get_size()[0] / 2 - 110, self.screen.get_size()[1] / 2 - 60))
			self.screen.blit(label2, (self.screen.get_size()[0] / 2 - 250, self.screen.get_size()[1] / 2))
			pygame.display.flip()
			clock.tick(60)

	def pre_game_instructions(self):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						sys.exit()
					if event.key == K_SPACE:
						main_window.load_data()
						main_window.main_loop()

			self.screen.fill((0, 0, 0))
			label = font_large.render('ARENA', 1, white)
			label2 = font.render('GOAL: Place mines and lure the enemy into them to win.', 1, white)
			label3 = font.render('CONTROLS:', 1, white)
			label4 = font.render('Arrow keys or WASD: move', 1, white)
			label5 = font.render('Space: place mine', 1, white)
			label6 = font.render('Read the README for more information and strategy tips', 1, white)
			label7 = font.render('PRESS SPACE TO PLAY', 1, white)

			self.screen.blit(label, (self.screen.get_size()[0] / 2 - 70, self.screen.get_size()[1] / 2 - 140))
			self.screen.blit(label2, (self.screen.get_size()[0] / 2 - 320, self.screen.get_size()[1] / 2 - 90))
			self.screen.blit(label3, (self.screen.get_size()[0] / 2 - 320, self.screen.get_size()[1] / 2 - 60))
			self.screen.blit(label4, (self.screen.get_size()[0] / 2 - 320, self.screen.get_size()[1] / 2 - 30))
			self.screen.blit(label5, (self.screen.get_size()[0] / 2 - 320, self.screen.get_size()[1] / 2))
			self.screen.blit(label6, (self.screen.get_size()[0] / 2 - 320, self.screen.get_size()[1] / 2 + 30))
			self.screen.blit(label7, (self.screen.get_size()[0] / 2 - 140, self.screen.get_size()[1] / 2 + 90))
			pygame.display.flip()
			clock.tick(60)

	# Draw player health bar, mines left and player label
	def draw_player_hud(self):
		bar_height = 25
		bar_width = 235
		padding = 4
		x = self.screen.get_size()[0] - bar_width - 10

		label = font.render('PLAYER', 1, gray)
		self.screen.blit(label, (x, 2))
		health_width = int(max(min(self.player.health / float(self.player.maxhealth) * (bar_width - padding * 2), (bar_width - padding * 2)), 0))
		pygame.draw.rect(self.screen, gray, (x, 30, bar_width, bar_height))
		pygame.draw.rect(self.screen, red, (x + padding, 30 + padding, health_width, bar_height - padding * 2))
		label = font.render('{}/{} mines'.format(self.player.minesleft, self.player.maxmines), 1, gray)
		self.screen.blit(label, (x, 55))

	# Draw enemy health bar, heals left and enemy label
	def draw_enemy_health(self):
		if self.enemy.health > 0:
			y_offset = self.screen.get_size()[1] - 90
			bar_height = 25
			bar_width = 235
			x = self.screen.get_size()[0] - bar_width - 10

			label = font.render('ENEMY', 1, gray)
			label2 = font.render('{} heal left'.format(self.enemy.heals_left), 1, gray)
			self.screen.blit(label, (x, y_offset + 2))
			self.screen.blit(label2, (x, y_offset + 56))
			padding = 4

			health_width = int(max(min(self.enemy.health / float(self.enemy.maxhealth) * (bar_width - padding * 2), (bar_width - padding * 2)), 0))
			pygame.draw.rect(self.screen, gray, (x, y_offset + 30, bar_width, bar_height))
			pygame.draw.rect(self.screen, orange, (x + padding, y_offset + 30 + padding, health_width, bar_height - padding * 2))

# Open game window
if __name__ == "__main__":
	main_window = Main()
	main_window.load_data()
	main_window.pre_game_instructions()
	main_window.main_loop()
