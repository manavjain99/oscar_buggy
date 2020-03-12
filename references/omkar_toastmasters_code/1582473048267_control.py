import sys, tty, termios, time
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
GPIO.setup(5, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(6, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(19, GPIO.OUT, initial=GPIO.HIGH)

def getkey():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def car():
    while True:
        key = getkey()
        if key == 's': #Down arrow
            print "Down"
            Backward()
        elif key == 'w': #Up arrow
            print "Up"
            Forward()
        elif key == 'a': 
            print "left"
            Left()
        elif key == 'd': 
            print "Right"
            Right()
        elif key == 'c':
			print "Centre"
			Centre()
	elif key == ' ': 
            print "Brake"
            Brake()
        elif key == 'q': #Quit
            print "That's It"
            break
def Forward():
    GPIO.output(5,True)  
    sleep(1)
    GPIO.output(6,False) 
def Backward():
    GPIO.output(6,True)  
    sleep(1)
    GPIO.output(5,False)   
def Right():
	GPIO.output(13,False) 
	sleep(1)
	GPIO.output(13,True)
	GPIO.output(19,True)
def Left():
	GPIO.output(19,False) 
	sleep(1)
	GPIO.output(19,True)
	GPIO.output(13,True) 
def Centre():
	GPIO.output(13,False) 
	sleep(2)
def Brake():
	GPIO.output(5,True)
	GPIO.output(6,True)
    
car()
