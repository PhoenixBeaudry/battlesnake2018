import bottle
import os
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )


    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    #Reading in game-state information.
    self_snake = data['you']
    enemy_snakes = data['snakes']
    food_locations = data['food']
    board_height = data['height']
    board_width = data['width']

    #################################

    #Snake Logic will end up going here.





    directions = ['up', 'down', 'left', 'right']

    return {
        'move': random.choice(directions),
        'taunt': 'battlesnake-python!'
    }




############################### Functions

def closestFood(self_snake, food_locations):
    minDistance = 0
    for food in food_locations:
        if(self_snake[body][data][0]["x"]-food["x"] > minDistance):
            minDistance = self_snake[body][data]["x"]-food["x"]

    return minDistance

#CHECKMOVE
#returns true if the move will not result in immediate death
#otherwise, returns false
'''
def checkMove(possible_move):
	w=avoidWall(possible_move)
	s=avoid(array, possible_move, current_location, [E,e])
	e=avoid(array, possible_move, current_location, [S,s])
	if(s and w and e):
		return true
	return false

'''

#AVOID
#takes a move as input (up,down,left,right) and checks
#to see if it will result in a collision with something specified in [types]
#which is ***already there*** (important)
#returns true if the move is safe, false otherwise
def avoid(array, move, current_location, types):
	destination=dest(move, current_location)
	result=not checkArray(array, destination, types)
	return result

#CHECKARRAY
#looks at the index specified by location and returns
#true if it contains anything in [types], false otherwise
def checkArray(array, location, types):
	for(each in types):
		if(array[location[0],location[1]]==each):
			return true
	return false
	
#DEST
#returns the coordinate that would be moved to
#if the move was submitted	
def dest(move, current_location):
	result={
		'up': lambda [x,y]: [x,y+1]
		'down': lambda [x,y]: [x,y-1]
		'left': lambda [x,y]: [x-1,y]
		'right': lambda [x,y]: [x+1,y]
	}[move](current_location)
	return result


def avoidWall(possible_move):
    if(possible_move == "up"):
        return missWallUp(self_snake, board_height, board_width)
    if(possible_move == "left"):
        return missWallLeft(self_snake, board_height, board_width)
    if(possible_move == "right"):
        return missWallRight(self_snake, board_height, board_width)
    if(possible_move == "down"):
        return missWallDown(self_snake, board_height, board_width)

def missWallUp(self_snake, board_height, board_width):
    if(self_snake[body][data][0]["y"] == 0):
        return false
    return true
def missWallLeft(self_snake, board_height, board_width):
    if(self_snake[body][data][0]["x"] == 0):
        return false
    return true
def missWallRight(self_snake, board_height, board_width):
    if(self_snake[body][data][0]["x"] == board_width):
        return false
    return true
def missWallDown(self_snake, board_height, board_width):
    if(self_snake[body][data][0]["y"] == board_width):
        return false
    return true



# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
