import pygame as pg
from os.path import join
import display
import random

DENSITY = 100
MIN_SPAWN_DISTANCE = display.MAX_RESOLUTION[0]
MAX_SPAWN_DISTANCE = 4000
CULL_DISTANCE = 5000

class AsteroidField:
	def __init__(self):
		# Load assets.
		global IMAGES
		IMAGES = [
			[
				pg.image.load(join("Assets", "meteorBrown_tiny1.png")),
				pg.image.load(join("Assets", "meteorBrown_tiny2.png")),
				pg.image.load(join("Assets", "meteorGrey_tiny1.png")),
				pg.image.load(join("Assets", "meteorGrey_tiny2.png")),
			],
			[
				pg.image.load(join("Assets", "meteorBrown_small1.png")),
				pg.image.load(join("Assets", "meteorBrown_small2.png")),
				pg.image.load(join("Assets", "meteorGrey_small1.png")),
				pg.image.load(join("Assets", "meteorGrey_small2.png")),
			],
			[
				pg.image.load(join("Assets", "meteorBrown_med1.png")),
				pg.image.load(join("Assets", "meteorBrown_med3.png")),
				pg.image.load(join("Assets", "meteorGrey_med1.png")),
				pg.image.load(join("Assets", "meteorGrey_med2.png")),
			],
			[
				pg.image.load(join("Assets", "meteorBrown_big1.png")),
				pg.image.load(join("Assets", "meteorBrown_big2.png")),
				pg.image.load(join("Assets", "meteorBrown_big3.png")),
				pg.image.load(join("Assets", "meteorBrown_big4.png")),
				pg.image.load(join("Assets", "meteorGrey_big1.png")),
				pg.image.load(join("Assets", "meteorGrey_big2.png")),
				pg.image.load(join("Assets", "meteorGrey_big3.png")),
				pg.image.load(join("Assets", "meteorGrey_big4.png")),
			]
		]

		global SCREEN_CENTER
		SCREEN_CENTER = pg.Vector2(pg.display.get_surface().get_rect().center)

		# Init state variables.
		global asteroids_killed
		asteroids_killed = 0
		self.asteroids = pg.sprite.Group()
		self.visible = pg.sprite.Group()

		# Generate the starting field.
		for _ in range(DENSITY):
			self.spawn_asteroid(pg.Vector2(0, 0), random.randint(100, 1000))

	def update(self, player_position: pg.Vector2):
		self.asteroids.update(player_position, self.visible)

		global asteroids_killed
		if asteroids_killed > 0:
			asteroids_killed -= 1
			self.spawn_asteroid(player_position, MIN_SPAWN_DISTANCE)

	def spawn_asteroid(self, position: pg.Vector2, min_distance: float):
		self.asteroids.add(Asteroid(
			position + pg.Vector2(0, 1).rotate(random.uniform(0, 360)) * random.uniform(min_distance, MAX_SPAWN_DISTANCE),
			random.uniform(0, 360)))

class Asteroid(pg.sprite.Sprite):
	def __init__(self, position: pg.Vector2, rotation: float):
		# Initialize sprite and set world position.
		self.POSITION = pg.Vector2(int(position.x), int(position.y))
		self.culling_check = self.check_culling_distance

		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.rotate(random.choice(random.choice(IMAGES)), rotation)
		self.rect = self.image.get_rect(center = self.POSITION)
		self.mask = pg.mask.from_surface(self.image)

	def update(self, player_position: pg.Vector2, visible_group: pg.sprite.Group):
		# Update screen position.
		position = self.POSITION - player_position
		self.rect.center = position + SCREEN_CENTER

		# Cull distant asteroids.
		self.culling_check(position.magnitude_squared(), visible_group)

	# Cull rendering off-screen.
	def check_visibility(self, distance_squared: float, visible_group: pg.sprite.Group):
		if distance_squared > MIN_SPAWN_DISTANCE * MIN_SPAWN_DISTANCE:
			self.remove(visible_group)
			self.culling_check = self.check_culling_distance

	# Cull completely if too distant.
	def check_culling_distance(self, distance_squared: float, visible_group: pg.sprite.Group):
		if distance_squared > CULL_DISTANCE * CULL_DISTANCE:
			self.on_kill()
		elif distance_squared < MIN_SPAWN_DISTANCE * MIN_SPAWN_DISTANCE:
			self.add(visible_group)
			self.culling_check = self.check_visibility

	# Increment the kill counter regardless of how kill is called.
	def on_kill(self):
		global asteroids_killed
		asteroids_killed += 1
		pg.sprite.Sprite.kill(self)

	def kill(self):
		self.on_kill()