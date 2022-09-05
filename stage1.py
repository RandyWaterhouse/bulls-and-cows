    
def GetFeedback(secret, guess):
    bulls = sum([secret[i] == guess[i] for i in range(5)])
    reduced_secret = [secret[i] for i in range(5) if secret[i] != guess[i]]
    reduced_guess = [guess[i] for i in range(5) if secret[i] != guess[i]]
    cows = sum([color in reduced_guess for color in reduced_secret])
    return 'B' * bulls + 'C' * cows 


print(GetFeedback([1, 2, 3, 4, 5], [1, 2, 3, 5, 4]))
print(GetFeedback([2, 3, 4, 5, 6], [1, 2, 3, 5, 4]))
print(GetFeedback([1, 2, 3, 4, 5], [8, 7, 6, 5, 4]))
print(GetFeedback([8, 7, 6, 5, 4], [3, 4, 1, 6, 7]))

# slides:
print("slides:", GetFeedback([4, 1, 7, 8, 5], [8, 2, 7, 4, 3]))
