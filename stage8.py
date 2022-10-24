#
# "Bulls and Cows", graphics version
#

import pygame
from pygame.locals import *
import math
import random
import time
import itertools

########################################################################
# constants
MAIN_WIDTH = 400
MAIN_HEIGHT = 850
MENUE_WIDTH = 120
TWIDTH = MAIN_WIDTH + MENUE_WIDTH
THEIGHT = MAIN_HEIGHT
VERSION = "1.0"
FONTSIZE = 20
PIN_SPACING_HORIZ = 40
PIN_OFFSET_HORIZ = 45
PIN_SPACING_VERT = 45
PIN_OFFSET_VERT = 120
COLOR_SEQ = ["GREY1", "RED", "SUNYELLOW", "DARKBLUE", "MEDIUMGREEN", "WHITE",
             "ORANGE", "BROWN", "PINK"]
MAP1 = {i: COLOR_SEQ[i] for i in range(9)}
MAP2 = {v: k for k, v in MAP1.items()}

########################################################################
# define colors for graphics output:
COLORS = {"WHITE": (255, 255, 255), "RED": (255, 0, 0), "GREEN": (0, 255, 0),
          "BLUE": (0, 0, 255), "BLACK": (0, 0, 0), "YELLOW": (255, 255, 0),
          "LIGHTBLUE": (0, 125, 227), "GREY1": (120, 120, 120),
          "GREY2": (224, 224, 224), "LIGHTBLUE": (102, 178, 255),
          "LIGHTRED": (255, 153, 153), "LIGHTYELLOW": (255, 255, 153),
          "PINK": (255, 51, 255), "DARKBLUE": (0, 0, 153),
          "LAVENDER": (204, 153, 255), "LIGHTGREEN": (153, 255, 204),
          "BROWN": (102, 51, 0), "OLIVE": (153, 153, 0), "DARKGREY": (105, 105, 105),
          "EARTHBLUE": (0, 128, 255), "MOONGREY": (224, 224, 224),
          "SUNYELLOW": (255, 255, 0), "MARSRED": (255, 99, 71),
          "VENUSYELLOW": (245, 222, 179), "MERCURYGREY": (211, 211, 211),
          "JUPITERRED" : (255, 160, 122), "SATURNGREY": (240,230,140),
          "URANUSBLUE": (135,206,250), "NEPTUNBLUE": (0, 0, 255),
          "MEDIUMGREEN": (60,179,113), "CRIMSON": (220, 20, 60),
          "BUTTONRED": (250, 50, 50), "BUTTONGREEN": (64, 209, 64),
          "CARD1": (224, 224, 224), "CARD2": (200, 190, 150),
          "ORANGE": (255, 128, 0), "VIOLET": (102, 0, 204)}

########################################################################
# helper functions
def draw_text(surface, font, text, position, color):
    # draw user-defined text in pygame graphics surface
    lable = font.render(text, 1, color)
    surface.blit(lable, position)
    
