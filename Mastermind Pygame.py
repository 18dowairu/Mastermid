# mastermind in pygame!
from typing import Self
import pygame
import random

pygame.init()

width = 450
height = 800
timer = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Mastermind")
font = pygame.font.Font('freesansbold.ttf', 18)
# game variables
backgroundColour = (0, 51, 51)
white = 'white'
grey = 'gray'
black = 'black'
red = 'red'
orange = 'orange'
yellow = 'yellow'
green = 'green'
blue = 'blue'
purple = 'purple'
# game lists
choiceColours = [red, orange, yellow, green, blue, purple]
answerColours = [random.choice(choiceColours), random.choice(choiceColours),
                 random.choice(choiceColours), random.choice(choiceColours)]
guessColours = [[white, white, white, white],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey],
                [grey, grey, grey, grey]]
fbColours = [[grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey],
             [grey, grey, grey, grey]]
selected = 0
turn = 0
selectedColour = (26, 230, 204)
solvedColour = (26, 230, 204)
solved = False                                                                     
menu = True
leaderboard = False
menu_img = pygame.transform.scale(pygame.image.load('MASTERMIND.png'), (width/2, height/2))
mainmenu_img = pygame.transform.scale(pygame.image.load('LOGO.jpeg'), (width, height/4))
check = False
win = False
lose = False
start = False
mainMenu = True
scoreAdded = False
class players:
    def __init__(self,name,score):
        self.name = name
        self.score = score
    def getName(self):
        return self.name
    def getScore(self):
        return self.score

        

# class for Buttons
class buttons:
    def __init__(self, text, coords, size):
        self.text = text
        self.coords = coords
        self.size = size
        self.rect = pygame.rect.Rect(self.coords, self.size)

    def draw(self):
        if self.rect.collidepoint(mouse_coords) and mouse_buttons[0]:
            colour = 'light blue'
        elif self.rect.collidepoint(mouse_coords):
            colour = 'light grey'
        else:
            colour = white
        pygame.draw.rect(screen, colour, self.rect)
        pygame.draw.rect(screen, black, self.rect, 1)
        screen.blit(font.render(self.text, True, black),
                    (self.coords[0] + self.size[0] / 4, self.coords[1] + self.size[1] / 3))


# draw the screen components
def drawScreen():
    # active turn rectangle
    pygame.draw.rect(screen, 'light grey', [0, 10 * height / 13 - turn * height / 13, width, height / 13])
    # guess circles
    for i in range(10):
        for j in range(4):
            pygame.draw.circle(screen, guessColours[i][j],
                               ((width / 5 * (j + 1.5)), ((11 * height / 13) - (height / 13 * i) - height / 26)),
                               height / 30)
    # feedback circles
    for i in range(10):
        for j in range(4):
            row = j // 2
            col = j % 2
            pygame.draw.circle(screen, fbColours[i][j],
                               (25 + (col * width / 12),
                                ((11 * height / 13) - (height / 13 * i) - (height / 26 * (row + 0.5)))),
                               height / 60)
    # answer circles
    for i in range(4):
        pygame.draw.circle(screen, answerColours[i], (width / 5 * (i + 1.5), height / 26), height / 30)
    # answer cover rectangle
    if not solved:
        pygame.draw.rect(screen, solvedColour, [width / 5, 0, 4 * width / 5, height / 13])
    # options colors to select and selected circle
    pygame.draw.circle(screen, selectedColour, (width / 7 * (selected + 1), 11.5 * height / 13), height / 26)
    for i in range(6):
        pygame.draw.circle(screen, choiceColours[i], (width / 7 * (i + 1), 11.5 * height / 13), height / 30)
    # buttons 
    menuButton.draw()
    submitButton.draw()
    restartButton.draw()
    # horizontal lines
    for i in range(14):
        pygame.draw.line(screen, white, (0, height / 13 * i), (width, height / 13 * i), 3)
    # vertical lines
    pygame.draw.line(screen, white, (width / 5, 0), (width / 5, 11 * height / 13), 3)
    pygame.draw.line(screen, white, (0, 0), (0, height), 3)
    pygame.draw.line(screen, white, (width - 1, 0), (width - 1, height), 3)

def drawMainMenu():
    pygame.draw.rect(screen, grey, [0,0, width , height])
    displayRect = pygame.Rect(width/4, height/2.5, width/2, height/8)
    inputRect = pygame.Rect(width/4, height/2, width/2, height/20)
    pygame.draw.rect(screen, white, inputRect)
    screen.blit(mainmenu_img, (0, 0))
    screen.blit(font.render(playerName, True, black), (inputRect))
    screen.blit(font.render('Enter your player name:', True, black), (displayRect))
    startButton.draw()
def calculateScore():
    global scoreAdded
    score = 10 - turn
    print('your score is', score)
    scoreAdded = True
    return score

def drawMenu():
    pygame.draw.rect(screen, white, [width / 4 - 5, height / 4 - 5, width / 2 + 10, height / 2 + 10])
    screen.blit(menu_img, (width/4, height/4))
    leaderboardButton.draw()

