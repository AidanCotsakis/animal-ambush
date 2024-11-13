import math

from settings import *

class HighlightBox():
	def __init__(self, parent, pos, level = 0):
		self.type = "highlightBox"
		self.parent = parent # must be a troop object
		self.pos = pos # position on the grid in tile coordinates, with [0,0] being the middle tile
		self.level = level

		self.rotation = 0
		self.angularAcceleration = 1

		self.priority = 40

		self.selectable = True
		self.selected = False
		self.hoverable = True
		self.drawOffset = [0,0,0] #x,y,z in world coordinates
		self.mouseHover = False
		self.hoverTick = -1
		self.deleteAnimationTick = 0
		self.delete = False
		self.deleteAnimation = False

	# called once upon being selected
	def onSelect(self, objects, level):
		self.selected = True
		self.deleteAnimation = True
		self.selectable = False

		parentDistance = [self.parent.pos[0]-self.pos[0], self.parent.pos[1]-self.pos[1]]
		self.parent.drawOffset = [parentDistance[0]*LEVEL_TILE_SIZE*STACK_SCALE_FACTOR, parentDistance[1]*LEVEL_TILE_SIZE*STACK_SCALE_FACTOR, self.parent.drawOffset[2]]
		self.parent.movementSpeed = [abs(self.parent.drawOffset[0]/TROOP_MOVEMENT_FRAMES), abs(self.parent.drawOffset[1]/TROOP_MOVEMENT_FRAMES)]

		self.parent.rotation = math.degrees(math.atan2(parentDistance[0], parentDistance[1]))+90

		self.parent.pos = self.pos

		# kill opposing troop on own tile
		for obj in objects:
			if obj.type == "troop" and obj.team != self.parent.team and obj.pos == self.pos:
				obj.delete = True

	# called per tick
	def tick(self):
		if not self.parent.selected or self.deleteAnimation:
			self.deleteAnimationTick += 1
			if self.selected:
				self.angularAcceleration *= 1.15
			else:
				self.delete = True
			
			if self.deleteAnimationTick == 30:
				self.delete = True

		self.rotation += self.angularAcceleration