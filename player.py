"""
Player do Space Invaders
"""
import pygame

from laser import Laser


class Player(pygame.sprite.Sprite):
	"""class player do space invaders"""
	def __init__(self, pos, constraint, speed):
		super(Player, self).__init__()
		self.image = pygame.image.load('graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom=pos)
		self.max_constraint = constraint
		self.speed = speed
		self.lives = 3
		self.ready = False
		self.laser_time = pygame.time.get_ticks()
		self.laser_cooldown = 700
		self.lasers = pygame.sprite.Group()

	def get_input(self):
		"""le entrada do usuário."""
		pygame.event.clear()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed
		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()

	def recharge(self):
		"""verifica tempo de espera para o disparo do laser"""
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_constraint:
			self.rect.right = self.max_constraint

	def shoot_laser(self):
		self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
		for laser in self.lasers:
			laser.sound.play(loops=0)

	def update(self, *args, **kwargs) -> None:
		self.recharge()
		self.constraint()
		self.lasers.update()
		self.get_input()
