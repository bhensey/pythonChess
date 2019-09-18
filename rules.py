 

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
	opponentMoves = []

	def __init__(self):
		"""Kings are always the first piece"""
		# White Pieces
		self.Pieces[WHITE] += [king(4,WHITE), castle(0,WHITE), castle(7,WHITE), bishop(5,WHITE)]
		self.Pieces[WHITE] +=  [rook(6,WHITE), rook(1,WHITE), bishop(2,WHITE), queen(3,WHITE)]
		for i in range(8): self.Pieces[WHITE].append(pawn(8+i,WHITE))

		# Black Pieces
		self.Pieces[BLACK] += [king(60,BLACK), castle(56,BLACK), castle(63,BLACK), bishop(61,BLACK)]
		self.Pieces[BLACK] += [rook(62,BLACK), rook(57,BLACK), bishop(58,BLACK), queen(59,BLACK)]
		for i in range(8): self.Pieces[BLACK].append(pawn(48+i,BLACK))

		# Initialize moves
		self._calcMoves()

	def _calcMoves(self):
		self.enemyMoves = [self._dummyKingMoves(self.Pieces[self.turn*-1][0].index)] + [piece.validMoves(self) for piece in self.Pieces[self.turn*-1][1:]]	
		self.enemyMovesList = [move for sublist in self.enemyMoves for move in sublist]
		self.allMoves = [piece.validMoves(self) for piece in self.Pieces[self.turn]]
		
		
	
	def validMoves(self):
		# If king is in check, restrict moves to getting him out or defending

		uncheckMoves = []
		kingIndex = self.Pieces[self.turn][0].index
		checkPieces = []
		for piece in range(len(self.enemyMoves)):
			for move in range(len(self.enemyMoves[piece])):
				if kingIndex == self.enemyMoves[piece][move]:
					checkPieces.append([self.Pieces[self.turn*-1][piece],piece])
					
		# If there is no check, return all moves
		if not checkPieces:
			return self.allMoves

		# If there are 2 checking pieces, you must eliminate them
		if len(checkPieces) > 1:
			uncheckMoves = [piece[0].index for piece in checkPieces]

		# If there is 1 checking piece, you must eliminate or block it
		elif len(checkPieces) == 1:
			piece = checkPieces[0]
			if isinstance(piece[0], (pawn, rook)):
				uncheckMoves = [piece[0].index]
			else:
				uncheckMoves = list(filter(lambda x: self._isBetween(x, self.Pieces[self.turn][0], piece[0]), self.enemyMoves[piece[1]])) + [piece[0].index]
		validMoves = [self.allMoves[0]]
		for moveList in self.allMoves[1:]:
			validMoves.append(list(filter(lambda x: x in uncheckMoves, moveList)))

		if not any(validMoves):
			print("Game Over")
				
		return validMoves

	def _isBetween(self, index, king, attacker):
		sign = lambda x: x and (1, -1)[x < 0]
		tmpPiece = piece(index, 'white')
		xDir = sign(king._xPos()-attacker._xPos())
		yDir = sign(king._yPos()-attacker._yPos())
		output =  (sign(tmpPiece._xPos()-attacker._xPos()) == xDir) and (sign(tmpPiece._yPos()-attacker._yPos()) == yDir)
		return output

	def _dummyKingMoves(self, index):
		validMoves = [index+8,index-8]
		# Add left moves
		if (index%8!=0):
			validMoves += [index-9,index-1,index+7]
		# Add right moves
		if (index%8!=7):
			validMoves += [index-7,index+1,index+9]
		# Remove invalid up/down moves, remove friendly moves
		validMoves = list(filter(lambda x: x<64 and x>-1, validMoves))
		return validMoves

	def move(self, prevIndex, index):
		self.getPiece(prevIndex).move(index, self)
		self.turn *= -1
		self._calcMoves()
		return

	def isCastle(self, index):
		if self.isPiece(index):
			piece = self.getPiece(index)
			if isinstance(piece,castle):
				return castle.firstMove

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

	pinned = False

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

	def isEmpty(self, index, board):
		return not (self.isFriend(index, board) or self.isEnemy(index, board))
		
	def _moveHelper(self, direction, board):
		"""Takes a direction vector and computes validMoves for it. Also sets the pinned status for opposing pieces """
		validMoves = []
		moveConstant = 0

		# Set board constraints
		constraints = ""
		if direction[0] == 1:
			constraints += "(tmpPos%8 != 0)"
			moveConstant += 1
		if direction[0] == -1:
			constraints += "(tmpPos%8 != 7)"
			moveConstant -= 1
		if direction[0] * direction[1] != 0:
			constraints += " and "
		if direction[1] == 1:
			constraints += "(tmpPos < 64)"
			moveConstant += 8
		if direction[1] == -1:
			constraints += "(tmpPos > -1)"
			moveConstant -= 8

		tmpPos = self.index + moveConstant
		while not(self.isFriend(tmpPos, board)) and eval(constraints):
			validMoves.append(tmpPos)
			if self.isEnemy(tmpPos, board): break
			tmpPos += moveConstant

		return validMoves

	def _pinHelper(self, direction, king, board):
		"""Checks for pinned pieces between a piece and a king. Gives a pinned piece the direction it is pinned from"""

		moveConstant = 0
		if direction[0] == 1:
			moveConstant += 1
		if direction[0] == -1:
			moveConstant -= 1
		if direction[1] == 1:
			moveConstant += 8
		if direction[1] == -1:
			moveConstant -= 8

		pin = False
		index = self.index + moveConstant
		while index != king.index:
			if self.isFriend(index, board): 
				return
			elif self.isEnemy(index, board) and not pin:
				pin = board.getPiece(index)
			elif self.isEnemy(index, board):
				return
			index += moveConstant
		if pin:
			pin.pinned = direction
		return

		

		return

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
	
	value = 1
	firstMove = True

	def __init__(self, index, color):
		super().__init__(index,color)

	def validMoves(self, board):
		validMoves = []
		# Basic moves
		moveIndex = self.index + self.color*8
		if self.isEmpty(moveIndex, board):
			validMoves.append(moveIndex)
			moveIndex += self.color*8
			if self.firstMove and self.isEmpty(moveIndex, board):
				validMoves.append(moveIndex)
		# Capture moves
		moveIndex = self.index + self.color*7
		if self.isEnemy(moveIndex, board) and self._yPos(moveIndex) == self._yPos()+self.color:
			validMoves.append(moveIndex)
		moveIndex = self.index + self.color*9
		if self.isEnemy(moveIndex, board) and self._yPos(moveIndex) == self._yPos()+self.color :
			validMoves.append(moveIndex)
		# Remove moves if pinned
		if self.pinned:
			moveIndex = [self.index + self.pinned[0]*-1 + self.pinned[1]*-8]
			moveIndex.append(moveIndex[0] + self.pinned[0]*-1 + self.pinned[1]*-8)
			validMoves = [move for move in validMoves if move in moveIndex]
			self.pinned = False

		# enPassant moves
		elif board.enPassant:
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
		# Check for promotion
		if self._yPos(index) == 1 or self._yPos(index) == 8:
			board.Pieces[self.color].remove(self)
			board.Pieces[self.color].append(queen(self.index, self.color))
		return

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♙')
		else:
			return super().__str__('♟')

