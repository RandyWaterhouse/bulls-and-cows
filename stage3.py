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
    
########################################################################
# class for game
class BullsAndCowsGame:

    def __init__(self):
        # initialization: determine random secret (5 of 8 colors, randomly placed):
        self.secret = list(map(str, range(1, 9)))
        random.shuffle(self.secret)
        self.secret = [int(_) for _ in self.secret[:5]]
        self.G = []  # guesses so far
        self.S = []  # survivors
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

G = BullsAndCowsGame()
print(G.CheckGuess([1, 2, 3, 4, 5]))
print(G.CheckGuess([1, 2, 3, 0, 5]))
print(G.CheckGuess([1, 2, 3, 4, 5]))
