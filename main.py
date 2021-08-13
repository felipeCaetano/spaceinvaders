"""
SPACE INVADERS WITH PYGAME
"""

import sys
import time
from random import choice, randint

import pygame

from aliens import Aliens, Extra
from laser import Laser
from player import Player
import obstacles


class Game:
	def __init__(self):
		self.new_game = False
		self.player = Player((screen_width / 2, screen_height), screen_width, 5)
		self.player_sprite = pygame.sprite.GroupSingle(self.player)
		self.lives_surf = pygame.image.load(
			'graphics/player.png').convert_alpha()
		self.lives_x_start_pos = screen_width - (self.lives_surf.get_size()[0]*2+20)
		self.score = 0
		self.font = pygame.font.Font('font/Pixeled.ttf', 14)
		self.shape = obstacles.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obs_num = 4
		self.obs_x_pos = [
			num * (screen_width / self.obs_num) for num in range(self.obs_num)
		]
		self.create_multiple_obstacles(
			self.obs_x_pos, x_start=screen_width / 15, y_start=480)
		self.aliens_direction = 1
		self.aliens = pygame.sprite.Group()
		self.aliens_lasers = pygame.sprite.Group()
		self.aliens_setup(rows=6, cols=8)
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40, 80)
		music = pygame.mixer.Sound('audio/music.wav')
		music.set_volume(.2)
		music.play(loops=-1)
		self.explosion = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion.set_volume(.3)

	def aliens_setup(self, rows, cols, x_distance=60, y_distance=48,
	                 x_offset=70, y_offset=100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				if row_index == 0: alien = Aliens('yellow', x, y)
				elif 1 <= row_index <= 2: alien = Aliens('green', x, y)
				else: alien = Aliens('red', x, y)
				self.aliens.add(alien)

	def aliens_position_checker(self):
		all_aliens = self.aliens.sprites()
		for aliens in all_aliens:
			if aliens.rect.right >= screen_width:
				self.aliens_direction = -1
				self.aliens_move_down(2)
			elif aliens.rect.left <= 0:
				self.aliens_direction = 1
				self.aliens_move_down(2)

	def aliens_move_down(self, distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.move_down(distance)

	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
			self.aliens_lasers.add(laser_sprite)

	def create_obstacle(self, x_start, y_start, offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index, col in enumerate(row):
				if col == 'X':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacles.Block(
						self.block_size, (198, 30, 218), x, y)
					self.blocks.add(block)

	def create_multiple_obstacles(self, offset, x_start, y_start):
		for offset_x in offset:
			self.create_obstacle(x_start, y_start, offset_x)

	def display_lives(self):
		for live in range(self.player.lives - 1):
			x = self.lives_x_start_pos + (live * (self.lives_surf.get_size()[0]+10))
			screen.blit(self.lives_surf, (x, 8))

	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}', False, 'white')
		score_rect = score_surf.get_rect(topleft=(0, 0))
		screen.blit(score_surf, score_rect)

	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right', 'left']), screen_width))
			self.extra_spawn_time = randint(400, 800)

	def collision_checks(self):
		if self.player_sprite.sprite.lasers:
			for laser in self.player_sprite.sprite.lasers:
				if pygame.sprite.spritecollide(laser, self.blocks, True):
					laser.kill()
				aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value[alien.color]
					laser.kill()
					self.explosion.play(loops=0)
				if pygame.sprite.spritecollide(laser, self.extra, True):
					laser.kill()
					self.score += 500
		if self.aliens_lasers:
			for laser in self.aliens_lasers:
				if pygame.sprite.spritecollide(laser, self.blocks, True):
					laser.kill()
				if pygame.sprite.spritecollide(laser, self.player_sprite, False):
					laser.kill()
					self.player.lives -= 1
					if self.player.lives <= 0:
						self.game_over()
		if self.aliens:
			for aliens_hit in self.aliens:
				pygame.sprite.spritecollide(aliens_hit, self.blocks, True)
				if pygame.sprite.spritecollide(aliens_hit, self.player_sprite, False):
					pygame.quit()
					sys.exit(0)

	def victory_message(self):
		if not self.aliens.sprites():
			victory_surf = self.font.render("You Won!", False, 'white')
			victory_rect = victory_surf.get_rect(
				center=(screen_width/2, screen_height/2)
			)
			self.extra_spawn_time = 1
			screen.blit(victory_surf, victory_rect)

	def game_over(self):
		self.font = pygame.font.Font('font/Pixeled.ttf', 24)
		end_surf = self.font.render("GAME OVER", False, 'green')
		font = pygame.font.Font('font/Pixeled.ttf', 14)
		handle_surf = font.render("press space", False, 'green')
		end_rect = end_surf.get_rect(
			center=(screen_width / 2, screen_height / 2)
		)
		handle_rect = handle_surf.get_rect(
			topright=(screen_width/2, end_rect.bottom + 20)
		)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.new_game = False
						self.font = pygame.font.Font('font/Pixeled.ttf', 14)
						return 0
				screen.fill((30, 30, 30))
				screen.blit(end_surf, end_rect)
				screen.blit(handle_surf, handle_rect)
				if time.time() % 1 > .5:
					pygame.draw.rect(screen, (30, 30, 30), handle_rect)
				pygame.display.flip()

	def menu(self):
		if not self.new_game:
			offset = 10
			logo = pygame.image.load(
				'graphics/space-invaders-logo.png').convert_alpha()
			logo = pygame.transform.scale(
				logo, (int(logo.get_width()*.45), int(logo.get_height()*.45)))
			logo_rect = logo.get_rect(
				center=(screen_width//2, logo.get_height()//2))
			point = pygame.image.load('graphics/red.png')
			point = pygame.transform.scale(
				point, (point.get_width()//2, point.get_height()//2))
			new_surf = self.font.render("New Game", False, 'white')
			record_surf = self.font.render("Records", False, 'white')
			credits_surf = self.font.render("Credits", False, 'white')
			year_surf = self.font.render(".2021.", False, 'white')
			new_rect = new_surf.get_rect(
				center=(screen_width / 2, screen_height / 2)
			)
			record_rect = record_surf.get_rect(
				center=(screen_width / 2, new_rect.bottom + offset))
			credits_rect = credits_surf.get_rect(
				center=(screen_width / 2, record_rect.bottom + offset)
			)
			year_rect = year_surf.get_rect(
				center=(screen_width / 2, screen_height - offset)
			)
			point_rect = point.get_rect(
				center=(new_rect.left - 3*offset, new_rect.centery))
			pos = 0
			while True:
				screen.fill((30, 30, 30))
				screen.blit(logo, logo_rect)
				screen.blit(new_surf, new_rect)
				screen.blit(record_surf, record_rect)
				screen.blit(credits_surf, credits_rect)
				screen.blit(year_surf, year_rect)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit(0)
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_DOWN:
							point_rect.y += 3 * offset
							pos += 1
						if event.key == pygame.K_UP:
							point_rect.y -= 3 * offset
							pos -= 1
						if event.key == pygame.K_SPACE and pos == 0:
							self.new_game = True
							self._restart()
							return 0
						elif event.key == pygame.K_SPACE and pos == 1:
							# records
							self.records()
						elif event.key == pygame.K_SPACE and pos == 2:
							# credits
							self.credits()
				if pos < 0:
					pos = 2
					point_rect.centery = credits_rect.centeryy + offset//2
				elif pos > 2:
					pos = 0
					point_rect.centery = new_rect.centery + offset//2
				screen.blit(point, point_rect)
				pygame.display.flip()

	def run(self):
		self.menu()
		self.player_sprite.draw(screen)
		self.blocks.draw(screen)
		self.aliens.draw(screen)
		self.aliens_lasers.draw(screen)
		self.extra.draw(screen)
		self.display_lives()
		self.player_sprite.update()
		self.aliens_lasers.update()
		self.extra.update()
		self.aliens.update(self.aliens_direction)
		self.aliens_position_checker()
		self.extra_alien_timer()
		self.player_sprite.sprite.lasers.draw(screen)
		self.display_score()
		self.victory_message()
		self.collision_checks()

	def records(self):
		pass

	def credits(self):
		pass

	def _restart(self):
		self.player = Player((screen_width / 2, screen_height), screen_width, 5)
		self.player_sprite = pygame.sprite.GroupSingle(self.player)
		self.score = 0
		self.font = pygame.font.Font('font/Pixeled.ttf', 14)
		self.aliens_direction = 1
		self.aliens = self.aliens = pygame.sprite.Group()
		self.aliens_setup(rows=6, cols=8)
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40, 80)


class CRT:
	def __init__(self):
		self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

	def create_crt_lines(self):
		line_height = 3
		line_amount = screen_height // line_height
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(
				self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

	def draw(self):
		self.tv.set_alpha(randint(75, 90))
		self.create_crt_lines()
		screen.blit(self.tv, (0, 0))


if __name__ == "__main__":
	pygame.init()
	screen_width = 600
	screen_height = 600
	screen = pygame.display.set_mode((screen_width, screen_height))
	clock = pygame.time.Clock()
	game = Game()
	crt = CRT()
	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER, 800)
	while True:
		# game.menu()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			if event.type == ALIENLASER:
				game.alien_shoot()
		screen.fill((30, 30, 30))
		game.run()
		crt.draw()
		pygame.display.flip()
		clock.tick(30)
