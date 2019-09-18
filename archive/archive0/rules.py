 

class board:

	# Initialize Chess Board 
	pieceArray = []

	def __init__(self):
		# White Pieces
		self.pieceArray +=  [self.castle([0,0],'white'), self.rook([1,0],'white'), self.bishop([2,0],'white'), self.queen([3,0],'white')]
		self.pieceArray += [self.king([4,0],'white'), self.bishop([5,0],'white'),self.rook([6,0],'white'), self.castle([7,0],'white')]
		for i in range(8): self.pieceArray.append(self.pawn([i,1],'white'))

		# Black Pieces
		self.pieceArray += [self.castle([0,7],'black'), self.rook([1,7],'black'), self.bishop([2,7],'black'), self.queen([3,7],'black')]
		self.pieceArray += [self.king([4,7],'black'), self.bishop([5,7],'black'),self.rook([6,7],'black'), self.castle([7,7],'black')]
		for i in range(8): self.pieceArray.append(self.pawn([i,6],'black'))


	def isPiece(self,index):
		for piece in self.pieceArray:
			if piece.index() == index:
				return True
		return False

	def getPiece(self,index):
		for piece in self.pieceArray:
			if piece.index() == index:
				return piece
		raise ValueError ("No piece on the square " + str(index))

	def pieceMoves(self,index):
		return getPiece(index).moveArray()

	def allMoves(self):
		output =[]
		for piece in self.pieceArray:
			output.append(piece.moveArray)
		return output

	def removePiece(self, index):
		self.pieceArray.remove(self.getPiece(index))
		return

	# All Pieces

	class piece:
		def __init__(self, position, color):
			self.position = position
			self.color = color
			if self.color == "white":
				self.colorMul = 1
			else:
				self.colorMul = -1

		def moveArray(self):
			# Test moves
			output = []
			output.append(self.index()+17)
			output.append(self.index()+15)
			output = list(filter(lambda x: not(self.isFriend(x)), output))
			return output

		def move(self,index):
			if self.isEnemy(index):
				print('enemy!')
			self.position[0] = index % 8
			self.position[1] = index // 8
			return

		def isEnemy(self,index):
			for piece in board.pieceArray:
				if piece.index() == index and piece.color != self.color:
					return True
			return False

		def isFriend(self,index):
			for piece in board.pieceArray:
				if piece.index() == index and piece.color == self.color:
					return True
			return False

		def index(self):
			return self.position[0] + self.position[1]*8

		def __str__(self, a):
			return a

	# Specific Pieces

	class pawn(piece):
		
		firstMove = True

		def __init__(self, position, color):
			super().__init__(position,color)

		def moveArray(self):
			moveArray = [self.index()+8*self.colorMul]
			if self.isFriend(moveArray[0]):
				return []
			if self.firstMove:
				moveArray.append(self.index()+16*self.colorMul)
			return moveArray

		def move(self,index):
			if self.firstMove:
				self.firstMove = False
			return super().move(index)

		def __str__(self):
			if self.color == "white":
				return super().__str__('♙')
			else:
				return super().__str__('♟')

	class castle(piece):
		def __init__(self, position, color):
			super().__init__(position,color)

		def moveArray(self):
			moveArray = []
			index = self.index()
			# Up moves
			tmpPos = index + 8
			while not(self.isFriend(tmpPos)) and (tmpPos<64):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 8
			# Down moves
			tmpPos = index - 8
			while not(self.isFriend(tmpPos)) and (tmpPos>-1):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 8
			#Right moves
			tmpPos = index + 1
			while not(self.isFriend(tmpPos)) and (tmpPos%8 != 0):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 1
			#Left moves
			tmpPos = index -1
			while not(self.isFriend(tmpPos)) and (tmpPos%8 != 7):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 1
			return moveArray

		def __str__(self):
			if self.color == "white":
				return super().__str__('♖')
			else:
				return super().__str__('♜')
		
	class rook(piece):
		def __init__(self, position, color):
			super().__init__(position,color)		

		def moveArray(self):
			moveArray = []
			index = self.index()
			#Add left moves
			if (index%8>0):
				moveArray += [index-17,index+15]
			if (index%8>1):
				moveArray += [index-10,index+6]
			#Add right moves
			if (index%8<7):
				moveArray += [index-15, index+17]
			if (index%8<6):
				moveArray += [index-6, index+10]
			# Remove invalid moves
			moveArray = list(filter(lambda x: x<64 and x>-1, moveArray))
			moveArray = list(filter(lambda x: not(self.isFriend(x)), moveArray))
			return moveArray

		def __str__(self):
			if self.color == "white":
				return super().__str__('♘')
			else:
				return super().__str__('♞')

	class bishop(piece):
		def __init__(self, position, color):
			super().__init__(position,color)

		def moveArray(self):
			moveArray = []
			index = self.index()
			# UpRight moves
			tmpPos = index + 9
			while not(self.isFriend(tmpPos)) and (tmpPos<64) and (tmpPos%8 != 0):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 9
			# UpLeft moves
			tmpPos = index + 7
			while not(self.isFriend(tmpPos)) and (tmpPos<64) and (tmpPos%8 != 7):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 7
			# DownRight moves
			tmpPos = index -7
			while not(self.isFriend(tmpPos)) and (tmpPos>-1) and (tmpPos%8 != 0):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 7
			# DownLeft moves
			tmpPos = index -9
			while not(self.isFriend(tmpPos)) and (tmpPos>-1) and (tmpPos%8 != 7):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 9
			return moveArray

		def __str__(self):
			if self.color == "white":
				return super().__str__('♗')
			else:
				return super().__str__('♝')

	class queen(piece):
		def __init__(self, position, color):
			super().__init__(position,color)

		def moveArray(self):
			moveArray = []
			index = self.index()
			# Up moves
			tmpPos = index + 8
			while not(self.isFriend(tmpPos)) and (tmpPos<64):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 8
			# Down moves
			tmpPos = index - 8
			while not(self.isFriend(tmpPos)) and (tmpPos>-1):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 8
			#Right moves
			tmpPos = index + 1
			while not(self.isFriend(tmpPos)) and (tmpPos%8 != 0):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 1
			#Left moves
			tmpPos = index -1
			while not(self.isFriend(tmpPos)) and (tmpPos%8 != 7):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 1
			index = self.index()
			# UpRight moves
			tmpPos = index + 9
			while not(self.isFriend(tmpPos)) and (tmpPos<64) and (tmpPos%8 != 0):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 9
			# UpLeft moves
			tmpPos = index + 7
			while not(self.isFriend(tmpPos)) and (tmpPos<64) and (tmpPos%8 != 7):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos += 7
			# DownRight moves
			tmpPos = index -7
			while not(self.isFriend(tmpPos)) and (tmpPos>-1) and (tmpPos%8 != 0):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 7
			# DownLeft moves
			tmpPos = index -9
			while not(self.isFriend(tmpPos)) and (tmpPos>-1) and (tmpPos%8 != 7):
				moveArray.append(tmpPos)
				if self.isEnemy(tmpPos): break
				tmpPos -= 9
			return moveArray

		def __str__(self):
			if self.color == "white":
				return super().__str__('♕')
			else:
				return super().__str__('♛')

	class king(piece):
		def __init__(self, position, color):
			super().__init__(position,color)		

		def moveArray(self):
			index = self.index()
			moveArray = [index+8,index-8]
			# Add left moves
			if (index%8!=0):
				moveArray += [index-9,index-1,index+7]
			# Add right moves
			if (index%8!=7):
				moveArray += [index-7,index+1,index+9]
			# Remove invalid moves
			moveArray = list(filter(lambda x: x<64 and x>-1, moveArray))
			moveArray = list(filter(lambda x: not(self.isFriend(x)), moveArray))
			return moveArray

		def __str__(self):
			if self.color == "white":
				return super().__str__('♔')
			else:
				return super().__str__('♚')


