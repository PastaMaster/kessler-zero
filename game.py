import pygame as pg
from pygame.constants import BLEND_ADD
import display
import player
import level
import exit_token

UI_OFFSET = 100

class Round:
	def __init__(self):
		# Initialize game objects.
		self.PLAYER = player.Ship()
		self.ASTEROID_FIELD = level.AsteroidField()

		# Initialize systems.
		self.CLOCK = pg.time.Clock()
		self.score = 0
		self.timer = 60
		pg.time.set_timer(pg.USEREVENT, 1000)

	def handle_events(self) -> bool:
		for event in pg.event.get():
			match event.type:

				# Player input.
				case pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						exit_token.exiting = True
						return False
					else:
						self.PLAYER.receive_input(event.key)
				case pg.KEYUP:
					self.PLAYER.cancel_input(event.key)

				# Timer.
				case pg.USEREVENT:
					self.timer -= 1
					if (self.timer < 1):
						return False

				# Application quit.
				case pg.QUIT:
					exit_token.exiting = True
					return False

		return True

	def update(self):
		# Update game objects.
		delta_time = self.CLOCK.tick(display.MAX_FPS) / 1000
		self.PLAYER.update(delta_time)
		self.ASTEROID_FIELD.update(self.PLAYER.position)

		# Detect collisions and call kill on collided asteroids.
		self.score += len(pg.sprite.spritecollide(self.PLAYER, self.ASTEROID_FIELD.visible, True, pg.sprite.collide_mask))

		# Update display.
		display.draw_background()
		screen = pg.display.get_surface()

		screen.blit(self.PLAYER.image, self.PLAYER.rect)
		self.ASTEROID_FIELD.visible.draw(screen)

		display.draw_text_left(str(self.timer), display.INFO_FONT, (UI_OFFSET, UI_OFFSET))
		display.draw_text_right(str(self.score), display.INFO_FONT, screen.get_rect().right - UI_OFFSET, UI_OFFSET)

		pg.display.update()
