from New_Game import *

class Menu:
    """Main menu pygame window where you start new game"""
    def __init__(self):
        # Initialise Pygame
        pygame.init()
        WIDTH, HEIGHT = 400, 400
        ROWS, COLUMNS = 8, 8
        SQUARE = 50
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('blackpawn.png')) # Icon
        pygame.display.set_caption("Python Chess")  # Set Caption

        # Listen for events
        exit = False
        start_new_game = False
        white_is_engine, black_is_engine = True, False
        self.draw_screen(screen, white_is_engine, black_is_engine)  # Draw menu
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:    
                    exit = True
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:    
                    x, y = pygame.mouse.get_pos()
                    if y>300 and y<350 and x>150 and x<250: # If presses on play button
                        start_new_game = True
                        exit = True
                        break
                    # Change selection for white and black
                    elif x>320 and x<370 and y<150 and y>100:
                        white_is_engine = not white_is_engine
                    elif x>320 and x<370 and y<250 and y>200:
                        black_is_engine = not black_is_engine

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        white_is_engine = not white_is_engine
                        print(white_is_engine)
                    elif event.key == pygame.K_b:
                        black_is_engine = not black_is_engine
                        print(black_is_engine)

            self.draw_screen(screen, white_is_engine, black_is_engine)  # Redraw window and update it

        if start_new_game:
            New_Game(white_is_engine, black_is_engine,1,1)
            # Menu()  # When game finishes return to menu

    def draw_screen(self, surface, white_is_engine, black_is_engine):
        # Draw menu depending on selections onto surface
        RED = (255,0,0)
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        GREEN = (0, 255, 0)
        # Draw "Python Chess"
        font = pygame.font.Font('freesansbold.ttf', 48)
        text = font.render("Python Chess", True, RED)
        surface.blit(text,(40,20))
        # Draw play button
        pygame.draw.rect(surface, RED, ((150, 300), (100,50)))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Play", True, BLACK)
        surface.blit(text,(168,308))
        # Draw white selection
        pygame.draw.rect(surface, RED, ((100, 100), (200,50)))
        font = pygame.font.Font('freesansbold.ttf', 20)
        text2 = font.render("White is computer?", True, BLACK)
        surface.blit(text2,(104,115))
        if white_is_engine:
            box_colour = GREEN
        else:
            box_colour = RED
        pygame.draw.rect(surface, box_colour, ((320, 100), (50,50)))
        # Draw black selection
        pygame.draw.rect(surface, RED, ((100, 200), (200,50)))
        font = pygame.font.Font('freesansbold.ttf', 20)
        text2 = font.render("Black is computer?", True, BLACK)
        surface.blit(text2,(104,215))
        if black_is_engine:
            box_colour = GREEN
        else:
            box_colour = RED
        pygame.draw.rect(surface, box_colour, ((320, 200), (50,50)))

        # Update display
        pygame.display.update()

