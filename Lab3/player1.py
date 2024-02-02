import paho.mqtt.client as mqtt
import numpy as np
import time
import sys
import pygame

# Button
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress: 
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

# TextBot
class TextBox():
    def __init__(self, x, y, width, height, textText='Text Box', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = '#add8e6'
        self.textSurface = pygame.Surface((self.width, self.height))
        self.textRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.textSurf = font.render(textText, True, (20, 20, 20))
        objects.append(self)
    def process(self):
        self.textSurface.fill(self.color)
        self.textSurface.blit(self.textSurf, [
            self.textRect.width/2 - self.textSurf.get_rect().width/2,
            self.textRect.height/2 - self.textSurf.get_rect().height/2
        ])
        screen.blit(self.textSurface, self.textRect)

# global variables
msg = None
usr_choice = None

def on_connect(client, userdata, flags, rc):
    client.subscribe("ece180d/test/rps/2", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    global msg, usr_choice
    msg = message.payload.decode()
    print('message recieved: ' + str(msg))
    if msg and usr_choice is not None:
        display_results(usr_choice, msg)
        msg = None
        usr_choice = None

#mqtt
client = mqtt.Client(client_id="player1")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 1000, 700
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 40)

objects = []

game_record = [0,0,0]
b_width = 400
b_height = 100
b_init_h = 140

def display_choice(user_input):
    choices = ['Rock', 'Paper', 'Scissors']
    text = 'You chose ' + choices[user_input - 1]
    TextBox((width - 700)/2, 460, 700, b_height, text)

def display_results(user_input, msg_input):
    choices = ['Rock', 'Paper', 'Scissors']
    other_choice = choices[int(msg_input) - 1]
    result = 0
    diff = user_input - int(msg_input)
    if diff == 0:
        result = 0
        game_record[0]+=1
    elif (diff % 3) == 1: 
        result = 1
        game_record[1]+=1
    else:
        result = 2
        game_record[2]+=1

    game_results = ['Tie Game!','You Win!','Player2 Wins!']
    text = 'Player 2 chose ' + other_choice + '. ' + game_results[result]
    TextBox((width - 700)/2, 540, 700, b_height, text)
    wl_record = 'W: ' + str(game_record[1]) + ' T: ' + str(game_record[0]) + ' L: ' + str(game_record[2])
    TextBox((width - 700)/2, 620, 700, b_height, wl_record)

def rockFunc():
    global usr_choice
    global msg
    usr_choice = 1
    client.publish("ece180d/test/rps/1", 1, qos=1)
    display_choice(usr_choice)
    if msg and usr_choice is not None:
        display_results(usr_choice, msg)
        msg = None
        usr_choice = None

def paperFunc():
    global usr_choice
    global msg
    usr_choice = 2
    client.publish("ece180d/test/rps/1", 2, qos=1)
    display_choice(usr_choice)
    if msg and usr_choice is not None:
        display_results(usr_choice, msg)
        msg = None
        usr_choice = None

def scissorsFunc():
    global usr_choice
    global msg
    usr_choice = 3
    client.publish("ece180d/test/rps/1", 3, qos=1)
    display_choice(usr_choice)
    if msg and usr_choice is not None:
        display_results(usr_choice, msg)
        msg = None
        usr_choice = None

Button((width - b_width)/2, b_init_h, b_width, b_height, 'Rock', rockFunc)
Button((width - b_width)/2, b_init_h + b_height + 10, b_width, b_height, 'Paper', paperFunc)
Button((width - b_width)/2, b_init_h + 2 * b_height + 20, b_width, b_height, 'Scissors', scissorsFunc  )
TextBox((width - 700)/2, 30, 700, b_height, 'Choose Rock Paper or Scissors!')
while True:
    screen.fill((173, 216, 230))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for object in objects:
        object.process()
    pygame.display.flip()
    fpsClock.tick(fps)