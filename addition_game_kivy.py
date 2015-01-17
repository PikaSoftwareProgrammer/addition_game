from __future__ import division
import kivy
kivy.require("1.8.0")
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ReferenceListProperty
from kivy.core.window import Window
from kivy.animation import Animation
from math import fabs, sqrt
import random as rand
import time

def magnitude(x1, y1, x2, y2):
	return sqrt((x2-x1)**2+(y2-y1)**2)


class SwoopAndZoom(Animation):
	def __init__(self, **kwargs):
		super(SwoopAndZoom, self).__init__(**kwargs)
		self.i = 0
		self.j = 0
		self.bs = 0

	def on_complete(self, Widget):
		Widget.x = self.j*(Window.width//self.bs)+(Window.width//self.bs)//2
		Widget.y = Window.height-(self.i+1)*(Window.height//self.bs)
		print Widget.color
		Widget.color = Widget.color[:3]+[0.0]

	def set_ij_bs(self, t, bs):
		self.i = t[0]
		self.j = t[1]
		self.bs = bs

class MeWidget(Widget):
	def __init__(self, **kwargs):
		super(MeWidget, self).__init__(**kwargs)
		
		# change this variable to change the number that makes you lose.
		self.nonum = 5

		# bs is boardsize
		self.bs = 4
		self.board = {}

		self.hidden_board = {(i//self.bs, i%self.bs):0 for i in range(self.bs**2)}
		self.hidden_board[(rand.randint(1,self.bs-2),rand.randint(1,self.bs-2))] = 1

		self.score = 0
		self.highscore = 0
		self.score_board = Label(text="Score: "+str(self.score)+" Highscore: "+str(self.highscore), font_size='24sp', x=Window.width//2, y=Window.height-100)
		self.score_board.x -= self.score_board.width//2
		self.add_widget(self.score_board)


		self._keyboard = Window.request_keyboard(self._keyboard_closed,self,'text')
		self._keyboard.bind(on_key_down=self._on_keyboard_down)

		#self.layout = GridLayout(rows=bs, cols=bs, col_default_width=Window.width//bs, row_default_height=Window.height//bs)
		for i in range(self.bs):
			for j in range(self.bs):
				self.board[(i, j)] = Label(color=(1,1, 1, 1),text=str(self.hidden_board[(i,j)]), font_size='40sp',\
					x=j*(Window.width//(self.bs+1))+(Window.width//(self.bs+1))//2, y=Window.height-(i+1)*(Window.height//(self.bs+1)))
				self.add_widget(self.board[(i,j)])

	def on_touch_down(self, touch):
		self.oldx = touch.x
		self.oldy = touch.y

	def on_touch_up(self, touch):
		mag = magnitude(self.oldx, self.oldy, touch.x, touch.y)
		dx = self.oldx - touch.x
		dy = self.oldy - touch.y

		if self.check_lose():
			self.reset()
		#change the number below to change the sensitivity of the swipe.
		elif mag > 20:
			if fabs(dx)>fabs(dy):
				if dx < 0:
					self.move_right()
				else:
					self.move_left()
			else:
				if dy < 0:
					self.move_up()
				else: 
					self.move_down()




	def one_plus_score(self):
		self.score += 1
		self.score_board.text = "Score: " + str(self.score) +" Highscore: "+str(self.highscore)

	def score_reset(self):
		if self.highscore < self.score: 
			self.highscore = self.score
		self.score = 0
		self.score_board.text = "Score: " + str(self.score) +" Highscore: "+str(self.highscore)


	def _keyboard_closed(self):
		print 'My keyboard have been closed!'
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None


		#self.add_widget(self.layout)
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if self.check_lose() or keycode[1] == "r":
			self.reset()
		elif keycode[1] == "up":
			self.move_up()
			return True
		elif keycode[1] == "down":
			self.move_down()
			return True
		elif keycode[1] == "left":
			self.move_left()
			return True
		elif keycode[1] == "right":
			self.move_right()
			return True
		# Return True to accept the key. Otherwise, it will be used by
		# the system.
		return False

	def move_right(self):
		for i in range(self.bs):
			for j in range(self.bs)[::-1]:
				if self.hidden_board[(i,j)] != 0:
					if j +1 < self.bs:
						self.hidden_board[(i,j+1)] += self.hidden_board[(i,j)]
						self.hidden_board[(i,j)] = 1 
		self.redraw_board()
		if self.check_lose():
			self.colour_wrong()
		else:
			self.one_plus_score()

	def on_complete_saz (t):
		self.board[t].x = t[1]*(Window.width//bs)+(Window.width//bs)//2
		self.board[t].y = Window.height-(t[0]+1)*(Window.height//bs)

	def move_left(self):
		# swoopandzoom = {}
		for i in range(self.bs):
			for j in range(self.bs):
				if self.hidden_board[(i,j)] != 0:
					if j - 1 >= 0:
						# swoopandzoom[(i,j)] = [SwoopAndZoom(x=(j-1)*(Window.width//self.bs)+(Window.width//self.bs)//2), self.board[(i,j)]]
						# swoopandzoom[(i,j)][0].set_ij_bs((i, j),self.bs)
						self.hidden_board[(i,j-1)] += self.hidden_board[(i,j)]
						self.hidden_board[(i,j)] = 1

		# for k in swoopandzoom:
		# 	swoopandzoom[k][0].start(swoopandzoom[k][1])
		# 	reset_alpha = Animation(color=swoopandzoom[k][1].color[:3]+[1.0])
		# 	reset_alpha.start(swoopandzoom[k][1])


		self.redraw_board()
		if self.check_lose():
			self.colour_wrong()
		else:
			self.one_plus_score()

	def move_down(self):
		for i in range(self.bs):
			for j in range(self.bs)[::-1]:
				if self.hidden_board[(j, i)] != 0:
					if j +1 < self.bs:
						self.hidden_board[(j+1, i)] += self.hidden_board[(j, i)] 
						self.hidden_board[(j, i)] = 1
		self.redraw_board()
		if self.check_lose():
			self.colour_wrong()
		else:
			self.one_plus_score()

	def move_up(self):
		for i in range(self.bs):
			for j in range(self.bs):
				if self.hidden_board[(j,i)] != 0:
					if j - 1 >= 0:
						self.hidden_board[(j-1, i)] += self.hidden_board[(j,i)]
						self.hidden_board[(j, i)] = 1
		self.redraw_board()
		if self.check_lose():
			self.colour_wrong()
		else:
			self.one_plus_score()

	def check_lose(self):
		for i in range(self.bs):
			for j in range(self.bs):
				if self.hidden_board[(i, j)] % self.nonum == 0 and self.hidden_board[(i, j)] != 0:
					return True
		return False

	def redraw_board(self):
		for k in self.board:
			if self.hidden_board[k] != 0:
				self.board[k].color = (0.0, 1.0, 0.0, 1.0)
			self.board[k].text = str(self.hidden_board[k])
	
	def colour_wrong(self):
		for k in self.hidden_board:
			if self.hidden_board[k]%5 == 0 and self.hidden_board[k] != 0:
				self.board[k].color = (1.0, 0.0, 0.0, 1.0)

	def reset(self):
		for k in self.hidden_board:
			self.hidden_board[k] = 0
			self.board[k].text = '0'
			self.board[k].color = (1.0, 1.0, 1.0, 1.0)
		a = rand.randint(1,self.bs-2)
		b = rand.randint(1,self.bs-2)
		self.hidden_board[(a,b)] = 1
		self.board[(a,b)].text = '1'
		self.board[(a,b)].color = (0.0, 1.0, 0.0, 1.0)
		self.score_reset()


		
			

class MeApp(App):
	def build(self):
		return MeWidget()

if __name__ == '__main__':
	MeApp().run()