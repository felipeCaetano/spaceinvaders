"""
class Laser do jogo
"""

import pygame


class Laser(pygame.sprite.Sprite):
	def __init__(self, pos, speed, screen_height):
		super(Laser, self).__init__()
		self.image = pygame.Surface((4, 20))
		self.rect = self.image.get_rect(center=pos)
		self.image.fill('white')
		self.speed = speed
		self.heigth_y_constraint = screen_height
		self.sound = pygame.mixer.Sound('audio/laser.wav')
		self.sound.set_volume(.2)

	def destroy(self):
		if self.rect.y <= -50 or self.rect.y >= self.heigth_y_constraint + self.rect.y:
			self.kill()

	def update(self, *args, **kwargs) -> None:
		self.rect.y += self.speed
		self.destroy()