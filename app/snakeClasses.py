#Classes
########################################################################
class Board:


	def __init__(self, data):

		height = data['height']
		width = data['width']
		board = [board[:] for board in [[0] * width] * height]
		turn = data['turn']
		enemySnakes = []
		foodList = []

		selfsnake = Snake(data['you'])

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
	headpos = Vector()
	bodypos = []

	def __init__(self, snakeInfo):
		health = snakeInfo['health']
		headpos = Vector(snakeInfo['body']['data'][0])

		bodypos = []
		for point in snakeInfo['body']['data'][1:]:
			bodypos.append(Vector(point))


class Food:
	pos = Vector()
	def __init__(self, foodInfo):
		pos = Vector(foodInfo)


class Vector:
	x = -1
	y = -1
	def __init__(self, point):
		x = point['x']
		y = point['y']