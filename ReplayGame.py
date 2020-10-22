from New_Game import New_Game_Replay
import csv
import pygame

class Replay_Menu():
    def __init__(self):
        pygame.init()
        WIDTH, HEIGHT = 400, 400
        ROWS, COLUMNS = 8, 8
        SQUARE = 50
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('files/blackpawn.png')) # Icon
        pygame.display.set_caption("Python Chess")  # Set Caption

        exit = False
        num_saved_games = number_of_saved_games()
        self.game_id_selected = 0
        replay_game_id = None

        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:    
                    exit = True
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    x, y = pygame.mouse.get_pos()
                    # If press on game selection toggle buttons and num games not 0
                    if num_saved_games !=0:
                        if x>99 and x<121 and y<270 and y>240:
                            self.game_id_selected = (self.game_id_selected-1)%num_saved_games
                        elif x>279 and x<301 and y<270 and y>240:
                            self.game_id_selected = (self.game_id_selected + 1)%num_saved_games
                    # If we press play
                    if y>300 and y<350 and x>150 and x<250: # If presses on play button
                        replay_game_id = self.game_id_selected
                        exit = True
                        break
                    # If press back to menu button
                    if y>299 and y<351 and x>324 and x<376:
                        exit = True
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.game_id_selected = (self.game_id_selected-1)%num_saved_games
                    elif event.key == pygame.K_RIGHT:
                        self.game_id_selected = (self.game_id_selected + 1)%num_saved_games

            # Re draw window
            self.draw_screen(screen)

        # Replay the chosen saved game
        if replay_game_id != None:
            if replay_game_id == 0:
                Replay_Game(num_saved_games)
            else:
                Replay_Game(replay_game_id)

        else:   # Else function is finished and we return to the menu
            pass

    def draw_screen(self, surface):
        BLUE = (0,0,255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        # Make note game 0 is most recent saved game
        font = pygame.font.SysFont('comicsansms', 26)
        text = font.render("Replay your saved games", True, BLUE)
        surface.blit(text,(44,42))
        # Draw play button
        pygame.draw.rect(surface, RED, ((150, 300), (100,50)))
        font = pygame.font.SysFont('comicsansms', 26)
        text = font.render("Replay", True, BLACK)
        surface.blit(text,(159,306))
        # Draw game id selection
        font = pygame.font.SysFont('comicsansms', 22)
        text = font.render("Game "+str(self.game_id_selected), True, BLACK)
        pygame.draw.rect(surface, BLUE, ((140, 230), (120,50)))  # Clock display box
        surface.blit(text, (150, 240))
        # Toggle clock selection arrows
        pygame.draw.polygon(surface, BLUE, [(120,270), (120,240), (100,255)])
        pygame.draw.polygon(surface, BLUE, [(280,270), (280,240), (300,255)])
        # Draw the return button
        pygame.draw.circle(surface, RED, (350,325), 25, 5)
        font = pygame.font.SysFont("comicsansms", 12)
        text = font.render("Menu", True, RED)
        surface.blit(text, (335,315))
        # Update display
        pygame.display.update()

class Replay_Game():
    def __init__ (self, replay_game_id):
        # Given an CSV file replay that game with time between each move
        if replay_game_id != 0:
            csv_path = "saved_games/game_id"+str(replay_game_id)
        else:
            csv_path = "saved_games/game_id"+str(number_of_saved_games())

        game_moves = []
        with open(csv_path, mode ='r') as file:     
            # reading the CSV file 
            csvFile = csv.reader(file)
            # displaying the contents of the CSV file 
            for line in csvFile:
                game_moves.append(line)
        
        moves = []
        for i in range(len(game_moves)):
            moves.append(game_moves[i][0])

        #print(moves)
        for move in moves:
            print(move)

        # Pass moves into new game
        New_Game_Replay(moves) 
       
def number_of_saved_games():
    # Return number of saved games in saved games folder
    import os
    files = os.listdir("saved_games")
    return len(files)
