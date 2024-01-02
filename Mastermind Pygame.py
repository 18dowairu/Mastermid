# mastermind in pygame!
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
menu = False
leaderboard = False
menu_img = pygame.transform.scale(pygame.image.load('MASTERMIND.png'), (width/2, height/2))
check = False


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


def drawMenu():
    pygame.draw.rect(screen, white, [width / 4 - 5, height / 4 - 5, width / 2 + 10, height / 2 + 10])
    screen.blit(menu_img, (width/4, height/4))
    leaderboardButton.draw()

def drawLeaderboard():
    pygame.draw.rect(screen, white, [width / 2, height / 2, width / 2 + 10, height / 2 + 10])

def checkGuess():
    global solved, menu
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


run = True
menuButton = buttons('Menu', (0, 0), (width / 5, height / 13))
submitButton = buttons('Submit', (0, 12 * height / 13), (width / 2, height / 13))
restartButton = buttons('Restart', (width / 2, 12 * height / 13), (width / 2, height / 13))
leaderboardButton = buttons("Leaderboard", (width-180, 3), (width / 2, height / 14))
while run:
    timer.tick(fps)
    screen.fill(backgroundColour)
    mouse_coords = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    # print(mouse_pressed)
    drawScreen()
    if menu:
        drawMenu()
        if leaderboard:
            drawLeaderboard()
    if check:
        checkGuess()
        turn += 1
        for i in range(4):
            guessColours[turn][i] = white
        check = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartButton.rect.collidepoint(event.pos):
                menu = False
                turn = 0
                solved = False
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
            elif menuButton.rect.collidepoint(event.pos):
                if not menu:
                    menu = True
                    if menu == True and leaderboardButton.rect.collidepoint(event.pos):
                        leaderboard = True
                else:
                    menu = False
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