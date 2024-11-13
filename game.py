import pygame
import random
import math

from settings import *
from camera import Camera
from troop import Troop
from highlightbox import HighlightBox

# creates the click status dict to be passed to other functions, this contains a variety of data about the status of the mouse
def formatClicks(clickStatus, camera):
	# track mouse position
	mouseWindowPos = pygame.mouse.get_pos()
	mousePos = [int(mouseWindowPos[0]/ (WIN_SCALE_FACTOR*camera.zoomAmount) - camera.cameraOrigin[0]), int(mouseWindowPos[1]/(WIN_SCALE_FACTOR*camera.zoomAmount) - camera.cameraOrigin[1])]
	clickStatus["mousePos"] = mousePos 

	# handle left click
	if clickStatus["lDown"]:
		clickStatus["lDown"] = False
		clickStatus["lHold"] = True
		clickStatus["lDownPos"] = mousePos
		if clickStatus["rHold"]:
			clickStatus["rUp"] = True

	# handle right click
	if clickStatus["rDown"]:
		clickStatus["rDown"] = False
		clickStatus["rHold"] = True
		clickStatus["rDownPos"] = mousePos
		if clickStatus["lHold"]:
			clickStatus["lUp"] = True

	# handle scroll up
	if clickStatus["scrollUp"]:
		clickStatus["scrollUp"] = False
		if clickStatus["rHold"]:
			clickStatus["rUp"] = True

	# handle scroll down
	if clickStatus["scrollDown"]:
		clickStatus["scrollDown"] = False
		if clickStatus["rHold"]:
			clickStatus["rUp"] = True

	# handle left release
	if clickStatus["lUp"]:
		clickStatus["lUp"] = False
		clickStatus["lHold"] = False

	# handle right release
	if clickStatus["rUp"]:
		clickStatus["rUp"] = False
		clickStatus["rHold"] = False

	return clickStatus

# returns the next player to play
def endTurn(player, players):
	return players[(players.index(player)+1)%len(players)]

# main game loop of the game
def run(window):
	clock = pygame.time.Clock()
	tick = 0
	camera = Camera(window)

	# # play music
	# music = pygame.mixer.music.load("music/triumphantLoop.wav")
	# pygame.mixer.music.play(-1)
	# pygame.mixer.music.set_volume(0.05)



	objects = []

	troopTypes = ["chicken", "pig", "cow", "cat"]
	troopRanks = ["king", "build", "farm", "army", "none"]

	# for x in range(-5,6):
	# 	for y in range(-5,6):
	# 		objects.append(Troop(random.choice(troopTypes), random.choice(troopRanks), [x,y], random.randint(0,360)))
	
	objects.append(Troop("chicken", "king", [-5,0], 0))
	objects.append(Troop("chicken", "army", [-4,0], 0))
	objects.append(Troop("chicken", "build", [-4,1], 0))
	objects.append(Troop("chicken", "build", [-4,-1], 0))
	objects.append(Troop("chicken", "farm", [-5,1], 0))
	objects.append(Troop("chicken", "farm", [-5,-1], 0))

	objects.append(Troop("cat", "king", [5,0], 180))
	objects.append(Troop("cat", "army", [4,0], 180))
	objects.append(Troop("cat", "build", [4,1], 180))
	objects.append(Troop("cat", "build", [4,-1], 180))
	objects.append(Troop("cat", "farm", [5,1], 180))
	objects.append(Troop("cat", "farm", [5,-1], 180))

	player = "chicken"
	players = ["chicken", "cat"]

	level = [
	[0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,1,1,1,1,1,1,1,0,0,0],
	[0,0,0,1,1,1,1,1,1,1,0,0,0],
	[0,1,1,1,0,1,1,1,0,1,1,1,0],
	[0,1,1,0,0,1,1,1,0,0,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,0,0,1,1,1,0,0,1,1,0],
	[0,1,1,1,0,1,1,1,0,1,1,1,0],
	[0,0,0,1,1,1,1,1,1,1,0,0,0],
	[0,0,0,1,1,1,1,1,1,1,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0]]


	# dict containing mouse information to be passed into other functions
	clickStatus = {
		"lDown" : False,
		"rDown" : False,
		"lUp" : False,
		"rUp" : False,
		"lHold" : False,
		"rHold" : False,
		"lDownPos" : [0, 0],
		"rDownPos" : [0, 0],
		"mousePos" : [0, 0],
		"scrollUp" : False,
		"scrollDown" : False
	}

	leftClick = False
	rightClick = False

	running = True
	while running:
		# cap fps at FPS
		clock.tick(FPS)
		if tick%60==0:
			print(clock.get_fps())

		clickStatus = formatClicks(clickStatus, camera)

		# check all pygame events
		for event in pygame.event.get():
			# handle quitting the game via the X button
			if event.type == pygame.QUIT:
				running = False

			# handle mouse down
			if event.type == pygame.MOUSEBUTTONDOWN:
				# left click
				if event.button == 1:
					clickStatus["lDown"] = True
				# right click
				if event.button == 3:
					clickStatus["rDown"] = True
				# scroll up
				if event.button == 4:
					clickStatus["scrollUp"] = True
				# scrollDown
				if event.button == 5:
					clickStatus["scrollDown"] = True

			# handle mouse up
			if event.type == pygame.MOUSEBUTTONUP:
				# left click
				if event.button == 1:
					clickStatus["lUp"] = True
				# right click
				if event.button == 3:
					clickStatus["rUp"] = True
		
		clickedObject = camera.handleMouse(clickStatus, objects, player, level)
		if clickedObject != None and clickedObject.type == "highlightBox":
			player = endTurn(player, players)


		# object interactions
		deleteFlag = False
		for obj in objects:
			obj.tick()
			if obj.delete:
				deleteFlag = True
		# delete objects
		if deleteFlag:
			objects = [obj for obj in objects if not obj.delete]

		camera.render(objects, tick)
		# used for animations
		tick += 1
