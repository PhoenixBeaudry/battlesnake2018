class Board:
	board = [board[:] for board in [[0] * board_width] * board_height]
	turn = 0

	def __init__(data):
		#SelfSnake
		board[data['you']['body']['data'][0]['x']][['data']['you']['body']['data'][0]['y']] = "S"
		for point in ['data']['you']['body']['data'][1:]:
			board[point['x']][point['y']] = "s"



		#Enemy Snakes
		for snake in enemy_snakes:
			board[snake["body"]["data"][0]["x"]][snake["body"]["data"][0]["y"]] = "E"
		for point in snake["body"]["data"][1:]:
			board[point["x"]][point["y"]] = "e"

		#Food
		for food in food_locations["data"]:
			board[food["x"]][food["y"]] = "F"
			
		#Return board
		return board




class Snake:

	def __init__(snakeInfo):
		health = snakeInfo['health']
		head = Vector(snakeInfo['body']['data'][0])

		body = []
		for point in snakeInfo['body']['data'][1:]:
			body.append(Vector(point))


class Food:
	def __init__(foodInfo):
		foodList = []

		for food in foodInfo["data"]:
			foodList.append(Vector(food))



class Vector:
	x = -1
	y = -1
	def __init__(point):
		x = point['x']
		y = point['y']


