import pygame
import math
import os

from settings import *

# slices a verticle stack of images into a list of individual images, assumes the slices are square, returns a list of images
def sliceLayers(source):
	sourceWidth = source.get_width()
	sourceHeight = source.get_height()

	numImages = int(sourceHeight/sourceWidth)

	# get each subsurface
	layers = []
	for i in range(numImages-1, -1, -1):
		layers.append(source.subsurface(pygame.Rect((0, sourceWidth*i), (sourceWidth, sourceWidth))))

	return layers

# renders a sprite stack at a given rotation, input is a sprite sheet with square tiles, output is a rendered surface
def buildStack(source, rotation, status = {"numCompleted" : 0, "total" : 1}, scale = STACK_SCALE_FACTOR, layerGap = STACK_LAYER_GAP, initialRotation = STACK_INITIAL_ROTATION, imageName = ""):
	# calculate scale
	layers = sliceLayers(source)
	spriteSize = source.get_width()*scale
	spriteMaxRotatedSize = math.ceil(math.sqrt(2)*spriteSize)
	surfSize = (spriteMaxRotatedSize, spriteMaxRotatedSize + math.ceil(layerGap*len(layers)))
	anchorPoint = (int(spriteMaxRotatedSize/2), surfSize[1]-math.ceil(spriteMaxRotatedSize/2))

	# create surface
	surf = pygame.Surface(surfSize, pygame.SRCALPHA, 32)
	surf = surf.convert_alpha()

	# render images onto surface
	yOffset = 0
	for layer in layers:
		scaled = pygame.transform.scale_by(layer, scale)
		rotated = pygame.transform.rotate(scaled, rotation+initialRotation)

		w = rotated.get_width()
		h = rotated.get_height()

		# fill the layer gap with multiple copies of the sprite to fill space
		for i in range(int(layerGap+1)):
			surf.blit(rotated, [anchorPoint[0]-int(w/2), anchorPoint[1]-int(h/2)-int(yOffset)-i])

		yOffset += layerGap
		status["numCompleted"] += source.get_width()*source.get_width()

	if STACK_CACHE_ENABLED:
		pygame.image.save(surf, f"{STACK_CACHE_FILENAME}/{imageName}{rotation}.png")

	return surf

# given a pygame image of stacked layers and a degreeGap, outputs a list of 360/degreeGap rendered sprite stacks 
def getRotationArray(source, status = {"numCompleted" : 0, "total" : 1}, degreeGap = STACK_DEGREE_GAP, imageName = ""):
	degree = 0

	sprites = []
	while degree < 360:
		sprites.append(buildStack(source, degree, status, imageName = imageName))
		degree += degreeGap

	return sprites

# returns a dictionary where the key is the stack filename and the value is a list of various rotated sprite stacks
def generateSpriteDict(imgDict, status = {"numCompleted" : 0, "total" : 1}):
	imageNames = [imageName[:-4] for imageName in os.listdir(STACK_FILENAME) if imageName.endswith(".png")]

	images = {}
	for imageName in imageNames:
		image = pygame.image.load(f"{STACK_FILENAME}/{imageName}.png").convert_alpha()
		images[imageName] = image

		status["total"] += image.get_width()*image.get_height()*int(360/STACK_DEGREE_GAP)

	for imageName in imageNames:
		imgDict[imageName] = getRotationArray(images[imageName], status, imageName = imageName)

def loadSpriteDict(imgDict, status = {"numCompleted" : 0, "total" : 1}, degreeGap = STACK_DEGREE_GAP):
	imageNames = [imageName[:-4] for imageName in os.listdir(STACK_FILENAME) if imageName.endswith(".png")]

	for imageName in imageNames:
		image = pygame.image.load(f"{STACK_CACHE_FILENAME}/{imageName}0.png")
		status["total"] += image.get_width()*image.get_height()*int(360/STACK_DEGREE_GAP)

	for imageName in imageNames:
		degree = 0
		sprites = []
		while degree < 360:
			surf = pygame.image.load(f"{STACK_CACHE_FILENAME}/{imageName}{degree}.png").convert_alpha()
			sprites.append(surf)
			degree += degreeGap
			status["numCompleted"] += surf.get_width()*surf.get_height()
		imgDict[imageName] = sprites

def getSpriteDict(imgDict, status = {"numCompleted" : 0, "total" : 1}):
	if os.path.exists(STACK_CACHE_FILENAME) and STACK_CACHE_ENABLED:
		loadSpriteDict(imgDict, status)
	else:
		if STACK_CACHE_ENABLED:
			os.makedirs(STACK_CACHE_FILENAME)
		generateSpriteDict(imgDict, status)

