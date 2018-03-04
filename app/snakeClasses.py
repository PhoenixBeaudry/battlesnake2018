#Classes
########################################################################
class Board:


	def __init__(self):
		self.width = 0
		self.height = 0


	def __init__(self, data):

		self.height = data['height']
		self.width = data['width']
		self.board = [board[:] for board in [["0"] * self.width] * self.height]
		self.turn = data['turn']
		self.enemySnakes = []
		self.foodList = []

		self.selfsnake = Snake(data['you'])

		for snake in data['snakes']['data']:
			self.enemySnakes.append(Snake(snake))

		for food in data['food']['data']:
			self.foodList.append(Food(food))


		self.board[self.selfsnake.headpos.x][self.selfsnake.headpos.y] = "S"
		for bodypart in self.selfsnake.bodypos:
			self.board[bodypart.x][bodypart.y] = "s"


		for enemy in self.enemySnakes:
			self.board[enemy.headpos.x][enemy.headpos.y] = "E"
			for bodypart in enemy.bodypos:
				self.board[bodypart.x][bodypart.y] = "e"

		for food in self.foodList:
			self.board[food.pos.x][food.pos.y] = "F"





class Snake:

	def __init__(self):
		self.health = 100
		self.headpos = Vector()
		self.bodypos = []

	def __init__(self, snakeInfo):
		self.health = snakeInfo['health']
		self.headpos = Vector(snakeInfo['body']['data'][0])

		self.bodypos = []
		for point in snakeInfo['body']['data'][1:]:
			self.bodypos.append(Vector(point))

	def getPos():
		snakeParts = []
		snakeParts.append(self.headpos)
		for bodypart in bodypos:
			snakeParts.append(bodypart)
		return snakeParts


class Food:

	def __init__(self):
		self.pos = Vector()


	def __init__(self, foodInfo):
		self.pos = Vector(foodInfo)


class Vector:
	
	def __init__(self):
		self.x = -1
		self.y = -1


	def __init__(self, point):
		self.x = point['x']
		self.y = point['y']
