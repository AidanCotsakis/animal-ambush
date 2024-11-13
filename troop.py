import math

from settings import *
from highlightbox import HighlightBox

def isGround(level, pos):
	pos = [pos[0] + int(len(level)/2), pos[1] + int(len(level)/2)]
	if pos[0] >= 0 and pos[1] > 0 and pos[0] < len(level) and pos[1] < len(level) and level[pos[1]][pos[0]] > 0:
		return True
	return False

class Troop():
	def __init__(self, team, rank, pos, rotation, level = 0):
		self.type = "troop"
		self.team = team # one of ["chicken", "pig", "cow", "cat"]
		self.rank = rank # one of ["none", "king", "build", "farm", "army"]
		self.pos = pos # position on the grid in tile coordinates, with [0,0] being the middle tile
		self.rotation = rotation # facing direction, with 0 being east
		self.level = level

		self.directions = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,-1],[-1,1],[1,-1]]

		self.priority = 50

		self.movementSpeed = [0,0]

		self.selectable = True
		self.drawOffset = [0,0,0] #x,y,z in world coordinates
		self.selected = False
		self.hoverTick = -1
		self.delete = False

	# called once upon being selected
	def onSelect(self, objects, level):
		self.hoverTick = 0
		self.selected = True

		invalidPostions = []
		for obj in objects:
			if obj.type == "troop" and obj.team == self.team:
				invalidPostions.append(obj.pos)

		# spawn selection boxes
		for i in self.directions:
			pos = [self.pos[0] + i[0], self.pos[1] + i[1]]
			if isGround(level, pos) and pos not in invalidPostions:
				objects.append(HighlightBox(self, pos))


	# gradually moves draw offset to 0 based on TROOP_MOVEMENT_SPEED
	def fixDrawOffset(self):
		if self.drawOffset[0] < 0 and self.drawOffset[0] + self.movementSpeed[0] < 0:
			self.drawOffset[0] += self.movementSpeed[0]
		elif self.drawOffset[0] > 0 and self.drawOffset[0] - self.movementSpeed[0] > 0:
			self.drawOffset[0] -= self.movementSpeed[0]
		else:
			self.drawOffset[0] = 0

		if self.drawOffset[1] < 0 and self.drawOffset[1] + self.movementSpeed[1] < 0:
			self.drawOffset[1] += self.movementSpeed[1]
		elif self.drawOffset[1] > 0 and self.drawOffset[1] - self.movementSpeed[1] > 0:
			self.drawOffset[1] -= self.movementSpeed[1]
		else:
			self.drawOffset[1] = 0


	# called per tick
	def tick(self):
		
		if self.drawOffset[0] != 0 or self.drawOffset[1] != 0:
			self.fixDrawOffset()

		# move the troop up and down if selected
		if self.selected:
			self.drawOffset[2] = -(math.sin(math.radians(self.hoverTick*OBJECT_HOVER_SPEED-90))+1)*OBJECT_HOVER_HEIGHT
			self.hoverTick += 1
		elif self.hoverTick != 0:
			if self.drawOffset[2] < -OBJECT_HOVER_THRESHOLD:
				self.drawOffset[2] = -(math.sin(math.radians(self.hoverTick*10-90))+1)*10
				self.hoverTick += 1
			else:
				self.drawOffset[2] = 0
				self.hoverTick = 0