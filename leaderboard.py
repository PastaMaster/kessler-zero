import pygame as pg
import display
import exit_token

FILENAME = "leaderboard.csv"

TITLE_OFFSET = 200
INFO_OFFSET = 100
NAME_OFFSET = 200

class Screen:
	def __init__(self, score: int):
		self.score = str(score)
		self.name = ""
		self.background = pg.display.get_surface().copy()

	def handle_events(self) -> bool:
		for event in pg.event.get():
			match event.type:

				# Player input.
				case pg.KEYDOWN:
					match event.key:
						case pg.K_ESCAPE:
							exit_token.exiting = True
							return False
						case pg.K_BACKSPACE:
							self.name = self.name[:-1]
						case pg.K_RETURN:
							pass
						case _:
							self.name += event.unicode
				case pg.KEYUP if event.key == pg.K_RETURN:
					with open(FILENAME, "a") as file:
						file.write(self.name + "," + self.score + "\n")
					return False

				# Application quit.
				case pg.QUIT:
					exit_token.exiting = False
					return False

		return True

	def update(self):
		# Update display.
		pg.display.get_surface().blit(self.background, (0, 0))
		screen_rect = pg.display.get_surface().get_rect()

		display.draw_text_centered("Game Over!", display.TITLE_FONT, screen_rect.centerx, screen_rect.centery - TITLE_OFFSET)
		display.draw_text_centered("Your score: " + self.score, display.HEADER_FONT, screen_rect.centerx, screen_rect.centery)
		display.draw_text_centered("Enter name:", display.INFO_FONT, screen_rect.centerx, screen_rect.centery + INFO_OFFSET)
		display.draw_text_centered(self.name, display.HEADER_FONT, screen_rect.centerx, screen_rect.centery + NAME_OFFSET)

		pg.display.update()