class castle(piece):

	value = 5
	firstMove = True

	def __init__(self, index, color):
		super().__init__(index,color)

	def move(self, index, board):
		self.firstMove = False
		super().move(index, board)
		return

	def validMoves(self, board):
		validMoves = []

		# Check if castle is pinning another piece
		enemyKing = board.Pieces[self.color*-1][0]
		if self._xPos() == enemyKing._xPos():
			if enemyKing._yPos()>self._yPos():
				super()._pinHelper((0, 1), enemyKing, board)
			else:
				super()._pinHelper((0, -1), enemyKing, board)

		elif self._yPos() == enemyKing._yPos():
			if enemyKing._xPos()>self._xPos():
				super()._pinHelper((1, 0), enemyKing, board)
			else:
				super()._pinHelper((-1, 0), enemyKing, board)

		# Compute valid moves
		if not self.pinned:
			validMoves += super()._moveHelper((0,1), board)
			validMoves += super()._moveHelper((0,-1), board)
			validMoves += super()._moveHelper((1,0), board)
			validMoves += super()._moveHelper((-1,0), board)

		elif self.pinned[0] == 0:
			validMoves += super()._moveHelper((0,1), board)
			validMoves += super()._moveHelper((0,-1), board)

		elif self.pinned[1] == 0:
			validMoves += super()._moveHelper((1,0), board)
			validMoves += super()._moveHelper((-1,0), board)

		self.pinned = False

		return validMoves


	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♖')
		else:
			return super().__str__('♜')
	
