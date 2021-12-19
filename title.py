import pygame as pg
from pygame.constants import BLEND_ADD
from leaderboard import FILENAME
import display as d
import exit_token

# Settings
TITLE = "Kessler 0"
TITLE_OFFSET = 100
BLINK_TIME = 1000

ROWS = 10
NAME_WIDTH = 600
SCORE_WIDTH = 400
LINE_SPACING = 4

class Screen:
	def __init__(self):
		# Create a surface to display the leaderboard.
		line_height = d.INFO_SIZE + LINE_SPACING
		self.BOARD = pg.Surface((NAME_WIDTH + SCORE_WIDTH, line_height * ROWS))

		# Read data from the file and blit it onto the board.
		try:
			with open(FILENAME) as file:
				data = file.readlines()
				data.sort(key = lambda line: -int(line.split(",")[1]))

				for i in range(min(len(data), ROWS)):
					row = data[i].strip("\n").split(",")
					d.blit_text_left(self.BOARD, row[0], d.INFO_FONT, (0, i * line_height))
					d.blit_text_left(self.BOARD, row[1], d.INFO_FONT, (NAME_WIDTH, i * line_height))

		# Display a message if the leaderboard is empty.
		except FileNotFoundError:
			d.blit_text_left(self.BOARD, "There are no high scores... yet.", d.INFO_FONT, (0, 0))

		# Update the display on a blink timer.
		self.blink = True
		self.update()
		pg.time.set_timer(pg.USEREVENT, BLINK_TIME)

	def handle_events(self) -> bool:
		for event in pg.event.get():
			match event.type:

				# Wait for player input.
				case pg.KEYDOWN if event.key == pg.K_ESCAPE:
					exit_token.exiting = True
					return False
				case pg.KEYUP:
					return False

				# System events.
				case pg.USEREVENT:
					self.update()
				case pg.QUIT:
					exit_token.exiting = True
					return False

		return True

	def update(self):
		# Update display.
		d.draw_background()
		screen_rect = pg.display.get_surface().get_rect()

		d.draw_text_centered(TITLE, d.TITLE_FONT, screen_rect.centerx, TITLE_OFFSET)
		pg.display.get_surface().blit(self.BOARD, self.BOARD.get_rect(center = screen_rect.center), special_flags = BLEND_ADD)

		if self.blink:
			d.draw_text_centered("Press any key to start", d.HEADER_FONT, screen_rect.centerx, screen_rect.bottom - 2 * d.HEADER_SIZE)
		self.blink = not self.blink

		pg.display.update()