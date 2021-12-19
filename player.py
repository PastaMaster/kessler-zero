import pygame as pg
from os.path import join
import display

# Settings
SCALE = 0.5
ACCELERATION = 300
MAX_SPEED = 256
TURN_SPEED = 120

class Ship(pg.sprite.Sprite):
	def __init__(self):
		# Initialize sprite, load assets, and cache screen centre coordinates.
		pg.sprite.Sprite.__init__(self)
		image = pg.image.load(join("Assets", "Player.png"))
		self.IMAGE = pg.transform.smoothscale(image, [px * 0.5 for px in image.get_size()])
		self.CENTER = pg.display.get_surface().get_rect().center

		# Init state variables.
		self.turn_input = 0
		self.boost_input = 0

		self.velocity = pg.Vector2()
		self.position = pg.Vector2()
		self.rotation = 0.0

	def update(self, delta_time: float):
		# Handle rotation.
		self.rotation = -180 + (self.rotation + self.turn_input * TURN_SPEED * delta_time + 180) % 360
		self.image = pg.transform.rotate(self.IMAGE, self.rotation)
		self.rect = self.image.get_rect(center = self.CENTER)

		# Handle movement.
		if self.boost_input != 0:
			boost = self.velocity + self.boost_input * pg.Vector2(0, 1).rotate(-self.rotation) * ACCELERATION * delta_time
			self.velocity = boost if boost.magnitude_squared() <= MAX_SPEED * MAX_SPEED else boost.normalize() * MAX_SPEED

		self.position += self.velocity * delta_time

	def receive_input(self, input: int):
		match input:
			case pg.K_w:
				self.boost_input = -1
			case pg.K_s:
				self.boost_input = 1
			case pg.K_a:
				self.turn_input = 1
			case pg.K_d:
				self.turn_input = -1

	def cancel_input(self, input: int):
		match input:
			case pg.K_w if self.boost_input == -1:
				self.boost_input = 0
			case pg.K_s if self.boost_input == 1:
				self.boost_input = 0
			case pg.K_a if self.turn_input == 1:
				self.turn_input = 0
			case pg.K_d if self.turn_input == -1:
				self.turn_input = 0