# pygame
import pygame
import random
pygame.init()
pygame.font.init()
pygame.display.set_caption("Battleship")
myfont = pygame.font.SysFont("fresansttf", 100)

#engine
def ship(size):
    ship.row = random.randrange(0,9)
    ship.col = random.randrange(0,9)
    ship.size = size
    ship.orientation = random.choice(["h","v"])
    ship.indexes = compute_indexes()
    return ship.row, ship.col, ship.orientation, ship.indexes, ship.size

def compute_indexes():
    start_index = ship.row * 10 + ship.col
    if ship.orientation == "h":
        return [start_index + i for i in range(ship.size)]
    elif ship.orientation == "v":
        return [start_index + i*10 for i in range(ship.size)]

def player():
    player.ships = []
    player.search = ["U" for i in range(100)] # U for unknown
    place_ships(sizes = [5,4,3,3,2])
    list_of_lists = [ship[3] for ship in player.ships]
    player.indexes = [index for sublist in list_of_lists for index in sublist]
    return player.ships, player.search

def place_ships(sizes):
    sizecount = 5
    if sizecount != 0:
        for size in sizes:
            #print(size)
            sizecount -= sizecount
            placed = False
            while not placed:

                #create new ship
                shipp = ship(size)

                #check if placement possible
                possible = True
                for i in ship.indexes:

                    # indexes must be < 100
                    if i >= 100:
                        possible = False
                        break

                    new_row = i // 10
                    new_col = i % 10
                    if new_row != ship.row and new_col != ship.col:
                        possible = False
                        break
                
                    # ships cannot intersect:
                    for other_ship in player.ships:
                        if i in other_ship[3]:
                            possible = False
                            break

                # place the ship
                if possible:
                    #print(shipp)
                    player.ships.append(shipp)
                    placed = True

def game():
    game.player1 = player()
    game.player2 = player()
    game.player1_turn = True
    game.over = False
    game.result = None
    return game.player1, game.player2, game.player1_turn, game.result

def make_move(i):
    player = game.player1 if game.player1_turn else game.player2
    opponent = game.player2 if game.player1_turn else game.player1
    hit = False
    #print(opponent)
    #list1 = [opponent[3] for i in opponent[0]]
    #print(list1)
    # set miss 'M' or hit 'H'
    for ship in opponent[0]:
        print(ship)
        if i in ship[3]:
            print(ship[3])
            player[1][i] = "H"
            hit = True

            # check if ship is sunk "S"
            for ship in opponent[0]:
                sunk = True
                for i in ship[3]:
                    if player[1][i] == "U":
                        sunk = False
                        break
                if sunk:
                    for i in ship[3]:
                        player[1][i] = "S"

        else:
            player[1][i] = "M"
    
    # check for game over
    game_over = True
    for ship in opponent[0]:
        for i in ship[3]:
            if player[1][i] == "U":
                game_over =False
    game.over = game_over
    game.result = 1 if game.player1_turn else 2

    # change the active team
    if not hit:
        game.player1_turn = not game.player1_turn


# global variables
SQ_SIZE = 35
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE
WIDTH = SQ_SIZE * 10 * 2 + H_MARGIN
HEIGHT = SQ_SIZE * 10 * 2 + V_MARGIN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INDENT = 10

# colors
GREY = (40,50,60)
WHITE = (255,250,250)
GREEN = (50,200,150)
RED = (250,50,100)
BLUE = (50, 150, 200)
ORANGE = (250, 140, 20)
COLORS = {"U": GREY, "M": BLUE, "H": ORANGE, "S": RED}

#function to draw a grid
def draw_grid(player, search = False, left = 0, top = 0):
    #print(player)
    for i in range(100):
        x = left + i % 10 * SQ_SIZE
        y = top + i // 10 * SQ_SIZE
        square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width = 3)
        if search:
            x += SQ_SIZE // 2
            y += SQ_SIZE // 2
            pygame.draw.circle(SCREEN, COLORS[player[1][i]], (x,y), radius= SQ_SIZE//4)

# function draw ships onto grids
def draw_ships(player, left = 0, top = 0):
    #print(player[0])
    for ship in player[0]: #ships
        x = left + ship[1] * SQ_SIZE + INDENT #col
        y = top + ship[0] * SQ_SIZE + INDENT #row
        if ship[2] == "h": # orientation
            width = ship[4] * SQ_SIZE - 2 * INDENT #size
            height = SQ_SIZE - 2 * INDENT
        else:
            width = SQ_SIZE - 2 * INDENT
            height =ship[4] * SQ_SIZE - 2 * INDENT #size
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, GREEN, rectangle, border_radius= 15)

#player1 = player()
#player2 = player()
games = game()


#player()
#print(player.indexes)

#def show_ships():
#    player.indexes = ["-" if i not in player.indexes else "X" for i in range(100)]
#    for row in range(10):
#       print(" ".join(player.indexes[(row-1)*10:row*10]))
#print(show_ships())

# pygame loop
animating = True
pausing =False
while animating:

    # track user interaction
    for event in pygame.event.get():

        #user closes the pygame window
        if event.type == pygame.QUIT:
            animating = False

        # user click on mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if game.player1_turn and x < SQ_SIZE*10 and y < 10*SQ_SIZE:
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                index = row * 10 + col
                make_move(index)
            elif not game.player1_turn and x > WIDTH - SQ_SIZE*10 and y > SQ_SIZE*10 + V_MARGIN:
                row = (y -SQ_SIZE*10 - V_MARGIN) // SQ_SIZE
                col = (x - SQ_SIZE*10 - H_MARGIN) // SQ_SIZE
                index = row * 10 + col
                make_move(index)

        #user presses key on keyboard
        if event.type == pygame.KEYDOWN:

            #escape key to close the animation
            if event.key == pygame.K_ESCAPE:
                animating =False

            #space bar to pause and unpause
            if event.key  == pygame.K_SPACE:
                pausing = not pausing
    
    #execution
    if not pausing:

        # draw background
        SCREEN.fill(GREY)

        # draw search grids
        draw_grid(games[0], search = True)
        draw_grid(games[1], search = True, left = (WIDTH - H_MARGIN)//2 + H_MARGIN, top = (HEIGHT - V_MARGIN)//2 + V_MARGIN)

        # draw position grids
        draw_grid(games[0], top = (HEIGHT - V_MARGIN)//2 + V_MARGIN)
        draw_grid(games[1], left = (WIDTH - H_MARGIN)//2 + H_MARGIN)

        #draw ships onto grid
        draw_ships(games[0], top = (HEIGHT - V_MARGIN)//2 + V_MARGIN)
        draw_ships(games[1], left = (WIDTH - H_MARGIN)//2 + H_MARGIN)

        #game over message
        if game.over:
            text = "Player " + str(game.result) + " wins!"
            textbox = myfont.render(text, False, GREY, WHITE)
            SCREEN.blit(textbox, (WIDTH//2 - 240, HEIGHT//2 - 50))

        #update screen
        pygame.display.flip()