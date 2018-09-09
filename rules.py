 

""" pythonChess is a module that provides a board object that holds and provides
 all the information to play a standard game of chess. Piece classes are used to hold data 
 and perform computations, but don't need to be interfaced with directly. 
""" 

# Module Constants
WHITE = 1
BLACK = -1

class board:

	# Initialize chessboard state
	Pieces = {WHITE:[], BLACK:[]}
	turn = WHITE
	enPassant = None


	def __init__(self):
		# White Pieces
		self.Pieces[WHITE] += [king(4,WHITE), bishop(5,WHITE),rook(6,WHITE), castle(7,WHITE)]
		self.Pieces[WHITE] +=  [castle(0,WHITE), rook(1,WHITE), bishop(2,WHITE), queen(3,WHITE)]
		for i in range(8): self.Pieces[WHITE].append(pawn(8+i,WHITE))

		# Black Pieces
		self.Pieces[BLACK] += [king(60,BLACK), bishop(61,BLACK),rook(62,BLACK), castle(63,BLACK)]
		self.Pieces[BLACK] += [castle(56,BLACK), rook(57,BLACK), bishop(58,BLACK), queen(59,BLACK)]
		for i in range(8): self.Pieces[BLACK].append(pawn(48+i,BLACK))

	def validMoves(self, piece):
		return piece.validMoves(self)

	def move(self, prevIndex, index):
		self.getPiece(prevIndex).move(index, self)
		self.turn *= -1
		return

	def isPiece(self, index):
		for piece in (self.Pieces[WHITE]+self.Pieces[BLACK]):
			if piece.index == index:
				return True
		return False

	def getPiece(self, index):
		for piece in (self.Pieces[WHITE]+self.Pieces[BLACK]):
			if piece.index == index:
				return piece
		raise ValueError ("No piece on the square", index)

	def remove(self, color, index):
		self.Pieces[color].remove(self.getPiece(index))
		return

"""Chess piece metaclass. Each piece can provide, compute, or alter the following information:
	1. index - (position on the chess board from 0 to 63)
	2. color - (white or black)
	3. validMoves() - legal chess moves avaliable to the piece
	4. move() 	
"""

