import requests

search_list=["BFS","DFS","UCS","GS","A*","A*2"]

search="A*2"
target_url="https://www.cmpe.boun.edu.tr/~emre/courses/cmpe480/hw1/input1.txt"

txt = requests.get(target_url).text

from enum import IntEnum
from collections import deque
from copy import deepcopy
import heapq

class DirectionPriority(IntEnum):
	LEFT = 1
	DOWN = 2
	RIGHT = 3
	UP = 4

time = 0 # in order to implement FIFO to priorityQueue, we're keeping the creation time of nodes

class Node:
	def __init__(self, board, parent=None, peg="", direction="", path="", cost=0, creationTime=0):
		global time
		self.state = board
		self.parent = parent
		self.peg = peg
		self.direction = direction
		self.creationTime = time
		if parent is None:
			self.depth = 0
			self.cost = 0
			self.path = path
		else:
			self.depth = parent.depth + 1
			self.cost = parent.cost + cost
			self.path = parent.path + path
		time = time + 1

	def goalTest(self): # checks whether the state is the goal
		return True if self.state.countPegsOnBoard() == 1 else False

	def successors(self): # finds the all possible successors of current Node by looking all possible moves at the Node's state
		succ = []
		for move in self.state.findAllValidMoves():
			peg, direction, cost, coordinates = move
			new_board = deepcopy(self.state)
			new_board.makeMove(coordinates)
			if new_board.countPegsOnBoard() == 1:
				path = "{} {}".format(peg, direction.lower())
			else:
				path = "{} {}, ".format(peg, direction.lower())
			succ.append(Node(new_board, self, peg, DirectionPriority[direction].value, path, cost))
		return succ

class Board:
	def __init__(self,givenBoardText):
		self.board = []
		rows = givenBoardText.split("\n")
		count = 0
		for row in rows:
			countColumn = 0
			if row != "":
				self.board.append([])
				for spot in row:
					self.board[count].append(spot)
				count += 1
		
		self.rowSize = len(self.board)
		self.columnSize =  len(self.board[0])

	def outOfBonds(self, r, c): # checks whether given location (r, c) is out of bonds
		return min(r, c) < 0 or r >= self.rowSize or c >= self.columnSize

	def isPeg(self, r, c): # checks whether there is a peg in given location (r, c)
		if not self.outOfBonds(r, c):
			if self.board[r][c] != '.':
				return True
		return False

	def isHole(self, r, c): # checks whether there is a hole in given location (r, c)
		if not self.outOfBonds(r, c):
			if self.board[r][c] == '.':
				return True
		return False

	def findAllPegs(self): # return a dictionary of pegName: (row, column)
		pegs = {}
		for r in range(self.rowSize):
			for c in range(self.columnSize):
				if self.board[r][c] != ".":
					pegs[self.board[r][c]] = (r,c)
		return pegs

	def findValidMoves(self, pegCoordinate, pegName):  # return a list of all valid moves as (peg, direction, cost, source, destination) for given peg
		validMoves = []
		r, c = pegCoordinate

		left = -1
		while self.isPeg(r, c+left):
			left -= 1
		if self.isHole(r, c+left) and left < -1:
			validMoves.append((pegName, "LEFT", 4, ((pegCoordinate,(r, c+left)))))

		down = 1
		while self.isPeg(r+down, c):
			down += 1
		if self.isHole(r+down, c) and down > 1:
			validMoves.append((pegName, "DOWN", 3, (pegCoordinate,(r+down, c))))

		right = 1
		while self.isPeg(r, c+right):
			right += 1
		if self.isHole(r, c+right) and right > 1:
			validMoves.append((pegName, "RIGHT", 2, (pegCoordinate,(r, c+right))))

		up = -1
		while self.isPeg(r+up, c):
			up -= 1
		if self.isHole(r+up, c) and up < -1:
			validMoves.append((pegName, "UP", 1, (pegCoordinate,(r+up, c))))

		return validMoves

	def findAllValidMoves(self): # return a list of all valid moves as (peg, direction, cost, source, destination) for all pegs on board
		allValidMoves = []
		pegs = self.findAllPegs()
		for peg in sorted(pegs.keys()):
			allValidMoves.extend(self.findValidMoves(pegs[peg], peg))
		return allValidMoves

	def makeMove(self, move): # changes board itself according to the given move
		source, destination = move
		sr, sc = source
		dr, dc = destination

		self.board[dr][dc] = self.board[sr][sc]
		
		if sr == dr and sc < dc: #right
			while(sc != dc):
				self.board[sr][sc] = "."
				sc += 1
		elif sr == dr and sc > dc: #left
			while(sc != dc):
				self.board[sr][sc] = "."
				sc -= 1
		elif sr < dr: #down
			while(sr != dr):
				self.board[sr][sc] = "."
				sr += 1
		else: #up
			while(sr != dr):
				self.board[sr][sc] = "."
				sr -= 1

	def countPegsOnBoard(self): # returns the number of pegs on the board
		count = 0
		for row in self.board:
			for spot in row:
				if spot != ".":
					count += 1
		return count

	def h1(self): # heuristic function h1(n) given in the description
		pegs = self.findAllPegs()
		row = set()
		column = set()
		for peg in pegs.keys():
			r, c = pegs[peg]
			row.add(r)
			column.add(c)
		return min(len(row), len(column)) - 1

	def h2(self): # heuristic function h2(n) implemented by me
		boardSize = self.rowSize * self.columnSize
		pegsNum = self.countPegsOnBoard()
		pegOccupancyRate = pegsNum / boardSize
		return pegOccupancyRate

