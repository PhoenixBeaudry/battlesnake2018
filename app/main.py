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

	# complex data:
	self_snake = data['you'] #snake object
	enemy_snakes = data['snakes'] #list of snake objects
	food_locations = data['food'] #list of coordinates

	# integers:
	board_height = data['height']
	board_width = data['width']
	turn_number = data['turn']

	#create board with data
	board = boardInit(data)

	#Snake Logic:

	#possible directions
	directions = ['up', 'down', 'left', 'right']

	#current snake head location [x,y]
	cur_loc=[self_snake[body][data][0]["x"], self_snake[body][data][0]["y"]]

	#step 1: remove possible directions which will certainly result in immediate death
	for each in directions:
		valid=checkMove(each, cur_loc, board_width, board_height)
		if not valid:
			directions.remove(each)

	#step 2: if there is more than one valid move, apply advanced behaviour
	#to narrow down the options
	if(len(directions)>1):
		dosomestuff()
	
	return{
		'move': random.choice(directions),
		'taunt': 'battlesnake-python!'
	}

############################### Functions

####higher-order behaviour

def dosomestuff():
	return



####basic functions

#BOARDINIT
#Initialize 2d gameboard array
#Enemy Heads: "E", Body: "e". Self Head: "S", Body: "s". Food: "F". Null: "0"
def boardInit(data):
    self_snake = data['you'] #snake object
    enemy_snakes = data['snakes'] #list of snake objects
    food_locations = data['food'] #list of coordinates
    board_height = data['height']
    board_width = data['width']

    #Init Board
    board = []
    for i in range(board_width):
        board.append([])
    for i in range(10):
        for j in range(board_height):
            board[i].append(0)

    #SelfSnake
    board[self_snake["body"]["data"][0]["x"]][self_snake["body"]["data"][0]["y"]] = "S"
    for point in self_snake["body"]["data"][1:]:
        board[point["x"]][point["y"]] = "s"


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

#CLOSESTFOOD
#takes the location of our snake head and a list of food coordinates
#and returns the location [x,y] of the closest food particle
def closestFood(head, food_locations):
	min_dist=0
	best=head
	for food in food_locations:
		delta_x=head[0]-food["x"]
		delta_y=head[1]-food["y"]
		distance=abs(delta_x)+abs(delta_y)
		if(min_dist==0 or distance<min_dist):
			min_dist=distance
			best=[food["x"], food["y"]]
	return best

#CHECKMOVE
#returns true if the move will not result in immediate death
#otherwise, returns false
def checkMove(possible_move, current_location, board_width, board_height):
	w=avoidWall(possible_move, current_location, board_width, board_height)
	e=avoid(array, possible_move, current_location, [E,e]) #avoid enemies
	s=avoid(array, possible_move, current_location, [S,s]) #avoid self
	if(s and w and e):
		return true
	return false

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
	for each in types:
		if(array[location[0],location[1]]==each):
			return true
	return false

#DEST
#returns the coordinate that would be moved to
#if the move was submitted
def dest(move, current_location):
	result={
		'up': lambda x,y: [x,y-1]
		'down': lambda x,y: [x,y+1]
		'left': lambda x,y: [x-1,y]
		'right': lambda x,y: [x+1,y]
	}[move](current_location)
	return result

#returns false if the proposed move places us on a board wall
def avoidWall(possible_move, current_location, board_width, board_height):
    destination = dest(possible_move, current_location)
    if(destination[0] < 0 or destination[0] > board_width):
        return False
    if(destination[1] < 0 or destination[1] > board_height):
        return False
    return True

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
