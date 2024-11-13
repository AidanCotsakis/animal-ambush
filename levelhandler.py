import pygame

from settings import *

# returns if the given position is above 0 (is ground)
def isGround(level, pos):
	if pos[0] >= 0 and pos[1] > 0 and pos[0] < len(level) and pos[1] < len(level) and level[pos[1]][pos[0]] > 0:
		return True
	return False

# returns true if the given position is a corner (NEEDS IMPROVEMENT)
def isCorner(level, pos):
	numTouch = numTouching(level, pos)
	numSurr = numSurrounding(level, pos)
	if (numSurrounding(level, pos) > 0
		and (numTouch == 3
			or numTouch == 0
			or numTouch == 4
			or (numTouch == 2
				and isGround(level,(pos[0]+1,pos[1])) != isGround(level,(pos[0]-1,pos[1]))
				)
			or (numTouch == 1 
				and (numSurr == 4
					or numSurr == 5)
				)
			)
		):
		return True
	return False

# returns the number of the 8 surrounding tiles that are above 0 (is ground) and 0 if pos is gound 
def numSurrounding(level, pos):
	if isGround(level, pos):
		return 0
	count = 0
	for i in range(-1,2):
		for j in range(-1,2):
			if (i != 0 or j != 0) and isGround(level, (pos[0] + i, pos[1] + j)):
				count += 1
	return count

# returns the number of the 4 adjacent tiles that are above 0 (is ground) and 0 if pos is gound 
def numTouching(level, pos):
	if isGround(level, pos):
		return 0
	count = 0
	for i in [-1,1]:
		if isGround(level, (pos[0] + i, pos[1])):
			count += 1
	for j in [-1,1]:
		if isGround(level, (pos[0], pos[1]+j)):
			count += 1
	return count