class priorityQueue: # priority queue implementation for UCS, GS, A*, and A*2 algorithms
	def __init__(self):
		self.data = []
		self.index = 0

	# in algorithms, priority is given as (function values of algo, pegName, direction, time) in order to apply given tie-breakers in the description
	def push(self, item, priority):
		heapq.heappush(self.data, (priority, self.index, item))
		self.index += 1

	def pop(self):
		 return heapq.heappop(self.data)[-1]


def bfsAlgo(rootNode):
	removedNodes = 0

	frontier = deque()
	frontier.append(rootNode)

	explored = []

	while(frontier):
		node = frontier.popleft()
		removedNodes += 1
		if node.goalTest(): return (node, removedNodes)
		explored.append(node.state)
		children = node.successors()
		for child in children:
			if child.state not in explored and child.state not in frontier:
				frontier.append(child)

	return "no solution"


def dfsAlgo(node, explored=[]):
	removedNodes = 0

	frontier = deque()
	frontier.append(rootNode)

	explored = []

	while(frontier):
		node = frontier.pop()
		removedNodes += 1
		if node.goalTest(): return (node, removedNodes)
		explored.append(node.state)
		children = node.successors()
		for child in children:
			if child.state not in explored and child.state not in frontier:
				frontier.append(child)

	return "no solution"


def ucsAlgo(startingBoard): # f = cost
	removedNodes = 0

	frontier = priorityQueue()
	frontier.push(rootNode, (rootNode.cost, rootNode.peg, rootNode.direction, rootNode.creationTime))

	explored = []

	while(frontier):
		node = frontier.pop()
		removedNodes += 1
		if node.goalTest(): return (node, removedNodes)
		explored.append(node.state)
		children = node.successors()
		for child in children:
			if child.state not in explored:
				frontier.push(child, (child.cost, child.peg, child.direction, child.creationTime))

	return "no solution"

def gsAlgo(startingBoard): # f = h
	removedNodes = 0

	frontier = priorityQueue()
	frontier.push(rootNode, (rootNode.state.h1(), rootNode.peg, rootNode.direction, rootNode.creationTime))

	explored = []

	while(frontier):
		node = frontier.pop()
		removedNodes += 1
		if node.goalTest(): return (node, removedNodes)
		explored.append(node.state)
		children = node.successors()
		for child in children:
			if child.state not in explored:
				frontier.push(child, (child.state.h1(), child.peg, child.direction, child.creationTime))

	return "no solution"

def AStarAlgo(startingBoard): # f = g + h1
	removedNodes = 0

	frontier = priorityQueue()
	frontier.push(rootNode, (rootNode.cost + rootNode.state.h1(), rootNode.peg, rootNode.direction, rootNode.creationTime))

	explored = []

	while(frontier):
		node = frontier.pop()
		removedNodes += 1
		if node.goalTest(): return (node, removedNodes)
		explored.append(node.state)
		children = node.successors()
		for child in children:
			if child.state not in explored:
				frontier.push(child, (child.cost + child.state.h1(), child.peg, child.direction, child.creationTime))

	return "no solution"

def AStar2Algo(startingBoard): # f = g + h2
	removedNodes = 0

	frontier = priorityQueue()
	frontier.push(rootNode, (rootNode.cost + rootNode.state.h2(), rootNode.peg, rootNode.direction, rootNode.creationTime))

	explored = []

	while(frontier):
		node = frontier.pop()
		removedNodes += 1
		if node.goalTest(): return (node, removedNodes)
		explored.append(node.state)
		children = node.successors()
		for child in children:
			if child.state not in explored:
				frontier.push(child, (child.cost + child.state.h2(), child.peg, child.direction, child.creationTime))

	return "no solution"

board = Board(txt)
rootNode = Node(board)

if search == "BFS":
	soln = bfsAlgo(rootNode)
	solnNode, removedNodes = soln
elif search == "DFS":
	soln = dfsAlgo(rootNode)
	solnNode, removedNodes = soln
elif search == "UCS":
	soln = ucsAlgo(rootNode)
	solnNode, removedNodes = soln
elif search == "GS":
	soln = gsAlgo(rootNode)
	solnNode, removedNodes = soln
elif search == "A*":
	soln = AStarAlgo(rootNode)
	solnNode, removedNodes = soln
elif search == "A*2":
	soln = AStar2Algo(rootNode)
	solnNode, removedNodes = soln

print(search)
print("Number of removed nodes: " + str(removedNodes))
print("Path cost: " + str(solnNode.cost))
print("Solution: " + str(solnNode.path))