import tkinter as tk
from rules import *

#Global Variables
class GUI:
	tiles = ["peachpuff3","floral white"]
	tiles = (tiles*4+tiles[::-1]*4)*4

	def __init__(self, board):
		self.window = tk.Tk(); self.window.title('ChessBoard'); self.window.resizable(0,0)
		self.board = board
		self.validMoves = self.board.validMoves()
		self.squareList=[]
		# Initiating chessboard squares in squareList
		for r in range(8):
			for c in range(8):
				label = tk.Label(self.window, bg=self.tiles[r*8+c], font=("Courier",40), width = 1, height = 1)
				label.grid(row = 7-r, column = c, ipadx=11, ipady=3)
				self.squareList.append(label)
		self.drawGame()
		self.window.mainloop()
 
	def selected(self, event):
		self.drawGame()
		index = self.squareList.index(event.widget)
		validMoves = self.validMoves[self.board.Pieces[self.board.turn].index(self.board.getPiece(index))]
		for square in validMoves:
			self.squareList[square].config(bg="dark sea green")
			self.squareList[square].bind("<Button-1>", lambda x: self.moveSelect(x,index,validMoves))
		return	


	def moveSelect(self, event,prevIndex,validMoves):
		""" Tells board to move give piece and compute next array of validMoves """
		self.board.move(prevIndex,self.squareList.index(event.widget))
		self.drawGame()
		self.validMoves = self.board.validMoves()
		return

	def drawGame(self):
		""" Redraw and unbind every square. Draw pieces and make one player's clickable """
		for i in range(len(self.squareList)):
			label = self.squareList[i]
			label.config(text="",bg=self.tiles[i])
			label.bind("<Button-1>", '')
		for piece in self.board.Pieces[WHITE]+self.board.Pieces[BLACK]:
			label = self.squareList[piece.index]
			label.config(text = piece)	
		for piece in self.board.Pieces[self.board.turn]:
			label = self.squareList[piece.index]
			label.bind("<Button-1>", self.selected)
		return

GUI = GUI(board())	











