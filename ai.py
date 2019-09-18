from rules import *
import copy

""" Takes a board instance and outputs a favorable move """

class boardTree():
	def __init__(self, board, parentBoard = None):
		self.board = board
		self.parent = parentBoard
		self.children = []
	
	def deeper(self, depth):
		validMoves = self.board.validMoves()
		for pieceIndex in range(len(validMoves)):
			for move in validMoves[pieceIndex]:
				piece = board.Pieces[board.turn][pieceIndex]
				newBoard = copy.deepcopy(self.board)
				newBoard.move(piece.index, move)
				self.children.append(boardTree(newBoard, self))
				print(len(self.children))
		if depth > 0:
			for child in self.children:
				child.deeper(depth-1)
		return

	def getScore(self):
		if self.children == []:
			return self.positionScore()
		else:
			maxScore = float("-inf")
			for child in self.children:
				childScore = child.positionScore()
				if childScore > maxScore:
					maxScore = childScore
			return maxScore

	def positionScore(self):
		positionScore = 0
		for piece in self.board.Pieces[self.board.turn]:
			positionScore += piece.value
		for piece in self.board.Pieces[self.board.turn*-1]:
			positionScore -= piece.value
		return positionScore


def search(board, depth):
	if not (depth%2):
		raise ValueError ("Depth must be an odd number")
	treeNode = boardTree(board)
	treeNode.deeper(depth)
	return treeNode.getScore()




