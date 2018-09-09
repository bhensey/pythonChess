import tkinter as tk
from rules import *

#Global Variables
tiles = ["floral white","peachpuff3"]
tiles = (tiles*4+tiles[::-1]*4)*4
squareList=[]


# If the selection is a piece, 
def unselected(event, board):
	drawGame(board)
	index = squareList.index(event.widget)
	validMoves = board.validMoves(board.getPiece(index))
	for square in validMoves:
		squareList[square].config(bg="dark sea green")
		squareList[square].bind("<Button-1>", lambda x: moveSelect(x,index,validMoves))
	return	


def moveSelect(event,prevIndex,validMoves):
	board.move(prevIndex,squareList.index(event.widget))
	drawGame(board)
	return


def initBoard(window, board):
	global squareList
	for r in range(8):
		for c in range(8):
			label = tk.Label(window, bg=tiles[r*8+c], font=("Courier",40), width = 1, height = 1)
			label.grid(row = 7-r, column = c, ipadx=11, ipady=3)
			squareList.append(label)
	drawGame(board)
	return


def drawGame(board):
	""" Redraw and unbind every square. Draw pieces and make one player's clickable """
	for i in range(len(squareList)):
		label = squareList[i]
		label.config(text="",bg=tiles[i])
		label.bind("<Button-1>", '')
	for piece in board.Pieces[WHITE]+board.Pieces[BLACK]:
		label = squareList[piece.index]
		label.config(text = piece)	
	for piece in board.Pieces[board.turn]:
		label = squareList[piece.index]
		label.bind("<Button-1>", lambda x: unselected(x, board))
	return


board = board()
window = tk.Tk()
window.title('ChessBoard')
window.resizable(0,0)

initBoard(window, board)
	
window.mainloop()










