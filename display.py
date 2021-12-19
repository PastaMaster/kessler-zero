import pygame as pg
from pygame.constants import BLEND_ADD
from os.path import join

# Settings
MAX_RESOLUTION = (1920, 1080)
MAX_FPS = 60
AA_FILL_COLOR = (0, 0, 0)

TITLE_SIZE = 128
TITLE_COLOR = (90, 120, 255)

HEADER_SIZE = 64
HEADER_COLOR = (255, 255, 255)

INFO_SIZE = 40
INFO_COLOR = (255, 255, 255)

def init():
	global BACKGROUND
	global COLORS

	global TITLE_FONT
	global HEADER_FONT
	global INFO_FONT

	# Set display mode.
	pg.display.set_mode(
		min(pg.display.list_modes()[0], MAX_RESOLUTION, key = lambda i: i[0]),
		pg.FULLSCREEN | pg.SCALED,
		vsync = 1
	)

	# Create the background texture.
	BACKGROUND = pg.Surface(pg.display.get_surface().get_size())
	tile = pg.image.load(join("Assets", "Space.png"))
	grid = pg.Vector2(tile.get_size())

	for x in range(int(BACKGROUND.get_width() / grid.x + 1)):
		for y in range(int(BACKGROUND.get_height() / grid.y + 1)):
			BACKGROUND.blit(tile, (x * grid.x, y * grid.y))

	# Load fonts.
	TITLE_FONT = pg.font.Font(join("Assets", "font.TTF"), TITLE_SIZE)
	HEADER_FONT = pg.font.Font(join("Assets", "font.TTF"), HEADER_SIZE)
	INFO_FONT = pg.font.Font(join("Assets", "font.TTF"), INFO_SIZE)

	COLORS = {
		TITLE_FONT: TITLE_COLOR,
		HEADER_FONT: HEADER_COLOR,
		INFO_FONT: INFO_COLOR
	}

	# Hide mouse.
	pg.mouse.set_visible(False)

def draw_background():
	pg.display.get_surface().blit(BACKGROUND, (0, 0))

# def draw_text(text: str, position: tuple[int, int] | pg.rect.Rect, font: pg.font.Font, color: tuple[int, int, int]):
# 	pg.display.get_surface().blit(font.render(text, True, color, (0, 0, 0)), position, special_flags = BLEND_ADD)

# def draw_text_centered(text: str, position: tuple[int, int], font: pg.font.Font, color: tuple[int, int, int]):
# 	text_image = font.render(text, True, color, BG_COLOR)
# 	pg.display.get_surface().blit(text_image, text_image.get_rect(center = position))

def blit_text_left(target: pg.Surface, text: str, font: pg.font.Font, position: tuple[int, int] | pg.Rect):
	target.blit(font.render(text, True, COLORS[font], AA_FILL_COLOR), position, special_flags = BLEND_ADD)

def draw_text_left(text: str, font: pg.font.Font, position: tuple[int, int] | pg.Rect):
	blit_text_left(pg.display.get_surface(), text, font, position)

def draw_text_right(text: str, font: pg.font.Font, right_x: int, top_y: int):
	image = font.render(text, True, COLORS[font], AA_FILL_COLOR)
	pg.display.get_surface().blit(image, image.get_rect(right = right_x, top = top_y), special_flags = BLEND_ADD)

def draw_text_centered(text: str, font: pg.font.Font, center_x: int, top_y: int):
	image = font.render(text, True, COLORS[font], AA_FILL_COLOR)
	pg.display.get_surface().blit(image, image.get_rect(centerx = center_x, top = top_y), special_flags = BLEND_ADD)