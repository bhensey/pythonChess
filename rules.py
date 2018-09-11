 

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
		self.enemyMoves = [piece.validMoves(self) for piece in self.Pieces[self.turn*-1][1:]]	
		self.enemyMovesList = [move for sublist in self.enemyMoves for move in sublist]
		self.allMoves = [piece.validMoves(self) for piece in self.Pieces[self.turn]]
		self.friendMoves = self.allMoves[1:]
	
	def validMoves(self):
		# If king is in check, restrict moves to getting him out or defending
		kingIndex = self.Pieces[self.turn][0].index
		if kingIndex in self.enemyMovesList:
			# Find checking piece
			for pieceIndex in range(len(self.enemyMoves)):
				for move in self.enemyMoves[pieceIndex]:
					if move == kingIndex:
						piece = self.Pieces[self.turn*-1][pieceIndex+1]
						break
			# Remove moves that don't address check
			if isinstance(piece, (pawn, rook)):
				uncheckMoves = [piece.index]
			else:
				uncheckMoves = list(filter(lambda x: self._isBetween(x, self.Pieces[self.turn][0], piece), piece.validMoves(self))) + [piece.index]
			validMoves = [self.allMoves[0]]
			for moveList in self.friendMoves:
				validMoves.append(list(filter(lambda x: x in uncheckMoves, moveList)))
		else:
			validMoves = self.allMoves
		# If there is a pinned piece, restrict it's movement
		king = self.Pieces[self.turn][0]
		for piece in self.Pieces[self.turn*-1]:
			if isinstance(piece, (castle, queen)):
				if piece._xPos() == king._xPos() or piece._yPos() == king._yPos():
					print('castle or queen is inline')
					pinnedPiece = self.pinnedPiece(king, piece)
					if pinnedPiece:
						print('pinned piece')
						pieceIndex = self.Pieces[self.turn].index(pinnedPiece)
						validMoves[pieceIndex] = [move for move in pinnedPiece.validMoves(self) if move in piece.validMoves(self)]

			elif isinstance(piece, (bishop, queen)):
				if (piece._xPos()-king._xPos()) % (piece._yPos()-king._yPos()) == 0:
					print('bishop or queen is diagonal')
					pinnedPiece = self.pinnedPiece(king, piece)
					if pinnedPiece:
						print('pinned piece')
						pieceIndex = self.Pieces[self.turn].index(pinnedPiece)
						validMoves[pieceIndex] = [move for move in pinnedPiece.validMoves(self) if move in piece.validMoves(self)]
		
		return validMoves

	def pinnedPiece(self, king, attacker):
		piece = None
		moveArray = list(filter(lambda x: self._isBetween(x, king, attacker), attacker.validMoves(self)))
		for index in moveArray:
			if attacker.isFriend(index, self): 
				return None
			if attacker.isEnemy(index, self): 
				if piece:
					return None
				piece = self.getPiece(index)
		return piece

	def _isBetween(self, index, king, attacker):
		sign = lambda x: x and (1, -1)[x < 0]
		tmpPiece = piece(index, 'white')
		xDir = sign(king._xPos()-attacker._xPos())
		yDir = sign(king._yPos()-attacker._yPos())
		output =  (sign(tmpPiece._xPos()-attacker._xPos()) == xDir) and (sign(tmpPiece._yPos()-attacker._yPos()) == yDir)
		return output



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

	firstMove = True

	def __init__(self, index, color):
		super().__init__(index,color)

	def move(self, index, board):
		self.firstMove = False
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


