import random
import itertools

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
