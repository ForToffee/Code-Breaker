from time import sleep
from peg import Peg
from random import choice
import Adafruit_CharLCD as LCD


# Initialize the LCD 
lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(1.0,1.0,1.0)

pegs = [Peg(red=17, green=21, blue=22), 
		Peg(red=18, green=23, blue=24), 
		Peg(red=10, green=9, blue=11),
		Peg(red=25, green=8, blue=7)]

colours_4 = [["Red", (1,0,0) ],
			["Green", (0,1,0) ],
			["Blue", (0,0,1) ],
			["White", (1,1,1) ]]

colours_8 = colours_4 + [
			["Orange", (1,0.4,0) ],
			["Cyan", (0,1,1) ],
			["Purple", (0.5,0,0.5) ],
			["Yellow", (1,0.75,0) ]]


mode = 0
MAX_MODE = 3

def gameMode():	
	global mode
	refresh = True
	prompt = "Select Mode:\n"
	
	while not lcd.is_pressed(LCD.SELECT):
		if lcd.is_pressed(LCD.DOWN):
			mode = min(mode + 1, MAX_MODE)
			refresh = True
		if lcd.is_pressed(LCD.UP):
			mode = max(mode - 1, 0)
			refresh = True

		if refresh:
			refresh = False
			lcd.clear()
			
			if mode == 0:
				lcd.message(prompt + "4 unique colours")
			elif mode == 1:
				lcd.message(prompt + "4 colours (any)")
			elif mode == 2:
				lcd.message(prompt + "8 unique colours")
			elif mode == 3:
				lcd.message(prompt + "8 colours (any)")

def gameSetup():
	lcd.clear()
	lcd.message("Randomising\n  Colours")
	sleep(0.5)

	chosen_colours = []
	if mode == 0 or mode == 1:
		colours = colours_4
	elif mode == 2 or mode == 3:
		colours = colours_8
	print colours
	
	for peg in pegs:
		peg.reset()
		winner = choice(colours)[1]
		
		if mode == 0 or mode == 2:
			while winner in chosen_colours:
				winner = choice(colours)[1]
			chosen_colours.append(winner)

		peg.colours = list(colours)
		peg.winning_colour = winner
		
	lcd.clear()
	lcd.message("Ready")
	sleep(0.5)

def setPegs(attempt):
	refresh = True
	id = 0
	prompt = "Attempt " + str(attempt) + " of 10\n"
	pegs[id].show()
	while True:
		if lcd.is_pressed(LCD.UP):
			if not pegs[id].locked:
				pegs[id].show_next()
				refresh = True
		if lcd.is_pressed(LCD.DOWN):
			if not pegs[id].locked:
				pegs[id].show_prev()
				refresh = True
		if lcd.is_pressed(LCD.LEFT):
			id = max(0, id - 1)
			refresh = True
			pegs[id].show()
		if lcd.is_pressed(LCD.RIGHT):
			id = min(3, id + 1)
			refresh = True
			pegs[id].show()
		
		if lcd.is_pressed(LCD.SELECT):
			for peg in pegs:
				if peg.current_colour == -1:
					lcd.clear()
					lcd.message("All lights must\nhave a colour")
					sleep(2)
					refresh = True 
					break
			if refresh == False:
				break

		
		if refresh:
			refresh = False
			lcd.clear()
			if pegs[id].locked:
				lcd.message(prompt + "LED " + str(id + 1) + ": Correct!")
			else:
				lcd.message(prompt + "LED " + str(id + 1) + ": " + pegs[id].colour_name())

def checkPegs(attempt):
	correct_pegs = 0
	n = 0
	for peg in pegs:
		peg.locked = peg.is_correct()
		if not peg.locked:
			peg.clear()
		else:
			correct_pegs += 1
		n+=1
	if correct_pegs == 4:
		lcd.clear()
		lcd.message("WELL DONE! Only\n" + str(attempt) + " attempts")
		sleep(5)
		return True
	elif correct_pegs < 4 and attempt == 10:
		lcd.clear()
		lcd.message("BAD LUCK! Only\n" + str(correct_pegs) + " are correct")
		sleep(2)
	else:
		lcd.clear()
		lcd.message(str(correct_pegs) + " are correct\n" + str(10 - attempt) + " attempts left")
		sleep(2)

def play():
	for attempt in range(1, 11):
		setPegs(attempt)
		if checkPegs(attempt):
			break

while True:				
	gameMode()
	gameSetup()
	play()
	
