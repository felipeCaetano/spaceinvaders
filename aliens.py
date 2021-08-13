"""
aliens in the game
"""

import pygame

from laser import Laser


class Aliens(pygame.sprite.Sprite):
	def __init__(self, color, x, y):
		super(Aliens, self).__init__()
		file_path = 'graphics/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft=(x, y))
		self.color = color
		self.value = {'red': 100, 'green': 200,	'yellow': 300}
		self.lasers = pygame.sprite.Group()

	def move_down(self, distance):
		self.rect.y += distance

	def shoot_laser(self):
		laser_sprite = Laser(self.rect.center, -6, 600)
		self.lasers.add(laser_sprite)

	def update(self, direction) -> None:
		self.rect.x += direction
		self.lasers.update()


class Extra(pygame.sprite.Sprite):
	def __init__(self, side, screen_width):
		super(Extra, self).__init__()
		self.image = pygame.image.load("graphics/extra.png").convert_alpha()
		if side == 'right':
			x = screen_width + 50
			self.speed = -3
		else:
			x = -50
			self.speed = 3
		self.rect = self.image.get_rect(topleft=(x, 80))

	def update(self):
		self.rect.x += self.speed
