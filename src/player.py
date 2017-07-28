import pygame
from general import *
from mine import *


class Player(pygame.sprite.Sprite):
	def __init__(self, screen):
		# Set player sprite
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('player.png', -1)

		# Setup player
		self.x_speed = 64
		self.y_speed = 64
		self.screen = screen
		self.maxhealth = 100
		self.health = self.maxhealth
		self.maxmines = 6
		self.minesleft = self.maxmines
		self.mine_cooldown = 3
		self.mines = []
		self.mine_sprites = []
		self.destination_x = self.rect.x
		self.destination_y = self.rect.y
		self.placing_mine = False
		self.mine_text_y = 0

	def move(self, key, walls):
		if self.destination_x == self.rect.x and self.destination_y == self.rect.y:
			# Setup movement
			destination_x = self.rect.x
			destination_y = self.rect.y
			moved = False
			wall_locs = [[w[0]*64, w[1]*64] for w in walls]

			width, height = self.screen.get_size()
			width -= 256

			if key == K_d or key == K_RIGHT:
				# Move right
				if self.rect.x + self.rect.width < width and [self.rect.x + self.x_speed, self.rect.y] not in wall_locs:
					destination_x += self.x_speed
					print('Player moves right.')
					self.mine_cooldown += 1
					moved = True
				# Jump right wall
				elif [self.rect.x + self.x_speed, self.rect.y] in wall_locs and [self.rect.x + (self.x_speed * 2), self.rect.y] not in wall_locs:
					destination_x += (self.x_speed * 2)
					print('Player jumps wall right.')
					self.mine_cooldown += 1
					moved = True
			elif key == K_a or key == K_LEFT:
				# Move left
				if self.rect.x > 0 and [self.rect.x - self.x_speed, self.rect.y] not in wall_locs:
					destination_x -= self.x_speed
					print('Player moves left.')
					self.mine_cooldown += 1
					moved = True
				# Jump left wall
				elif [self.rect.x - self.x_speed, self.rect.y] in wall_locs and [self.rect.x - (self.x_speed * 2), self.rect.y] not in wall_locs:
					destination_x -= (self.x_speed * 2)
					print('Player jumps wall left.')
					self.mine_cooldown += 1
					moved = True
			elif key == K_w or key == K_UP:
				# Move up
				if self.rect.y > 0 and [self.rect.x, self.rect.y - self.y_speed] not in wall_locs:
					destination_y -= self.y_speed
					print('Player moves up.')
					self.mine_cooldown += 1
					moved = True
				# Jump up wall
				elif [self.rect.x, self.rect.y - self.y_speed] in wall_locs and [self.rect.x, self.rect.y - (self.y_speed * 2)] not in wall_locs:
					destination_y -= (self.y_speed * 2)
					print('Player jumps wall up.')
					self.mine_cooldown += 1
					moved = True
			elif key == K_s or key == K_DOWN:
				# Move down
				if self.rect.y + self.rect.height < height and [self.rect.x, self.rect.y + self.y_speed] not in wall_locs:
					destination_y += self.y_speed
					print('Player moves down.')
					self.mine_cooldown += 1
					moved = True
				# Jump down wall
				elif [self.rect.x, self.rect.y + self.y_speed] in wall_locs and [self.rect.x, self.rect.y + (self.y_speed * 2)] not in wall_locs:
					destination_y += self.y_speed * 2
					print('Player jumps wall down.')
					self.mine_cooldown += 1
					moved = True
			elif key == K_SPACE:
				moved = self.attack()
			self.destination_x = destination_x
			self.destination_y = destination_y
			return moved
		return False

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

	# Check for collision between playet and target sprite
	def check_collision(self, sprite):
		return pygame.sprite.collide_rect(self, sprite)

	# Deal damage to player
	def hurt(self, amount):
		self.health = self.health - amount
		print('Player takes {} damage. {} health remaining.'.format(amount, self.health))

	# Drop mine
	def attack(self):
		mine_on_square = False
		for mine in self.mines:
			if mine.rect.x == self.rect.x and mine.rect.y == self.rect.y and mine.enabled is True:
				mine_on_square = True
		if not mine_on_square:
			if self.minesleft > 0:
				if self.mine_cooldown > 2:
					print('Player places a mine.')
					self.placing_mine = True
					m = Mine(self.rect.x, self.rect.y)
					self.mines.append(m)
					self.mine_sprites.append(pygame.sprite.RenderPlain(m))
					self.minesleft -= 1
					self.mine_cooldown = 0
					return True
				else:
					print('You cannot place two mines immediately after one another.')
			else:
				print('You have no mines left!')
				return False
		else:
			print('There is already a mine here.')
			return False

	# Draw mines to screen
	def draw_mines(self):
		for index, mine in enumerate(self.mines):
			if mine.enabled:
				self.mine_sprites[index].draw(self.screen)

	# Animate mine placement
	def animate_mine(self):
		if self.placing_mine:
			alpha = 255 - (self.mine_text_y * 10)
			red = pygame.Color(190, 75, 75)
			font = pygame.font.SysFont("arial", 42, True)
			label = font.render('O', 1, red)

			blit_with_alpha(self.screen, label, [self.rect.x + (self.rect.width / 2) - 16, self.rect.y + self.mine_text_y], alpha)
			self.mine_text_y += 2
			if self.mine_text_y >= 40:
				self.placing_mine = False
				self.mine_text_y = 0

