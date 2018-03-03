#Classes
########################################################################
class Board:


	def __init__(self, data):

		self.height = data['height']
		self.width = data['width']
		self.board = [board[:] for board in [[0] * width] * height]
		self.turn = data['turn']
		self.enemySnakes = []
		self.foodList = []

		self.selfsnake = Snake(data['you'])

		for snake in data['snakes']['data']:
			enemySnakes.append(Snake(snake))

		for food in data['food']['data']:
			foodList.append(Food(food))


		board[selfsnake.headpos.x][selfsnake.headpos.y] = "S"
		for bodypart in selfsnake.bodypos:
			board[bodypart.x][bodypart.y] = "s"


		for enemy in enemySnakes:
			board[enemy.headpos.x][enemy.headpos.y] = "E"
			for bodypart in enemy.bodypos:
				board[bodypart.x][bodypart.y] = "e"

		for food in foodList:
			board[food.pos.x][food.pos.y] = "F"


		return board




class Snake:

	def __init__(self):
		self.health = 100
		self.headpos = Vector()
		self.bodypos = [];

	def __init__(self, snakeInfo):
		self.health = snakeInfo['health']
		self.headpos = Vector(snakeInfo['body']['data'][0])

		self.bodypos = []
		for point in snakeInfo['body']['data'][1:]:
			bodypos.append(Vector(point))

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