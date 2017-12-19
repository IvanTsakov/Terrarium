import random

class Terrain():
	def __init__(self, x, y):
		self.x = x 
		self.y = y
		self.num_creatures =2 #input('Please enter how many creatures you\'d want: ')
		self.cells = []
		self.creatures =[]

	def __str__(self):
		return '[%s:%s]' % (self.x, self.y)
	
	def __repr__(self):
		return '[%s:%s]' % (self.x, self.y)

	def __call__(self):
		return self

	def get_size(self):
		size = self.x * self.y 
		return size # get the size of the current field
	
	def generate_size_for_side(self, z):
		list1 = list(range(1, z+1))
		return list1 #get the coordinate system values for x and y ( z = x; z = y )

	def generate_cells(self):
		list1 = []
		for item in self.generate_size_for_side(self.x):
			for value in self.generate_size_for_side(self.y):
				list1.append((item,value))
		return list1 # building a list for storing the coords of every cell in the Terrain, used for building a terrain_list

	def has_animal_alive(self):
		if self.creatures != []:
			for i in self.creatures:
				if i.status == 'dead' or 'eaten':
					self.creatures.remove(i)
		else:
			print 'That is it, the game is over. All animals are dead'
			return 

	def get_creatures(self):
		list2 =[ ]
		for i in range(self.num_creatures):
			types = [Carnivore(1), Hernivore(2), Scavenger(3)]
			beast = random.choice(types)
			list2.append(beast)
		return list2

	def make_Terrain(self): #method for the whole area of the game.
		terrain_list = []
		terrain_list = self.generate_cells()

		creatures = []
		creatures_list = self.get_creatures()

		for i in creatures_list:
			i.cell = random.choice(terrain_list)
			self.creatures.append(i)
	
		for x, y in terrain_list:
			generated_cell = TerrainCell(x, y, self)  #coords = (self.x,self.y), Terrain = self)
			self.cells.append(generated_cell)
			for c in self.creatures:
				if c.cell == generated_cell.coords:
					c.cell = generated_cell
					generated_cell.creatures.append(c)
		return self.cells

	def get_surrounding_cells(self, x1, y1):
		surrounding_cells = []
		for x2 in range(x1-1, x1+2):
			for y2 in range(y1-1, y1+2):
				if (x1 != x2 or y1 != y2) and (0 < x2 <= self.x) and (0 < y2 <= self.y):
					surrounding_cells.append((x2,y2))
		for cell in self.cells:
			for i in surrounding_cells:
				if cell.coords == i:
					i == cell
					surrounding_cells.remove(i)
					surrounding_cells.append(cell)
		return surrounding_cells


	def play(self, something):

		for i in self.creatures:
			if i.status == 'alive':
				i.age += 1	
			else:
				print i.age 
			if i.cell.cell_type == 'Water':
				print i.cell
				print 'All animals here are dead, because this is a Water cell.'
				i.status = 'dead'
				continue
			print 'The cell we are currently in is: ', i.cell
			print 
			print 'It\'s my turn ->', i
			print i.play()
			print
		


class TerrainCell(object):
	def __init__(self, x, y, terrain):
		self.terrain = terrain
		self.cell_type = random.choice(['Water', 'Grass', 'Mountain', 'Desert']) #gets random type.
		self.x = x
		self.y = y
		self.creatures = []

	@property
	def coords(self):
		return (self.x,self.y)

	def __str__(self):
		return '[%s - %s - %s ]' % (self.coords, self.cell_type, self.creatures)

	def __repr__(self):
		return '[%s - %s]' % (self.coords, self.cell_type)


class Creatures:
	def __init__(self, cell):
		self.cell = cell #shows the current animal cell 
		self.hunger = random.randrange(3,8)  #stores hunger value -> from generate hunger
		self.status = 'alive' # status check
		self.age = 0
	def __str__(self):
		return '[Type:%s]--[Hunger:%s]--[Status:%s] -- [Age: %s]'%(self.type, self.hunger, self.status, self.age)

	def __repr__(self):
		return '[Type:%s]--[Hunger:%s]--[Status:%s]--[Age: %s]'%(self.type, self.hunger, self.status, self.age)

	def can_eat(self):
		raise NotImplemented('Hello darkness my old friend')

	def eat(self):
			self.hunger = self.hunger + random.randint(2,5)
			return self.hunger

	def play(self):
		if self.hunger <= 0 or self.status != 'alive':
			if self.status == 'eaten':
				return 'This creature has been eaten', self
			else:
				self.status = 'dead'
				return 'This creature is dead', self

		if self.hunger < 5:
			if self.can_eat():
				print self, ' is really happy because it is fed now'
				return 'It ate a lot and the new hunger is:', self.hunger
			else:
				print 'I moved to ->', self.move()
				self.cell.creatures.append(self)
				self.hunger = self.hunger - 1
				if self.hunger <= 0:
					self.status = 'dead'
					return 'whoops i died', self
				return self.cell
		else:
			print 'I am not hungry enough to do something'
			self.hunger = self.hunger - 1
			return 'My hunger is: ', self.hunger


	def move(self):
		self.cell.creatures.remove(self)
		moves = self.cell.terrain.get_surrounding_cells(self.cell.x, self.cell.y)
		self.cell = random.choice(moves)
		return self.cell

class Carnivore(Creatures):
	def __init__(self, cell):
		Creatures.__init__(self, cell)
		self.type = 'Carnivore'

	def __call__(self,cell):
		return self

	def can_eat(self):
		for i in self.cell.creatures:
			if self == i:
				continue
			else:
				if i.type == 'Hernivore' and i.status == 'alive':
					self.eat()
					i.status = 'eaten'
					return self.hunger
		return

class Hernivore(Creatures):
	def __init__(self, cell):
		Creatures.__init__(self, cell)
		self.type = 'Hernivore'

	def __call__(self):
		return self

	def can_eat(self):
		if self.cell.cell_type == 'Grass':
			return self.eat()



class Scavenger(Creatures):
	def __init__(self, cell):
		Creatures.__init__(self, cell)	
		self.type = 'Scavenger'

	def __call__(self,cell):
		return self

	def can_eat(self):
		for i in self.cell.creatures:
			if self == i:
				continue
			else:
				if i.status == 'dead':
					self.eat()
					i.status = 'eaten'
					return self.hunger
		return


def main():
	terrain = Terrain(1,2)
	terrain.make_Terrain()

	day = 1
	while day <=2 or terrain.has_animal_alive():
		print 'Today is day: ', day
		terrain.play(day)
		day += 1

if __name__ == main():
	main()