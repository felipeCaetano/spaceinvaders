"""Obstacles of the game"""

import pygame

shape = [
	'  XXXXXXX',
	' XXXXXXXXX',
	'XXXXXXXXXXX',
	'XXXXXXXXXXX',
	'XXXXXXXXXXX',
	'XXX     XXX',
	'XX       XX',
]

class Block(pygame.sprite.Sprite):
	def __init__(self, size, color, x, y):
		super(Block, self).__init__()
		self.image = pygame.Surface((size, size))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft=(x, y))