import pygame
from general import *
import numpy as np
from astar import *
from neural import *
from random import random
from enemy_mine import *
from fuzzy import *


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		# Set Enemy sprite
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('enemy.png', -1)

		# Enemy setup
		self.x_speed = 64
		self.y_speed = 64
		self.health = 100
		self.maxhealth = 100
		self.enabled = True
		self.nn = NeuralNetwork()
		self.mines = []
		self.mine_sprites = []
		self.heals_left = 1
		self.FOLLOW_PLAYER = 1
		self.HEAL = 2
		self.DROP_MINE = 3
		self.destination_x = self.rect.x
		self.destination_y = self.rect.y
		self.placing_mine = False
		self.mine_text_y = 0
		self.heal_text_y = 0
		self.healing = False

	# Immediately move enemy to set location (used for initial placement)
	def move(self, x, y):
		self.rect.move_ip(x * self.x_speed, y * self.y_speed)
		self.destination_x = self.rect.x
		self.destination_y = self.rect.y

	# Train neural network by iteratively adjusting the weights to minimise cost
	def train_network(self):
		# Data in: (player health, player mines)
		# Data out: (charge chance)
		data_in = np.array(([1, 1], [0.75, 0.75], [0.5, 0.5], [0.25, 0.25]), dtype=float)
		data_out = np.array(([40], [60], [80], [100]), dtype=float)

		data_out /= 100  # Bounds are 100 as chance is expressed as a percentage

		self.nn.forward(data_in)

		num_tests = 100
		step = 3
		for i in range(0, num_tests):
			# Calculate gradient of cost (so we can move down the gradient)
			dcost_dweight1, dcost_dweight2 = self.nn.delta_cost(data_in, data_out)
			self.nn.weight1 -= step * dcost_dweight1  # Move down weight 1
			self.nn.weight2 -= step * dcost_dweight2  # Move down weight 2

		self.nn.forward(data_in)

	# Calculate next move using neural network and fuzzy logic
	def next_move(self, player, walls, grid):
		rand = random()

		# Neural network
		data_in = [player.health / 100, player.minesleft / player.maxmines]
		values = self.nn.forward(data_in)
		result = np.round(values, 3)

		# Fuzzy logic
		ran = self.calculate_distance(player, walls, grid)
		hea = self.health
		threat = logic_system(ran, hea)
		if threat == 'high' and self.heals_left > 0:
			move = self.HEAL
		elif rand * result > 0.15:
			move = self.FOLLOW_PLAYER
		else:
			move = self.DROP_MINE

		if move == self.FOLLOW_PLAYER:
			# Move towards player
			self.calculate_movement(player, walls, grid)
		elif move == self.HEAL:
			# Heal

			self.heal(50)
		elif move == self.DROP_MINE:
			self.attack()

	# A* pathfinding function
	def calculate_movement(self, player, walls, grid):
		destination_x = 0
		destination_y = 0

		if not(self.rect.x == player.rect.x and self.rect.y == player.rect.y):
			# Initialise an empty grid of game dimensions
			g = np.zeros([grid[0], grid[1]])
			x = 0 # Column counter
			for col in g:
				y = 0 # Row counter
				for row in col:
					if [x, y] in walls:
						g[x][y] = 1 # Mark grid square as a wall if the location is in the walls array
					y += 1
				x += 1

			# Call A* function - find_path(grid, (source_x, source_y), (destination_x, destination_y))
			route = find_path(g, (int(self.rect.x / 64), int(self.rect.y / 64)), (int(player.rect.x / 64), int(player.rect.y / 64)))

			# Translate route coordinates to grid squares
			destination_x += route[-1][0] * self.x_speed
			destination_y += route[-1][1] * self.y_speed
			if destination_x > self.rect.x:
				print('Enemy moves right.')
			elif destination_x < self.rect.x:
				print('Enemy moves left.')
			elif destination_y > self.rect.y:
				print('Enemy moves down.')
			elif destination_y < self.rect.y:
				print('Enemy moves up.')
			self.destination_x = destination_x
			self.destination_y = destination_y

	# Animate movement along the X axis
	def tween_movement_x(self):
		if self.destination_x != self.rect.x:
			if self.destination_x < self.rect.x:
				self.rect.x -= 8
			else:
				self.rect.x += 8

	# Animate movement along the Y axis
	def tween_movement_y(self):
		if self.destination_y != self.rect.y:
			if self.destination_y < self.rect.y:
				self.rect.y -= 8
			else:
				self.rect.y += 8

	# Calculate distance between enemy and player
	def calculate_distance(self, player, walls, grid):
		if not (self.rect.x == player.rect.x and self.rect.y == player.rect.y):
			# Initialise an empty grid of game dimensions
			g = np.zeros([grid[0], grid[1]])
			x = 0  # Column counter
			for col in g:
				y = 0  # Row counter
				for row in col:
					if [x, y] in walls:
						g[x][y] = 1  # Mark grid square as a wall if the location is in the walls array
					y += 1
				x += 1

			# Call A* function - find_path(grid, (source_x, source_y), (destination_x, destination_y))
			route = find_path(g, (int(self.rect.x / 64), int(self.rect.y / 64)), (int(player.rect.x / 64), int(player.rect.y / 64)))

			# Return length of route to player
			return len(route)
		else:
			return 0

	# Damage enemy
	def hurt(self, amount):
		self.health = self.health - amount
		print('Enemy takes {} damage. {} health remaining.'.format(amount, self.health))

	# Heal enemy
	def heal(self, amount):
		print('Enemy heals.')
		self.heals_left -= 1
		self.healing = True
		if self.health + amount < self.maxhealth:
			self.health = self.health + amount
		else:
			self.health = self.maxhealth

	# Drop mine
	def attack(self):
		mine_on_square = False
		for mine in self.mines:
			if mine.rect.x == self.rect.x and mine.rect.y == self.rect.y and mine.enabled is True:
				mine_on_square = True
		if not mine_on_square:
			print('Enemy places a mine.')
			m = EnemyMine(self.rect.x, self.rect.y)
			self.placing_mine = True
			self.mines.append(m)
			self.mine_sprites.append(pygame.sprite.RenderPlain(m))
			return True
		else:
			print('Enemy tries to place a mine, but there is already a mine there.')
			return False

	# Draw mine sprites to screen
	def draw_mines(self, screen):
		for index, mine in enumerate(self.mines):
			if mine.enabled:
				self.mine_sprites[index].draw(screen)

	# Animate mine placement
	def animate_mine(self, screen):
		if self.placing_mine:
			alpha = 255 - (self.mine_text_y * 10)
			red = pygame.Color(190, 75, 75)
			font = pygame.font.SysFont("arial", 42, True)
			label = font.render('O', 1, red)

			blit_with_alpha(screen, label, [self.rect.x + (self.rect.width / 2) - 16, self.rect.y + self.mine_text_y], alpha)
			self.mine_text_y += 2
			if self.mine_text_y >= 40:
				self.placing_mine = False
				self.mine_text_y = 0

	# Animate healing
	def animate_heal(self, screen):
		if self.healing:
			alpha = 255 - (-self.heal_text_y * 10)
			green = pygame.Color(75, 190, 75)
			font = pygame.font.SysFont("arial", 42, True)
			label = font.render('+', 1, green)

			blit_with_alpha(screen, label, [self.rect.x + (self.rect.width / 2) - 12, self.rect.y + self.heal_text_y], alpha)
			self.heal_text_y -= 2
			if self.heal_text_y <= -40:
				self.healing = False
				self.heal_text_y = 0
