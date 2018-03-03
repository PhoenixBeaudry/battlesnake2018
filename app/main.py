import bottle
import os
import random
import snakeClasses


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
        'color': '#bab5a9',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():

	data = bottle.request.json
	gamestate=Board(data)

	#Snake Logic:

	#possible directions
	directions = ['up', 'down', 'left', 'right']

	#current snake head location [x,y]
	cur_loc=gamestate.selfsnake.headpos

	#step 1: remove possible directions which will certainly result in immediate death
	for each in directions:
		valid=checkMove(each, cur_loc, board_width, board_height, gamestate)
		if not valid:
			directions.remove(each)

	#step 2: if there is more than one valid move, apply advanced behaviour
	#to narrow down the options
	if(len(directions)>1):
		dosomestuff()

	return{
		'move': random.choice(directions),
		'taunt': "testHeadX"
	}

############################### Functions

####higher-order behaviour

def dosomestuff():
	return

	
	
	

#CLOSESTFOOD
#takes the location of our snake head and a list of food coordinates
#and returns the location [x,y] of the closest food particle
def closestFood(head, food_locations):
	min_dist=0
	best=head
	for food in food_locations:
		thisfood=[food["x"],food["y"]]
		distance=findDist(head, thisfood)
		if(min_dist==0 or distance<min_dist):
			min_dist=distance
			best=[food["x"], food["y"]]
	return best
	
#FINDDIST
#takes two points and returns the distance to travel between them
def findDist(a, b):
	dx=abs(a[0]-b[0])
	dy=abs(a[1]-b[1])
	return dx+dy

####basic functions
	
#CHECKMOVE
#returns true if the move will not result in immediate death
#otherwise, returns false
def checkMove(possible_move, current_location, board_width, board_height, gamestate):
	w=avoidWall(possible_move, current_location, board_width, board_height)
	#w=True
	e=True
	s=True
	#e=avoid(board, possible_move, current_location, [E,e]) #avoid enemies
	#s=avoid(board, possible_move, current_location, [S,s]) #avoid self
	if(s and w and e):
		return True
	return False

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
			return True
	return False

#DEST
#returns the coordinate that would be moved to
#if the move was submitted
def dest(move, current_location):
	result={
		'up': lambda x,y: [x,y-1],
		'down': lambda x,y: [x,y+1],
		'left': lambda x,y: [x-1,y],
		'right': lambda x,y: [x+1,y]
	}[move](current_location)
	return result

#returns false if the proposed move places us on a board wall
def avoidWall(possible_move, current_location, board_width, board_height):
	'''destination = dest(possible_move, current_location)
	wallBuffer = 0
	if(destination[0] < 0 + wallBuffer or destination[0] > board_width - wallBuffer):
		return False
	if(destination[1] < 0 + wallBuffer or destination[1] > board_height - wallBuffer):
		return False'''
	return True

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
