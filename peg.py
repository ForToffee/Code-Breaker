from gpiozero import RGBLED

class Peg(RGBLED):
	pass

	colours = []
	current_colour = -1
	last_colour = -1
	winning_colour = (0,0,0)
	locked = False
	
	def reset(self):
		self.last_colour = -1
		self.winning_colour = (0,0,0)
		self.locked = False
		self.current_colour = -1
		self.value = (0,0,0)
	
	def clear(self):
		del self.colours[self.current_colour]
		self.last_colour = min(self.last_colour, len(self.colours) - 1)
		self.current_colour = -1
		self.value = (0,0,0)
		
	def show(self):
		if self.current_colour < 0:
			self.current_colour = max(0,self.last_colour)
		self.value = self.colours[self.current_colour][1]
		self.last_colour = self.current_colour
	
	def show_winner(self):
		self.value = self.winning_colour
	
	def show_next(self):
		self.current_colour += 1
		if self.current_colour >= len(self.colours):
			self.current_colour = 0
		self.show()

	def show_prev(self):
		self.current_colour -= 1
		if self.current_colour < 0 :
			self.current_colour = len(self.colours) - 1
		self.show()
		
	def is_correct(self):
		return self.winning_colour == self.colours[self.current_colour][1]
	
	def colour_name(self):
		return self.colours[self.current_colour][0]
