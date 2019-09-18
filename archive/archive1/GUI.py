import tkinter as tk
from gameState import *

#Global Variables
tiles = ["floral white","peachpuff3"]
tiles = (tiles*4+tiles[::-1]*4)*4
squareList=[]

		

# If the selection is a piece, 
def unselected(event):
	index = squareList.index(event.widget)
	drawPieces()
	if board.isPiece(index):
		moveArray = board.getPiece(index).moveArray()
		for square in moveArray:
			squareList[square].config(bg="dark sea green")
			squareList[square].bind("<Button-1>", lambda x: moveSelect(x,index,moveArray))
	else:
		drawPieces()
	return		

def moveSelect(event,prevIndex,moveArray):
	index = squareList.index(event.widget)
	if index in moveArray:
		board.move(prevIndex,index)
	for square in moveArray:
		squareList[square].bind("<Button-1>", unselected)
	drawPieces()
	return



def initBoard(window):
	global squareList
	for r in range(8):
		for c in range(8):
			label = tk.Label(window, bg=tiles[r*8+c], font=("Courier",40), width = 1, height = 1)
			label.grid(row = 7-r, column = c, ipadx=11, ipady=3)
			label.bind("<Button-1>", unselected)
			squareList.append(label)
	drawPieces()
	return


def drawPieces():
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










