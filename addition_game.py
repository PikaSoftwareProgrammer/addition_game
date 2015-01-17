from __future__ import division
import random as rand


class Board:

	def __init__(self, n) :
		# (rows, columns)
		self.board = {(i//n, i%n):0 for i in range(n**2)}
		self.board[(rand.randint(1,n-2),rand.randint(1,n-2))] = 1
		self.bs = n

	def __str__(self):
		s = ""
		for i in range(self.bs):
			for j in range(self.bs):
				s += str(self.board[(i, j)])
				if j != self.bs - 1:
					s += " | "
			s += "\n"
			s += "---"*self.bs
			s += "\n"
		s+="\n"
		return s

	def move_right(self):
		# Loop through the board
		for i in range(self.bs):
			for j in range(self.bs)[::-1]:
				if self.board[(i,j)] != 0:
					self.board[(i,(j+1)%self.bs)] += self.board[(i,j)]
					self.board[(i,j)] = 1 
					


	def move_left(self):
		for i in range(self.bs):
			for j in range(self.bs):
				if self.board[(i,j)] != 0:
					self.board[(i,(j-1)%self.bs)] += self.board[(i,j)]
					self.board[(i,j)] = 1


	def move_down(self):
		for i in range(self.bs):
			for j in range(self.bs)[::-1]:
				if self.board[(j, i)] != 0:
					self.board[((j+1)%self.bs, i)] += self.board[(j, i)] 
					self.board[(j, i)] = 1

	def move_up(self):
		for i in range(self.bs):
			for j in range(self.bs):
				if self.board[(j,i)] != 0:
						self.board[((j-1)%self.bs, i)] += self.board[(j,i)]
						self.board[(j, i)] = 1

	def check_lose(self):
		for i in range(self.bs):
			for j in range(self.bs):
				if self.board[(i, j)] % 5 == 0 and self.board[(i, j)] != 0:
					return True

		return False



if __name__ == "__main__":
	b = Board(4)
	turns = 0
	print b
	while True:
		print "Turn: " + str(turns)
		user = raw_input("Enter Your move! (W-up, A-left, S-down, D-right )")
		if len (user) > 1 or len(user) == 0 or user != 'w' or user != 'a' or user != 's' or user != 'd':
			if user == "w":
				b.move_up()
			elif user == "s":
				b.move_down()
			elif user == "a":
				b.move_left()
			else:
				b.move_right()
		if b.check_lose():
			print b
			print "You Lose!"
			break
		print b
		turns += 1