class rook(piece):

	value = 3

	def __init__(self, index, color):
		super().__init__(index,color)		

	def validMoves(self, board):
		# No valid moves if pinned to king
		if self.pinned:
			self.pinned = False
			return []

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

	value = 3

	def __init__(self, index, color):
		super().__init__(index,color)

	def validMoves(self, board):
		# Check if bishop is pinning another piece
		enemyKing = board.Pieces[self.color*-1][0]
		if abs(self._xPos()-enemyKing._xPos()) == abs(self._yPos()-enemyKing._yPos()):
			direction = [-1,-1]
			if enemyKing._yPos()>self._yPos(): 
				direction[1] = 1
			if enemyKing._xPos()>self._xPos():
				direction[0] = 1
			super()._pinHelper(direction, enemyKing, board)

		#Compute valid moves
		validMoves = []
		if not self.pinned:
			validMoves += super()._moveHelper((1,1), board)
			validMoves += super()._moveHelper((-1,-1), board)
			validMoves += super()._moveHelper((1,-1), board)
			validMoves += super()._moveHelper((-1,1), board)
		
		elif self.pinned[0] * self.pinned[1] == 1:
			validMoves += super()._moveHelper((1,1), board)
			validMoves += super()._moveHelper((-1,-1), board)

		elif self.pinned[0] * self.pinned[1] == -1:
			validMoves += super()._moveHelper((1,-1), board)
			validMoves += super()._moveHelper((-1,1), board)

		self.pinned = False

		return validMoves

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♗')
		else:
			return super().__str__('♝')

class queen(piece):

	value = 9

	def __init__(self, index, color):
		super().__init__(index,color)

	def validMoves(self, board):

		# Check if castle is pinning another piece
		enemyKing = board.Pieces[self.color*-1][0]
		if self._xPos() == enemyKing._xPos():
			if enemyKing._yPos()>self._yPos():
				super()._pinHelper((0, 1), enemyKing, board)
			else:
				super()._pinHelper((0, -1), enemyKing, board)

		elif self._yPos() == enemyKing._yPos():
			if enemyKing._xPos()>self._xPos():
				super()._pinHelper((1, 0), enemyKing, board)
			else:
				super()._pinHelper((-1, 0), enemyKing, board)

		elif abs(self._xPos()-enemyKing._xPos()) == abs(self._yPos()-enemyKing._yPos()):
			direction = [-1,-1]
			if enemyKing._yPos()>self._yPos(): 
				direction[1] = 1
			if enemyKing._xPos()>self._xPos():
				direction[0] = 1
			super()._pinHelper(direction, enemyKing, board)

		validMoves = []

		# Compute valid moves
		if not self.pinned:
			validMoves += super()._moveHelper((0,1), board)
			validMoves += super()._moveHelper((0,-1), board)
			validMoves += super()._moveHelper((1,0), board)
			validMoves += super()._moveHelper((-1,0), board)
			validMoves += super()._moveHelper((1,1), board)
			validMoves += super()._moveHelper((1,-1), board)
			validMoves += super()._moveHelper((-1,-1), board)
			validMoves += super()._moveHelper((-1,1), board)

		elif self.pinned[0] == 0:
			validMoves += super()._moveHelper((0,1), board)
			validMoves += super()._moveHelper((0,-1), board)

		elif self.pinned[1] == 0:
			validMoves += super()._moveHelper((1,0), board)
			validMoves += super()._moveHelper((-1,0), board)

		elif self.pinned[0] * self.pinned[1] == 1:
			validMoves += super()._moveHelper((1,1), board)
			validMoves += super()._moveHelper((-1,-1), board)

		elif self.pinned[0] * self.pinned[1] == -1:
			validMoves += super()._moveHelper((1,-1), board)
			validMoves += super()._moveHelper((-1,1), board)

		self.pinned = False

		return validMoves

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♕')
		else:
			return super().__str__('♛')

class king(piece):

	value = 0

	firstMove = True

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
		# Remove moves that put king in check
		validMoves = list(filter(lambda x: x not in board.enemyMovesList, validMoves))

		# Castling moves
		if self.index not in board.enemyMovesList:
			if self.firstMove == True:
				if self.isEmpty(self.index+1, board) and self.isEmpty(self.index+2, board):
					if self.index+1 and self.index+2 not in board.enemyMovesList:
						if board.isCastle(self.index+3):
							validMoves.append(self.index+2)
				if self.isEmpty(self.index-1, board) and self.isEmpty(self.index-2, board) and self.isEmpty(self.index-3, board):
					if self.index-1 and self.index-2 not in board.enemyMovesList:
						if board.isCastle(self.index-4):
							validMoves.append(self.index-2)
		return validMoves

	def move(self, index, board):
		# Check for castling
		if self.firstMove:
			self.firstMove = False
			if index == self.index+2:
				board.getPiece(self.index+3).move(self.index+1, board)
			if index == self.index-2:
				board.getPiece(self.index-4).move(self.index-1, board)
		super().move(index, board)

		return

	def __str__(self):
		if self.color == WHITE:
			return super().__str__('♔')
		else:
			return super().__str__('♚')


