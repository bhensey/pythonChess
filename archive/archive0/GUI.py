import tkinter as tk
from rules import *

#Global Variables
board = board()
tiles = ["floral white","peachpuff3"]
tiles = (tiles*4+tiles[::-1]*4)*4
squareList = []
moveList = []
prevSquare = False
		

# Triggered by click on piece. Colors selection and offers possible moves.	
def select(event):
	global prevSquare, moveList
	index = squareList.index(event.widget)
	if board.isPiece(index):
		piece = board.getPiece(index)
	else:
		piece = False
	# Select move or cancel selection
	if index in moveList:
		board.getPiece(prevSquare).move(index)
		moveList = []
		prevSquare = False
		drawPieces(board)
		return
	elif not piece:
		moveList = []
		prevSquare = False
		drawPieces(board)
		return
	else:
		drawPieces(board)
		squareList[index].config(bg="dark sea green")
		moveList = piece.moveArray()
		for move in moveList:
			squareList[move].config(bg="dark sea green")
		prevSquare = index	
	return

#def click(event, prevIndex, moveChoices):
#	index = squareList.index(event.widget)
#	# Selecting a move
#	if prevIndex:
#		if index in moveList:
			



def initBoard(window):
	for r in range(8):
		for c in range(8):
			label = tk.Label(window, bg=tiles[r*8+c], font=("Courier",40), width = 1, height = 1)
			label.grid(row = 7-r, column = c, ipadx=11, ipady=3)
			label.bind("<Button-1>", select)
			squareList.append(label)
	drawPieces(board)
	return


def drawPieces(board):
	for i in range(len(squareList)):
		squareList[i].config(text="",bg=tiles[i])
	for piece in board.pieceArray:
		label = squareList[piece.position[0]+piece.position[1]*8]
		label.config(text = piece)	
	return



window = tk.Tk()
window.title('ChessBoard')
window.resizable(0,0)

initBoard(window)
	
window.mainloop()










