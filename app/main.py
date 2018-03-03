import bottle
import os
import random
from snakeClasses import *

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
	gamestate = Board(data)

	#Snake Logic:

	#possible directions
	directions = ['up', 'down', 'left', 'right']

	#step 1: remove possible directions which will certainly result in immediate death
	'''
	for each in directions:
		valid=checkMove(each, gamestate)
		if not valid:
			directions.remove(each)
	'''

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

#FOODREGION
#takes a snake (typically ours) and a food particle (typically nearest)
#and returns the region bordering both the food and our snake
def foodRegion(snake, foodlocation):
	particles=snake.getPos()
	particles=particles.append(foodlocation)
	return findRegion(particles)
		
#DANGERZONE
#returns the # of enemy snakes inside the region defined by findRegion
def dangerZone(snake, esnakes, fn):
	count=0
	snakereg=fn(snake)
	for each in esnakes:
		enemyreg=findRegion(each)
		overlap=regionOverlap(snakereg, enemyreg)
		if overlap:
			count++
	return count

#REGIONOVERLAP
#determins whether two input regions overlap, returns true if so
def regionOverlap(a, b):
	if b[0]>a[1] or b[1]<a[0] or b[2]>a[3] or b[3]<a[2]:
		return False
	return True
	
#takes a snake and returns the smallest box-shaped region
#that inludes it
def findRegion(snake):
	minx=findLeftBorder(snake)
	maxx=findRightBorder(snake)
	miny=findTopBorder(snake)
	maxy=findBottomBorder(snake)
	return [minx, maxx, miny, maxy]

#####
#HELPER FUNCTIONS FOR FINDREGION METHOD
def findLeftBorder(snake):
	segments=snake.getPos()
	minx=snake.headPos.x
	for segment in segments:
		if segment.x<minx:
			minx=segment.x
	return minx
	
def findRightBorder(snake):
	segments=snake.getPos()
	maxx=snake.headPos.x
	for segment in segments:
		if segment.x>maxx:
			maxx=segment.x
	return maxx
	
def findTopBorder(snake):
	segments=snake.getPos()
	miny=snake.headPos.y
	for segment in segments:
		if segment.y<miny:
			miny=segment.y
	return miny
	
def findBottomBorder(snake):
	segments=snake.getPos()
	maxy=snake.headPos.y
	for segment in segments:
		if segment.y>maxy:
			maxx=segment.y
	return maxy
#####

#DIRTOTARGET
#takes current location and a target and returns a subset of directions[]
#which bring it closer to the target
def dirToTarget(head, target, directions):
	options=[]
	for each in directions:
		distfromcurr=findDist(head, target)
		destination=dest(each, gamestate.selfsnake.headpos)
		distifmove=findDist(destination, target)
		if(distifmove<distfromcurr):
			options.append(each)
	return options
	
####basic functions

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
def checkMove(possible_move, gamestate):
	w=avoidWall(possible_move, gamestate)
	#w=True
	#e=True
	#s=True
	e=avoid(gamestate, possible_move, [E,e]) #avoid enemies
	s=avoid(gamestate, possible_move, [S,s]) #avoid self
	if(s and w and e):
		return True
	return False

#AVOID
#takes a move as input (up,down,left,right) and checks
#to see if it will result in a collision with something specified in [types]
#which is ***already there*** (important)
#returns true if the move is safe, false otherwise
def avoid(gamestate, move, types):
	destination=dest(move, gamestate.selfsnake.headpos)
	result=not checkState(gamestate, destination, types)
	return result

#CHECKSTATE
#looks at the index specified by location and returns
#true if it contains anything in [types], false otherwise
def checkState(gamestate, location, types):
	for each in types:
		if(gamestate.board[location[0]][location[1]]==each):
			return True
	return False

#DEST
#returns the coordinate that would be moved to
#if the move was submitted
def dest(move, head):
	result={
		'up': lambda x,y: [x,y-1],
		'down': lambda x,y: [x,y+1],
		'left': lambda x,y: [x-1,y],
		'right': lambda x,y: [x+1,y]
	}[move](head)
	return result

#returns false if the proposed move places us on a board wall
def avoidWall(possible_move, gamestate):
	destination = dest(possible_move, gamestate.selfsnake.headpos)
	wallBuffer = 0
	if(destination[0] < 0 + wallBuffer or destination[0] > gamestate.width - wallBuffer):
		return False
	if(destination[1] < 0 + wallBuffer or destination[1] > gamestate.height - wallBuffer):
		return False
	return True

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))