# generates the sprite stack image for a given level and replaces "spritestacks/environment.png"
def generateLevelStack(level):
	levelSide = len(level)
	layerSide = levelSide*LEVEL_TILE_SIZE
	surfSize = (layerSide, layerSide*LEVEL_STACK_HEIGHT)

	surf = pygame.Surface(surfSize, pygame.SRCALPHA, 32)
	surf = surf.convert_alpha()

	# draw one tile at a time
	for x in range(levelSide):
		for y in range(levelSide):
			pos = (x, y)

			# determines the colour of ground if this is a ground tile
			shade = (x+y)%2
			if shade == 0:
				tileColour = LEVEL_GROUND_COLOUR0
			else:
				tileColour = LEVEL_GROUND_COLOUR1

			# handle drawing the boarder
			if not isGround(level, pos) and numSurrounding(level, pos) >= 1:
				# draw the solid parts of the boarder for given levels
				pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE, LEVEL_TILE_SIZE, LEVEL_TILE_SIZE), 2) # draw top layer solid bit
				pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide, LEVEL_TILE_SIZE, LEVEL_TILE_SIZE)) # draw second layer solid bit
				pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide*(LEVEL_STACK_HEIGHT-1), LEVEL_TILE_SIZE, LEVEL_TILE_SIZE)) #draw last layer solid bit
				pygame.draw.rect(surf, LEVEL_BORDER_COLOUR1, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE+2+layerSide, LEVEL_TILE_SIZE-4, LEVEL_TILE_SIZE-4))
				pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE+3, y*LEVEL_TILE_SIZE+3, 2, 2)) # draw top layer solid bit

				# carve top layer and add shade to second layer based on weather or not the adjacent tiles are walls
				if numSurrounding(level, (x+1, y)) > 0 and (not isGround(level, (x+2,y)) or isCorner(level, (x+1, y))):
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+6, y*LEVEL_TILE_SIZE+2, 2, 1))
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+6, y*LEVEL_TILE_SIZE+5, 2, 1))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE+3, y*LEVEL_TILE_SIZE+3, 3, 2))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR1, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE+2+layerSide, LEVEL_TILE_SIZE-2, LEVEL_TILE_SIZE-4))
				if numSurrounding(level, (x-1, y)) > 0 and (not isGround(level, (x-2,y)) or isCorner(level, (x-1, y))):
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+2, 2, 1))
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+5, 2, 1))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE+3, 3, 2))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR1, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+2+layerSide, LEVEL_TILE_SIZE-2, LEVEL_TILE_SIZE-4))
				if numSurrounding(level, (x, y+1)) > 0 and (not isGround(level, (x,y+2)) or isCorner(level, (x, y+1))):
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+5, y*LEVEL_TILE_SIZE+6, 1, 2))
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE+6, 1, 2))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE+3, y*LEVEL_TILE_SIZE+3, 2, 3))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR1, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE+2+layerSide, LEVEL_TILE_SIZE-4, LEVEL_TILE_SIZE-2))
				if numSurrounding(level, (x, y-1)) > 0 and (not isGround(level, (x,y-2)) or isCorner(level, (x, y-1))):
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+5, y*LEVEL_TILE_SIZE, 1, 2))
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE, 1, 2))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE+3, y*LEVEL_TILE_SIZE+2, 2, 3))
					pygame.draw.rect(surf, LEVEL_BORDER_COLOUR1, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE+layerSide, LEVEL_TILE_SIZE-4, LEVEL_TILE_SIZE-2))
				
				# draw indented "ground" side if only touching one ground tile based on what direction said tile is in (does this for all layers this applies to) 
				if numTouching(level, pos) == 1:
					for i in range(1, LEVEL_STACK_HEIGHT-1):
						if isGround(level, (x+1, y)) and numSurrounding(level, (x-1, y)) <= 0:
							pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide*i, 1, LEVEL_TILE_SIZE))
							pygame.draw.rect(surf, tileColour, (x*LEVEL_TILE_SIZE+1, y*LEVEL_TILE_SIZE+layerSide*i, 1, LEVEL_TILE_SIZE))
						if isGround(level, (x-1, y)) and numSurrounding(level, (x+1, y)) <= 0:
							pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+7, y*LEVEL_TILE_SIZE+layerSide*i, 1, LEVEL_TILE_SIZE))
							pygame.draw.rect(surf, tileColour, (x*LEVEL_TILE_SIZE+6, y*LEVEL_TILE_SIZE+layerSide*i, 1, LEVEL_TILE_SIZE))
						if isGround(level, (x, y+1)) and numSurrounding(level, (x, y-1)) <= 0:
							pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide*i, LEVEL_TILE_SIZE, 1))
							pygame.draw.rect(surf, tileColour, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide*i+1, LEVEL_TILE_SIZE, 1))
						if isGround(level, (x, y-1)) and numSurrounding(level, (x, y+1)) <= 0:
							pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide*i+7, LEVEL_TILE_SIZE, 1))
							pygame.draw.rect(surf, tileColour, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide*i+6, LEVEL_TILE_SIZE, 1))
				# draw in pillars on all valid layers if this is a corner tile
				else:
					for i in range(2, LEVEL_STACK_HEIGHT-1):
						pygame.draw.rect(surf, LEVEL_BORDER_COLOUR0, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide*i, LEVEL_TILE_SIZE, LEVEL_TILE_SIZE))
						

			# handle drawing the ground
			if isGround(level, pos):
				pygame.draw.rect(surf, tileColour, (x*LEVEL_TILE_SIZE, y*LEVEL_TILE_SIZE+layerSide, LEVEL_TILE_SIZE, LEVEL_TILE_SIZE))

	# pass through each tile again to carve grooves in the top layer at each corner
	for x in range(levelSide):
		for y in range(levelSide):
			pos = (x, y)
			if not isGround(level, pos) and numSurrounding(level, pos) >= 1 and isCorner(level, pos):
				numTouch = numTouching(level, pos)
				if numTouch == 4:
					pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+2, y*LEVEL_TILE_SIZE+2, LEVEL_TILE_SIZE-4, LEVEL_TILE_SIZE-4), 1)
				elif numTouch == 2 or numTouch == 0:
					if numSurrounding(level, (x+1, y)) > 0 and (not isGround(level, (x+2,y)) or isCorner(level, (x+1, y))):
						pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+7+LEVEL_GROOVE_DISTANCE, y*LEVEL_TILE_SIZE+3, 1, 2))
					if numSurrounding(level, (x-1, y)) > 0 and (not isGround(level, (x-2,y)) or isCorner(level, (x-1, y))):
						pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE-LEVEL_GROOVE_DISTANCE, y*LEVEL_TILE_SIZE+3, 1, 2))
					if numSurrounding(level, (x, y+1)) > 0 and (not isGround(level, (x,y+2)) or isCorner(level, (x, y+1))):
						pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+3, y*LEVEL_TILE_SIZE+7+LEVEL_GROOVE_DISTANCE, 2, 1))
					if numSurrounding(level, (x, y-1)) > 0 and (not isGround(level, (x,y-2)) or isCorner(level, (x, y-1))):
						pygame.draw.rect(surf, LEVEL_ALPHA, (x*LEVEL_TILE_SIZE+3, y*LEVEL_TILE_SIZE-LEVEL_GROOVE_DISTANCE, 2, 1))

	# save image to the sprite stacks folder
	pygame.image.save(surf, f"{STACK_FILENAME}/environment.png")
	return surf

if __name__ == "__main__":
	from spritestack import getRotationArray

	pygame.init()
	window = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)

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

	# level = [
	# [0,0,0,0,0,0,0,0,0,0,0,0,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],	
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,1,1,1,1,1,1,1,1,1,1,1,0],
	# [0,0,0,0,0,0,0,0,0,0,0,0,0]]

	surf = generateLevelStack(level)
	img = pygame.image.load(f"{STACK_FILENAME}/environment.png").convert_alpha()
	print(surf)
	print(img)
	getRotationArray(surf, imageName = "environment")
