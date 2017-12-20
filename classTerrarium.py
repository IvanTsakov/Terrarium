import random
from termcolor import colored
class Terrain():
	def __init__(self, x, y):
		self.x = x 
		self.y = y
		self.num_creatures = 2#input('Please enter how many creatures you\'d want: ')
		self.cells = []
		self.creatures = []
		self.create_cells()
		self.create_creatures()

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

	def generate_coords(self):
		list1 = []
		for item in self.generate_size_for_side(self.x):
			for value in self.generate_size_for_side(self.y):
				list1.append((item,value))
		return list1 # building a list for storing the coords of every cell in the Terrain, used for building a terrain_cords

	def has_animal_alive(self):	
		return any(c for c in self.creatures if c.alive)


	def create_creatures(self):
		if not self.cells:
			raise ValueError('No cells')
		if self.creatures:
			raise ValueError('Creatures already created')

		creature_classess = [Carnivore, Hernivore, Scavenger]
		for i in range(self.num_creatures):
			cell = random.choice(self.cells)
			beast = random.choice(creature_classess)(cell)
			self.creatures.append(beast)

	def create_cells(self): #method for the whole area of the game.
		if self.cells:
			raise ValueError('Cells already created')

		for x, y in self.generate_coords():
			cell = TerrainCell(x, y, self) 

	def get_surrounding_cells(self, x1, y1):
		surrounding_cords = []
		surrounding_cells = []
		for x2 in range(x1-1, x1+2):
			for y2 in range(y1-1, y1+2):
				if (x1 != x2 or y1 != y2) and (0 < x2 <= self.x) and (0 < y2 <= self.y):
					surrounding_cords.append((x2,y2))

		cell_map = {cell.coords: cell for cell in self.cells}

		for coords in surrounding_cords:
			surrounding_cells.append(cell_map[coords])
					
		return surrounding_cells


	def play(self, something):

		for c in self.creatures:
			if not c.alive:
				continue

			c.age += 1
 
			print colored('The cell we are currently in is >>> ', 'red'), c.cell
			print colored('Those are the creatures in the cell >>>>>', 'blue'), c.cell.creatures
			print colored('>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<', 'cyan')
			print colored("It\'s my turn ->", 'green'), c
			c.play()
			print
		


class TerrainCell(object):
	def __init__(self, x, y, terrain):
		self.x = x
		self.y = y
		self.creatures = []
		self.cell_type = random.choice(['Water', 'Grass', 'Mountain', 'Desert']) #gets random type.
		self.terrain = terrain
		self.terrain.cells.append(self)

	@property
	def coords(self):
		return (self.x, self.y)

	@property
	def is_water(self):
		return self.cell_type == 'Water'

	def __str__(self):
		return '[%s - %s]' % (self.coords, self.cell_type)

	def __repr__(self):
		return '[%s - %s]' % (self.coords, self.cell_type)


class Creatures(object):
	def __init__(self, type, cell):
		self.age = 0
		self.type = type
		self.status = 'alive' # status check
		self.hunger = random.randrange(3,8)  #stores hunger value -> from generate hunger
		self.cell = cell #shows the current animal cell 

	def __str__(self):
		return '[Type:%s]--[Hunger:%s]--[Status:%s] -- [Age: %s]'%(self.type, self.hunger, self.status, self.age)

	def __repr__(self):
		return '[Type:%s]--[Hunger:%s]--[Status:%s]--[Age: %s]'%(self.type, self.hunger, self.status, self.age)

	@property
	def cell(self):
		return self._cell

	@cell.setter
	def cell(self, value):
		prev_cell = getattr(self, '_cell', None)
		if prev_cell:
			prev_cell.creatures.remove(self)

		self._cell = value
		self._cell.creatures.append(self)

		if self._cell.is_water:
			self.status = 'dead'

	@property
	def hunger(self):
		return self._hunger

	@hunger.setter
	def hunger(self, value):
		if not self.alive:
			raise ValueError('I"m already dead')

		self._hunger = value
		if self._hunger <= 0:
			self.status = 'dead'

	@property
	def alive(self):
		return self.status == 'alive'

	@property
	def dead(self):
		return self.status == 'dead'

	@property
	def eaten(self):
		return self.status == 'eaten'

	def can_eat(self):
		raise NotImplemented('Hello darkness my old friend')

	def eat(self):
		self.hunger = self.hunger + random.randint(2,5)
		return self.hunger

	def play(self):
		self.hunger = self.hunger - 1

		if not self.alive:
			print "I'm %s i wont do anything" % self.status
			return

		if self.hunger < 5:
			if self.can_eat():
				self.eat()
				print colored((self, ' is really happy because it is fed now'),'red', 'on_white')
			else:
				self.move()
				print colored(('I moved to ->', self.cell),'blue', 'on_white')
		else:
			print colored('I am not hungry enough to do something', 'yellow', 'on_white')


	def move(self):
		moves = self.cell.terrain.get_surrounding_cells(self.cell.x, self.cell.y)
		self.cell = random.choice(moves)

class Carnivore(Creatures):
	def __init__(self, cell):
		super(Carnivore, self).__init__('Carnivore', cell)

	def __call__(self,cell):
		return self

	def search_food(self):
		try:
			c = next(c for c in self.cell.creatures if c.type == 'Hernivore' and c.alive)
			return c
		except StopIteration:
			return None

	def eat(self):
		food = self.search_food()
		if not food:
			raise ValueError('No food found')
		# call parent to increase the hunger
		super(Carnivore, self).eat()
		food.status = 'dead'

	def can_eat(self):
		food = self.search_food()
		if not food:
			return False
		return True

class Hernivore(Creatures):
	def __init__(self, cell):
		super(Hernivore, self).__init__('Hernivore', cell)

	def __call__(self):
		return self

	def can_eat(self):
		return self.cell.cell_type == 'Grass'


class Scavenger(Creatures):
	def __init__(self, cell):
		super(Scavenger, self).__init__('Scavenger', cell)

	def __call__(self,cell):
		return self

	def search_food(self):
		try:
			c = next(c for c in self.cell.creatures if c.dead)
			return c
		except StopIteration:
			return None

	def eat(self):
		food = self.search_food()

		if not food:
			raise ValueError('No food found')

		# call parent to increase the hunger
		super(Scavenger, self).eat()
		food.status = 'eaten'

	def can_eat(self):
		food = self.search_food()
		if not food:
			return False
		return True


def main():
	terrain = Terrain(5,5)
	day = 1
	while terrain.has_animal_alive() and day <= 20:
		print 'Today is day: ', day
		terrain.play(day)
		day += 1
	print colored('The game is over, feel free to play again','white', 'on_red')
if __name__ == main():
	main()