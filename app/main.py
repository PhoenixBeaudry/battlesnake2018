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
def checkMove(possible_move):
	s=avoidSelf()
	w=avoidWall()
	e=avoidEnemy()
	if(s and w and e):
		return true
	return false




def nearWall(self_snake, board_height, board_width):
    if(self_snake[body][data][0]["x"] == board_width):
        if(self_snake[body][data][0]["y"] == board_height):
            # return right and bottom
        if(self_snake[body][data][0]["y"] == 0):
            # return right and top
        # return right
    if(self_snake[body][data][0]["x"] == 0):
        if(self_snake[body][data][0]["y"] == board_height):
            # return left and bottom
        if(self_snake[body][data][0]["y"] == 0):
            # return left and top
        # return left
    if(self_snake[body][data][0]["y"] == 0):
        if(self_snake[body][data][0]["x"] == board_width):
            # return top and right
        if(self_snake[body][data][0]["x"] == 0):
            # return top and left
        # return top
    if(self_snake[body][data][0]["y"] == board_width):
        if(self_snake[body][data][0]["x"] == board_width):
            # return bottom and right
        if(self_snake[body][data][0]["x"] == 0):
            # return bottom and left
        # return bottom


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