class piece:
	def __init__(self, index, color):
		self.index = index
		self.color = color

	def validMoves(self, board):
		# Test moves
		validMoves = [35]
		#output = list(filter(lambda x: not(self.isFriend(x)), output))
		return validMoves

	def move(self, index, board):
		if self.isEnemy(index, board):
			board.remove(self.color*-1,index)
		self.index = index
		board.enPassant = None
		return

	def isFriend(self, index, board):
		for piece in board.Pieces[self.color]:
			if piece.index == index:
				return True
		return False

	def isEnemy(self, index, board):
		for piece in board.Pieces[self.color*-1]:
			if piece.index == index:
				return True
		return False
		
	def _xPos(self, index=None):
		""" xPos ranges from 1 to 8 for piece or given location
		"""
		if index is None:
			index = self.index
		return (index % 8)+1

	def _yPos(self, index=None):
		""" yPos ranges from 1 to 8 for piece or given location
		"""
		if index is None:
			index = self.index
		return (index // 8)+1

	def __str__(self, a):
		return a

# Specific Pieces

class pawn(piece):
	
	firstMove = True

	def __init__(self, index, color):
		super().__init__(index,color)

	def validMoves(self, board):
		validMoves = []
		# Basic moves
		moveIndex = self.index + self.color*8
		if not self.isFriend(moveIndex, board):
			validMoves.append(moveIndex)
			if self.firstMove:
				validMoves.append(moveIndex+self.color*8)
		# Capture moves
		moveIndex = self.index + self.color*7
		if self.isEnemy(moveIndex, board) and self._yPos(moveIndex) == self._yPos()+self.color:
			validMoves.append(moveIndex)
		moveIndex = self.index + self.color*9
		if self.isEnemy(moveIndex, board) and self._yPos(moveIndex) == self._yPos()+self.color :
			validMoves.append(moveIndex)
		# enPassant moves
		if board.enPassant:
			if board.enPassant._yPos() == self._yPos():
				if abs(board.enPassant.index-self.index) == 1:
					validMoves.append(board.enPassant.index+self.color*8)
		return validMoves

	def move(self, index, board):
		enPassant = board.enPassant
		super().move(index, board)
		# Set enPassant and firstMove flags
		if self.firstMove == True and self._yPos() in [4,5]:
			board.enPassant = self
		self.firstMove = False	
		# Check for enPassant capture
		if enPassant:
			if enPassant.index == index-self.color*8:
				board.remove(self.color*-1,index-self.color*8)
		return

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♙')
		else:
			return super().__str__('♟')

class castle(piece):
	def __init__(self, index, color):
		super().__init__(index,color)

	def move(self, index, board):
		super().move(index, board)
		return

	def validMoves(self, board):
		validMoves = []
		# Up moves
		tmpPos = self.index + 8
		while not(self.isFriend(tmpPos, board)) and (tmpPos<64):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 8
		# Down moves
		tmpPos = self.index - 8
		while not(self.isFriend(tmpPos, board)) and (tmpPos>-1):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 8
		#Right moves
		tmpPos = self.index + 1
		while not(self.isFriend(tmpPos, board)) and (tmpPos%8 != 0):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 1
		#Left moves
		tmpPos = self.index -1
		while not(self.isFriend(tmpPos, board)) and (tmpPos%8 != 7):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 1
		return validMoves


	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♖')
		else:
			return super().__str__('♜')
	
class rook(piece):
	def __init__(self, index, color):
		super().__init__(index,color)		

	def validMoves(self, board):
		validMoves = []
		#Add left moves
		if (self.index%8>0):
			validMoves += [self.index-17,self.index+15]
		if (self.index%8>1):
			validMoves += [self.index-10,self.index+6]
		#Add right moves
		if (self.index%8<7):
			validMoves += [self.index-15, self.index+17]
		if (self.index%8<6):
			validMoves += [self.index-6, self.index+10]
		# Remove invalid moves
		validMoves = list(filter(lambda x: x<64 and x>-1, validMoves))
		validMoves = list(filter(lambda x: not(self.isFriend(x, board)), validMoves))
		return validMoves

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♘')
		else:
			return super().__str__('♞')

class bishop(piece):
	def __init__(self, index, color):
		super().__init__(index,color)

	def validMoves(self, board):
		validMoves = []
		# UpRight moves
		tmpPos = self.index + 9
		while not(self.isFriend(tmpPos, board)) and (tmpPos<64) and (tmpPos%8 != 0):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 9
		# UpLeft moves
		tmpPos = self.index + 7
		while not(self.isFriend(tmpPos, board)) and (tmpPos<64) and (tmpPos%8 != 7):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 7
		# DownRight moves
		tmpPos = self.index -7
		while not(self.isFriend(tmpPos, board)) and (tmpPos>-1) and (tmpPos%8 != 0):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 7
		# DownLeft moves
		tmpPos = self.index -9
		while not(self.isFriend(tmpPos, board)) and (tmpPos>-1) and (tmpPos%8 != 7):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 9
		return validMoves

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♗')
		else:
			return super().__str__('♝')

class queen(piece):
	def __init__(self, index, color):
		super().__init__(index,color)

	def validMoves(self, board):
		validMoves = []
		# Castle moves
		# Up moves
		tmpPos = self.index + 8
		while not(self.isFriend(tmpPos, board)) and (tmpPos<64):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 8
		# Down moves
		tmpPos = self.index - 8
		while not(self.isFriend(tmpPos, board)) and (tmpPos>-1):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 8
		#Right moves
		tmpPos = self.index + 1
		while not(self.isFriend(tmpPos, board)) and (tmpPos%8 != 0):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 1
		#Left moves
		tmpPos = self.index -1
		while not(self.isFriend(tmpPos, board)) and (tmpPos%8 != 7):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 1
		# Bishop moves
		# UpRight moves
		tmpPos = self.index + 9
		while not(self.isFriend(tmpPos, board)) and (tmpPos<64) and (tmpPos%8 != 0):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 9
		# UpLeft moves
		tmpPos = self.index + 7
		while not(self.isFriend(tmpPos, board)) and (tmpPos<64) and (tmpPos%8 != 7):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += 7
		# DownRight moves
		tmpPos = self.index -7
		while not(self.isFriend(tmpPos, board)) and (tmpPos>-1) and (tmpPos%8 != 0):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 7
		# DownLeft moves
		tmpPos = self.index -9
		while not(self.isFriend(tmpPos, board)) and (tmpPos>-1) and (tmpPos%8 != 7):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos -= 9
		return validMoves

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♕')
		else:
			return super().__str__('♛')

class king(piece):

	castleKing = True
	castleQueen = True

	def __init__(self, index, color):
		super().__init__(index,color)		

	def validMoves(self, board):
		validMoves = [self.index+8,self.index-8]
		# Add left moves
		if (self.index%8!=0):
			validMoves += [self.index-9,self.index-1,self.index+7]
		# Add right moves
		if (self.index%8!=7):
			validMoves += [self.index-7,self.index+1,self.index+9]
		# Remove invalid up/down moves, remove friendly moves
		validMoves = list(filter(lambda x: x<64 and x>-1, validMoves))
		validMoves = list(filter(lambda x: not(self.isFriend(x, board)), validMoves))

		# Castling moves


		return validMoves

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♔')
		else:
			return super().__str__('♚')