def drawLeaderboard():
    score = calculateScore()
    name = playerName
    pygame.draw.rect(screen, white, [width / 4 - 5, height / 4 - 5, width / 2 + 10, height / 2 + 10])
    for i, (name, score) in enumerate(leaderboardDisplay):
        text = (f"{i + 1}. {name}: {score}")
        screen.blit(font.render(text, True, black), (width / 4 + 10, height / 4 + i * 20))

  
    
def checkGuess():
    global solved, menu, win
    checkTurn = guessColours[turn]
    responses = [grey, grey, grey, grey]
    responseIndex = 0
    for i in range(4):
        if checkTurn[i] == answerColours[i]:
            responses[responseIndex] = red
            responseIndex += 1
            print(f'{checkTurn[i]} is in the right spot')
        elif checkTurn[i] in answerColours:
            guessCount = checkTurn.count(checkTurn[i])
            answerCount = answerColours.count(checkTurn[i])
            onlyInout = (guessCount == 1) # true or false if this guess only appears once
            severalOutputs = (answerCount >= guessCount) # t or f if more in ans than guess
            guessIndexes = []
            answerIndexes = []
            for j in range(4):
                if checkTurn[j] == checkTurn[i] and checkTurn[j] != answerColours[j]:
                    guessIndexes.append(j)
                if answerColours[j] == checkTurn[i] and checkTurn[j] != answerColours[j]:
                    answerIndexes.append(j)
            count_this = guessIndexes.index(i) < len(answerIndexes)
            if onlyInout or severalOutputs or count_this:
                responses[responseIndex] = white
                responseIndex += 1
                print(f'{checkTurn[i]} is in the answer but wrong spot')
    random.shuffle(responses)
    print(responses)
    fbColours[turn] = responses
    if responses.count(red) == 4:
        solved = True
        menu = True
        win = True

leaderboardDisplay = []
playerName = ''
run = True
menuButton = buttons('Menu', (0, 0), (width / 5, height / 13))
submitButton = buttons('Submit', (0, 12 * height / 13), (width / 2, height / 13))
restartButton = buttons('Restart', (width / 2, 12 * height / 13), (width / 2, height / 13))
leaderboardButton = buttons("Leaderboard", (width/4, 10* height/13), (width / 2, height / 14))
loseButton = buttons('  You lose', (width/4, 2* height/13), (width / 2, height / 14))
winButton = buttons('   You win', (width/4, 2* height/13), (width / 2, height / 14))
startButton = buttons("      Start", (width/4, 9* height/13), (width / 2, height / 14))
while run:
    timer.tick(fps)
    screen.fill(backgroundColour)
    mouse_coords = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    # print(mouse_pressed)
    if mainMenu:
        drawMainMenu()
    if not mainMenu:
        drawScreen()
        if menu or win or lose:
            drawMenu()
            if win:
                winButton.draw()
                solved = True
            elif lose:
                loseButton.draw()
                solved = True
            if (win or lose) and not scoreAdded:
                leaderboardDisplay.append((playerName, calculateScore()))
                leaderboardDisplay.sort(key=lambda x: x[1], reverse=True)
                scoreAdded = True
            if leaderboard and menu:
                drawLeaderboard()
    if check:
        checkGuess()
        turn += 1
        for i in range(4):
            try:
                guessColours[turn][i] = white
            except:
                menu = True
                lose = True
        check = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                playerName = playerName[0:-1]
            else:
                playerName += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartButton.rect.collidepoint(event.pos):
                playerName = ''
                mainMenu = True
                scoreAdded = False
                menu = True
                turn = 0
                solved = False
                lose = False
                win = False
                answerColours = [random.choice(choiceColours), random.choice(choiceColours),
                                 random.choice(choiceColours), random.choice(choiceColours)]
                guessColours = [[white, white, white, white],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey],
                                [grey, grey, grey, grey]]
                fbColours = [[grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey],
                             [grey, grey, grey, grey]]
            elif startButton.rect.collidepoint(event.pos):
                mainMenu = False
            elif menuButton.rect.collidepoint(event.pos):
                if not menu:
                    menu = True
                else:
                    menu = False
            if leaderboardButton.rect.collidepoint(event.pos):
                if not leaderboard:
                    leaderboard = True
                else:
                    leaderboard = False
            if not menu:
                if width / 14 < event.pos[0] < 13 * width / 14 \
                        and 11 * height / 13 < event.pos[1] < 12 * height / 13:
                    x_pos = event.pos[0] // (width / 14)
                    selected = int((x_pos - 1) // 2)
                elif width / 5 < event.pos[0] \
                        and (10 - turn) * height / 13 < event.pos[1] < (11 - turn) * height / 13:
                    x_pos = int(event.pos[0] // (width / 5))
                    guessColours[turn][x_pos - 1] = choiceColours[selected]
                elif submitButton.rect.collidepoint(event.pos):
                    if white not in guessColours[turn]:
                        check = True

    pygame.display.flip()
pygame.quit()