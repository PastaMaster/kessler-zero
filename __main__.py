import pygame as pg
import display
import title
import game
import leaderboard
import exit_token

def main():
	# Initialization
	pg.init()
	display.init()
	pg.display.set_caption(title.TITLE)
	# pg.display.set_icon(icon)

	# Main loop
	while not exit_token.exiting:
		title_screen = title.Screen()
		while not exit_token.exiting and title_screen.handle_events():
			pass

		game_round = game.Round()
		while not exit_token.exiting and game_round.handle_events():
			game_round.update()

		leaderboard_screen = leaderboard.Screen(game_round.score)
		while not exit_token.exiting and leaderboard_screen.handle_events():
			leaderboard_screen.update()

if __name__ == "__main__":
	main()