######################################################################
# Button class for control section, PyGame doesn't have ready-to-use
# buttons or similar:
class Button():

    def __init__(self, width, height, text, color, tcolor):
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.tcolor = tcolor

    def SetText(self, text):
        self.text = text

    def PlaceButton(self, surface, x, y):
        self.x = x
        self.y = y
        surface = self.DrawButton(surface, x, y)
        surface = self.ButtonText(surface, x, y)

    def DrawButton(self, surface, x, y):
        pygame.draw.rect(surface, self.color, (x, y, self.width, self.height), 0)
        return surface

    def ButtonText(self, surface, x, y):
        font_size = int(self.width // len(self.text))
        font = pygame.font.SysFont("Arial", FONTSIZE)
        text = font.render(self.text, 1, self.tcolor)
        surface.blit(text, ((x + self.width/2) - text.get_width()/2, (y + self.height/2) - text.get_height()/2))
        return surface

    def IsPressed(self, mouse):
        return mouse[0] > self.x and \
               mouse[1] > self.y and \
               mouse[0] <= self.x + self.width and \
               mouse[1] < self.y + self.height

#################################################################################
# Class for pins, we use 15 rows of 5 pins each, pins are represented by circles:
class Pin():

    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.is_selected = False

    def SetColor(self, color):
        self.color = color

    def GetColor(self):
        return self.color

    def PlacePin(self, surface, x, y):
        self.x = x
        self.y = y
        surface = self.DrawPin(surface, x, y)
        
    def DrawPin(self, surface, x, y):
        pygame.draw.circle(surface, COLORS[self.color], (x, y), self.radius, 0)
        if self.is_selected:
            pygame.draw.circle(surface, COLORS["VIOLET"], (x, y), self.radius, 3)
        return surface

    def SelectPin(self):
        self.is_selected = True

    def UnselectPin(self):
        self.is_selected = False

    def IsPressed(self, mouse):
        return (mouse[0] - self.x)**2 + (mouse[1] - self.y)**2 <= self.radius**2

#################################################################################
# Class for pin colors, we use 8 colors to select from
class PinColor():

    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.is_available = True

    def GetColor(self):
        return self.color

    def PlacePinColor(self, surface, x, y):
        self.x = x
        self.y = y
        surface = self.DrawPinColor(surface, x, y)
        
    def DrawPinColor(self, surface, x, y):
        pygame.draw.circle(surface, COLORS[self.color], (x, y), self.radius, 0)
        return surface

    def IsPressed(self, mouse):
        return (mouse[0] - self.x)**2 + (mouse[1] - self.y)**2 <= self.radius**2

########################################################################
# class for game
class BullsAndCowsGame:

    def __init__(self):
        # initialization: determine random secret (5 of 8 colors, randomly placed):
        self.secret = list(map(str, range(1, 9)))
        random.shuffle(self.secret)
        self.secret = [int(_) for _ in self.secret[:5]]
        self.G = []   # guesses so far
        self.S = []   # survivors
        for comb in itertools.combinations(list(range(1, 9)), 5):
            for perm in itertools.permutations(comb):
                self.S.append(tuple(perm))

    def CutSurvivors(self, guess, feedback):
        S_guess = set(guess)
        black, white, n = feedback.count('B'), feedback.count('W'), len(feedback)
        self.S = [s for s in self.S if len(S_guess.intersection(set(s))) == n and \
                    sum([guess[i] == s[i] for i in range(5)]) == black]

    def GetGuess(self):
        return random.choice(self.S)

    def GetFeedback(secret, guess):
        bulls = sum([secret[i] == guess[i] for i in range(5)])
        reduced_secret = [secret[i] for i in range(5) if secret[i] != guess[i]]
        reduced_guess = [guess[i] for i in range(5) if secret[i] != guess[i]]
        cows = sum([color in reduced_guess for color in reduced_secret])
        return 'B' * bulls + 'C' * cows 

    def CheckGuess(self, guess):
        # check guess submitted by player; return values:
        # status: 0 = valid guess, < 0 = invalid guess
        # msg: text message to display
        # feedback: sequence of bulls and cows
        if 0 in guess:
            return -1, "Please submit 5 colors", ""
        if guess in self.G:
            return -2, "Are you sure? You already tried that...", ""
        self.G.append(guess)
        feedback = self.GetFeedback(guess)
        self.CutSurvivors(guess, feedback)
        if feedback == "BBBBB":
            msg = "You won! Great job!"
        else:
            msg = "You have " + str(feedback.count('B')) + " bull(s) and " + \
                  str(feedback.count('C')) + " cows(s)!"
        return 0, msg, feedback
    
######################################################################
# pygame main loop:
def mainloop(surface):

    # Buttons:
    button_submit =   Button(80, 40, "submit", COLORS["BUTTONGREEN"], COLORS["BLACK"])
    button_autoplay = Button(80, 40, "autoplay", COLORS["SUNYELLOW"], COLORS["BLACK"])
    button_restart =  Button(80, 40, "restart", COLORS["EARTHBLUE"], COLORS["BLACK"])
    button_quit =     Button(80, 40, "quit", COLORS["BUTTONRED"], COLORS["BLACK"])

    # Pin colors:
    pin_colors = [PinColor(12, COLOR_SEQ[i]) for i in range(1, 9)]

    # Pins:
    pins = {(row, col): Pin(12, COLOR_SEQ[0]) for row in range(15) for col in range(5)}

    G = BullsAndCowsGame()
    
    # loop until user event:
    msg = ""
    active_row = 0
    selected_pin = pins[(active_row, 0)]
    selected_pin.SelectPin()
    feedbacks = {}
    n_guess = 0
    start_time = time.time()
    while True:
        # Event handler:
        for event in pygame.event.get():
            # pygame event handler
            if event.type == QUIT:
                # graphics window is closed
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                # key is pressed
                if event.key in [K_ESCAPE, K_q]:
                    pygame.quit()
                    return
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_quit.IsPressed((x, y)):
                    pygame.quit()
                    return
                if button_restart.IsPressed((x, y)):
                    G = BullsAndCowsGame()
                    active_row = 0
                    n_guess = 0
                    msg = ""
                    for pin in pins.values():
                        pin.SetColor(COLOR_SEQ[0])
                        pin.UnselectPin()
                    selected_pin = pins[(active_row, 0)]
                    selected_pin.SelectPin()
                    feedbacks = {}
                    start_time = time.time()
                if button_submit.IsPressed((x, y)):
                    guess = [MAP2[pins[(active_row, col)].GetColor()] for col in range(5)]
                    status, msg, feedback = G.CheckGuess(guess)
                    if status == 0:
                        feedbacks[active_row] = feedback
                        n_guess += 1
                        active_row += 1
                        selected_pin = pins[(active_row, 0)]
                        selected_pin.SelectPin()
                        if active_row > 14:
                            msg = "Sorry, you lost, you had 15 tries to solve the game!"
                            active_row = 0
                if button_autoplay.IsPressed((x, y)):
                    # finish game with "autoplay":
                    while True:
                        guess = G.GetGuess()
                        for col in range(5):
                            pins[(active_row, col)].SetColor(COLOR_SEQ[guess[col]])
                        status, msg, feedback = G.CheckGuess(guess)
                        feedbacks[active_row] = feedback
                        n_guess += 1
                        active_row += 1
                        msg = "Autoplay did the job for you..."
                        if feedback == "BBBBB":
                            break
                for col in range(5):
                    pin = pins[(active_row, col)]
                    if pin.IsPressed((x, y)):
                        pin.SelectPin()
                        selected_pin = pin
                        for col2 in range(5):
                            if col == col2:
                                continue
                            pin2 = pins[(active_row, col2)]
                            pin2.UnselectPin()
                if selected_pin != None:
                    for col in range(8):
                        pin_color = pin_colors[col]
                        if pin_color.IsPressed((x, y)):
                            selected_pin.SetColor(pin_color.GetColor())
                            selected_pin.UnselectPin()
                            for col2 in range(5):
                                pin2 = pins[(active_row, col2)]
                                if pin2 != selected_pin and pin2.GetColor() == selected_pin.GetColor():
                                    pin2.SetColor(COLOR_SEQ[0])
                            for col2 in range(4):
                                if pins[(active_row, col2)] == selected_pin:
                                    selected_pin = pins[(active_row, col2+1)]
                                    selected_pin.SelectPin()
                                    break

        # Draw on surface:                
        surface.fill(COLORS["GREY2"], (0, 0, TWIDTH, THEIGHT))
        pygame.draw.line(surface, COLORS["BLACK"], (MAIN_WIDTH, 0), (MAIN_WIDTH, THEIGHT-40), 4)
        pygame.draw.line(surface, COLORS["BLACK"], (0, THEIGHT-40), (TWIDTH, THEIGHT-40), 4)
        draw_text(surface, helv20, "Select pin, then color:", (50, 10), COLORS["BLUE"])
        draw_text(surface, helv24, "Guesses:", (MAIN_WIDTH+10, 10), COLORS["BLUE"])
        draw_text(surface, helv24, str(n_guess), (MAIN_WIDTH+50, 40), COLORS["BLUE"])
        draw_text(surface, helv20, "Elapsed", (MAIN_WIDTH+10, 260), COLORS["BLUE"])
        draw_text(surface, helv20, "time:", (MAIN_WIDTH+10, 290), COLORS["BLUE"])
        elapsed = int(time.time() - start_time)
        minutes, seconds = elapsed // 60, elapsed % 60
        draw_text(surface, helv20, str(minutes).zfill(2) + ":" + str(seconds).zfill(2), (MAIN_WIDTH+60, 290), COLORS["BLUE"])
        draw_text(surface, helv24, msg, (10, THEIGHT-30), COLORS["BUTTONRED"])
        button_submit.PlaceButton(surface, MAIN_WIDTH+20, 105)
        button_autoplay.PlaceButton(surface, MAIN_WIDTH+20, 450)
        button_restart.PlaceButton(surface, MAIN_WIDTH+20, MAIN_HEIGHT-160)
        button_quit.PlaceButton(surface, MAIN_WIDTH+20, MAIN_HEIGHT-100)
        for (row, col), pin in pins.items():
            pin.PlacePin(surface, PIN_OFFSET_HORIZ + PIN_SPACING_HORIZ * col, PIN_OFFSET_VERT + PIN_SPACING_VERT * row)
        pygame.draw.circle(surface, COLORS["GREEN"], (PIN_OFFSET_HORIZ // 2 - 5, PIN_OFFSET_VERT +  PIN_SPACING_VERT * active_row), 5)
        for col, pin_color in enumerate(pin_colors):
            pin_color.PlacePinColor(surface, 25 + PIN_SPACING_HORIZ * col, 60)
        for row, feedback in feedbacks.items():
            x = PIN_OFFSET_HORIZ + PIN_SPACING_HORIZ * 5 
            y = PIN_OFFSET_VERT + PIN_SPACING_VERT * row
            for _ in range(feedback.count('B')):
                pygame.draw.circle(surface, COLORS["BLACK"], (x, y), 8, 0)
                x += 30
            for _ in range(feedback.count('C')):
                pygame.draw.circle(surface, COLORS["WHITE"], (x, y), 8, 0)
                x += 30
        pygame.display.flip()
        
######################################################################
# main program:
if __name__ == "__main__":
    pygame.init()
    helv20 = pygame.font.SysFont("Helvetica", 20)
    helv24 = pygame.font.SysFont("Helvetica", 24)
    helv_scores = pygame.font.SysFont("Helvetica", 18)
    fpsClock = pygame.time.Clock()
    surface = pygame.display.set_mode((TWIDTH, THEIGHT))
    surface.set_alpha(None)
    pygame.display.set_caption("Bulls and Cows, v" + VERSION + ", by Peter U., 2022")

    # pygame main loop:
    mainloop(surface)

#G = BullsAndCowsGame()
#print(G.CheckGuess([1, 2, 3, 4, 5]))
#print(G.CheckGuess([1, 2, 3, 0, 5]))
#print(G.CheckGuess([1, 2, 3, 4, 5]))

