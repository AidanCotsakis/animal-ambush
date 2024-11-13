import pygame
import math
from functools import cmp_to_key

from settings import *
from spritestack import getSpriteDict

import threading

# a comparator which returns what object should be drawn first
# the data is structured as follows [cameraPosBeforeZ, cameraPosAfterZ, obj]
def compareObjectPositions(obj1Data, obj2Data):
	y1 = obj1Data[0][1]
	y2 = obj2Data[0][1]
	if abs(y1-y2) < 0.1:
		y1 = obj1Data[2].level
		y2 = obj2Data[2].level

		if abs(y1-y2) < 0.1:
			y1 = obj1Data[2].priority
			y2 = obj2Data[2].priority

	return y1 - y2

class Camera():
	def __init__(self, window):
		self.window = window
		self.win = pygame.Surface(WIN_SIZE)
		
		self.cameraPos = [0,0]
		self.cameraRotation = 360*5000

		self.zoomAmount = 1
		self.winSize = WIN_SIZE
		self.cameraOrigin = CAMERA_ORIGIN

		self.cameraPosOffset = [0,0]
		self.cameraRotationOffset = 0

		# load cache of all sprite stacks in a new thread and display loading screen
		self.stacks = {}
		threadStatus = {
			"numCompleted": 0,
			"total": 1
		}
		thread = threading.Thread(target=getSpriteDict, args=(self.stacks,threadStatus,))
		thread.start()
		self.showLoadingScreen(thread, threadStatus)

	# shows a loading screen while caches are generating
	def showLoadingScreen(self, thread, threadStatus):
		loadingScreen = pygame.image.load("images/loadingScreen0.png")
		scaledLoadingScreen = pygame.transform.scale(loadingScreen, WIN_SIZE)
		clock = pygame.time.Clock()

		running = True
		while running and thread.is_alive():
			# cap fps at FPS
			clock.tick(10)

			# check all pygame events
			for event in pygame.event.get():
				# handle quitting the game via the X button
				if event.type == pygame.QUIT:
					running = False

			# draw loading screen and bar
			self.win.blit(scaledLoadingScreen, (0,0))
			pygame.draw.rect(self.win, LOADING_BAR_BACKGROUND_COLOUR, LOADING_BAR_BOX, 0, 50)
			pygame.draw.rect(self.win, LOADING_BAR_COLOUR, (LOADING_BAR_BOX[0], LOADING_BAR_BOX[1], int((threadStatus["numCompleted"]/threadStatus["total"])*LOADING_BAR_BOX[2]), LOADING_BAR_BOX[3]), 0, 50)

			self.renderWindow()

	# render win onto window
	def renderWindow(self):
		# scale win
		scaled = pygame.transform.scale_by(self.win, WIN_SCALE_FACTOR*self.zoomAmount)
		w = scaled.get_width()
		h = scaled.get_height()
		# draw onto window
		self.window.blit(scaled, (int(WINDOW_SIZE[0]/2-w/2), int(WINDOW_SIZE[1]/2-h/2)))
		pygame.display.update()

	# returns the hypotenuse of a right triangle with side lengths stored in the length 2 list "sides"
	def hypotenuse(self, sides):
		c = math.sqrt(sides[0]**2 + sides[1]**2)
		return c

	# returns the position of the object viewed from the window before z translation 
	def getGroundWinPos(self, obj = None, pos = None):
		if obj != None:
			pos = [obj.pos[0]*LEVEL_TILE_SIZE*STACK_SCALE_FACTOR + obj.drawOffset[0], obj.pos[1]*LEVEL_TILE_SIZE*STACK_SCALE_FACTOR + obj.drawOffset[1]]

		observedRotation = int((self.cameraRotation + self.cameraRotationOffset)/STACK_DEGREE_GAP)*STACK_DEGREE_GAP
		rotationRadians = math.radians(observedRotation)

		# find where the image should be given the current observedRotation
		position = [self.cameraPos[0] + self.cameraPosOffset[0] + pos[0], self.cameraPos[1] + self.cameraPosOffset[1] + pos[1]]
		polarRadius = self.hypotenuse(position)
		polarAngle = math.atan2(position[0], position[1])
		drawPosition = [self.cameraOrigin[0] + polarRadius*math.sin(rotationRadians+polarAngle), self.cameraOrigin[1] + polarRadius*math.cos(rotationRadians+polarAngle)]

		return drawPosition

	def getWinPos(self, pos, obj = None, level = None):
		if obj != None:
			return [pos[0], pos[1]-obj.level*STACK_LEVEL_HEIGHT + obj.drawOffset[2]]
		else:
			return [pos[0], pos[1]-level*STACK_LEVEL_HEIGHT]

	# draws a single sprite stack on win given a game pos, converts it to a screen pos and renders
	def drawStack(self, pos, obj = None, rotation = None, stackName = None):
		if obj != None:
			rotation = obj.rotation
			if obj.type == "troop":
				stackName = f"{obj.team}-{obj.rank}"
			elif obj.type == "highlightBox":
				stackName = "highlightBox"

		rotationIndex = int((self.cameraRotation + self.cameraRotationOffset + rotation)/STACK_DEGREE_GAP) % int(360/STACK_DEGREE_GAP)

		image = self.stacks[stackName][rotationIndex]

		imageWidth = image.get_width()
		imageHeight = image.get_height()

		self.win.blit(image, (int(pos[0] - imageWidth/2), int(pos[1] - (imageHeight-imageWidth/2))))

	# handles flagging objects as clicked or not, returns the successfully selected object, or none 
	def handleObjectSelection(self, clickStatus, objects, player, level):
		objectData = self.getSortedObjects(objects)

		minDistance = math.inf
		minObj = None

		prevSelected = None

		for obj in objectData:
			if obj[2].selectable and not (obj[2].type == "troop" and obj[2].team != player):
				if obj[2].selected:
					obj[2].selected = False
					prevSelected = obj[2]
	
				differenceCoords = [clickStatus["mousePos"][0] - (obj[1][0] - CAMERA_ORIGIN[0]/self.zoomAmount), clickStatus["mousePos"][1] - (obj[1][1] - CAMERA_ORIGIN[1]/self.zoomAmount)]

				distance = self.hypotenuse(differenceCoords)

				if distance < minDistance:
					minDistance = distance
					minObj = obj[2]

		if minDistance < CAMERA_SELECT_DISTANCE and minObj != prevSelected:
			minObj.onSelect(objects, level)
			return minObj
		elif minDistance < CAMERA_SELECT_DISTANCE:
			minObj.selected = True

		return None

	# handles camera movement
	def handleCameraMovement(self, clickStatus):
		# handle right click for rotation
		if clickStatus["rHold"]:
			rotationDifference = int(clickStatus["mousePos"][0]*WIN_SCALE_FACTOR*self.zoomAmount - clickStatus["rDownPos"][0]*WIN_SCALE_FACTOR*self.zoomAmount)
			self.cameraRotationOffset = rotationDifference*CAMERA_ROTATION_MULTIPLIER
		if clickStatus["rUp"]:
			self.cameraRotation += self.cameraRotationOffset
			self.cameraRotationOffset = 0
		
		# handle left click for dragging the screen
		if clickStatus["lHold"]:
			observedRotation = int((self.cameraRotation + self.cameraRotationOffset)/STACK_DEGREE_GAP)*STACK_DEGREE_GAP
			rotationRadians = math.radians(observedRotation)
			
			winPositionDifference = [clickStatus["mousePos"][0] - clickStatus["lDownPos"][0], clickStatus["mousePos"][1] - clickStatus["lDownPos"][1]]
			mouseDistance = self.hypotenuse(winPositionDifference)
			dragAngle = math.atan2(winPositionDifference[1], winPositionDifference[0])
			worldPositionDifference = [int(mouseDistance * math.cos(rotationRadians+dragAngle)), int(mouseDistance * math.sin(rotationRadians+dragAngle))]
			self.cameraPosOffset = worldPositionDifference

		if clickStatus["lUp"]:
			self.cameraPos = [self.cameraPos[0] + self.cameraPosOffset[0], self.cameraPos[1] + self.cameraPosOffset[1]]
			self.cameraPosOffset = [0,0]

		# handle zooming in and out
		if clickStatus["scrollUp"] or clickStatus["scrollDown"]:
			# zoom in
			if clickStatus["scrollUp"]:
				if self.zoomAmount * CAMERA_ZOOM_MULTIPLIER <= CAMERA_ZOOM_MAX:
					self.zoomAmount *= CAMERA_ZOOM_MULTIPLIER
				else:
					self.zoomAmount = CAMERA_ZOOM_MAX

			# zoom out
			if clickStatus["scrollDown"]:
				if self.zoomAmount / CAMERA_ZOOM_MULTIPLIER >= 1:
					self.zoomAmount /= CAMERA_ZOOM_MULTIPLIER
				else:
					self.zoomAmount = 1

			# scale window based on zoom level
			self.winSize = [math.ceil(WIN_SIZE[0]/self.zoomAmount),math.ceil(WIN_SIZE[1]/self.zoomAmount)]
			self.win = pygame.Surface(self.winSize)
			self.cameraOrigin = [math.ceil(CAMERA_ORIGIN[0]/self.zoomAmount),math.ceil(CAMERA_ORIGIN[1]/self.zoomAmount)]

	# handle mouse events given the status of the mouse, returns any object that is clicked, or none
	def handleMouse(self, clickStatus, objects, player, level):
		# detect opject selection on mouse up only when mouse hasnt moved very much
		returnValue = None
		if clickStatus["lUp"] and self.hypotenuse(self.cameraPosOffset) <= CAMERA_SELECT_DISTANCE_THRESHOLD:
			returnValue = self.handleObjectSelection(clickStatus, objects, player, level)
		
		self.handleCameraMovement(clickStatus)

		return returnValue

	# returns a list of objects sorted bases on their y pos, the list includes screen pos before and after z translation
	def getSortedObjects(self, objects):
		objData = []
		for obj in objects:
			beforeZpos = self.getGroundWinPos(obj = obj)
			afterZpos = self.getWinPos(beforeZpos, obj = obj)
			objData.append([beforeZpos, afterZpos, obj])

		objData = sorted(objData, key=cmp_to_key(compareObjectPositions))

		return objData

	# main call to draw everything on to screen
	def render(self, objects, tick = 0):
		self.win.fill(GAME_BACKGROUND_COLOUR)

		envPos = self.getWinPos(self.getGroundWinPos(pos = [0,0]), level = -1)
		self.drawStack(envPos, rotation = 0, stackName = "environment")

		objData = self.getSortedObjects(objects)
		for obj in objData:
			self.drawStack(obj[1], obj = obj[2])

		self.renderWindow()
