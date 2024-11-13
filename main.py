import pygame
import os

from settings import *
import game

def main():
	# setup pygame window
	pygame.init()
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	window = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
	pygame.display.set_caption(WINDOW_TITLE)

	# run game
	game.run(window)

if __name__ == "__main__":
	main()