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
        pygame.display.set_icon(pygame.image.load('files/blackpawn.png')) # Icon
        pygame.display.set_caption("Python Chess")  # Set Caption

        self.clock_times = ['None', '1|0', '2|1', '3|0', '3|2', '5|0', '5|5', '10|0', '15|10']  
        self.clock_index_selected = 4   # Keep track of index of selected clock setting 

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
                    elif x>324 and x<375 and y<150 and y>100:
                        white_is_engine = not white_is_engine
                    elif x>324 and x<375 and y<210 and y>160:
                        black_is_engine = not black_is_engine
                    elif x>99 and x<121 and y<270 and y>240:
                        self.clock_index_selected = (self.clock_index_selected-1)%len(self.clock_times)
                    elif x>279 and x<301 and y<270 and y>240:
                        self.clock_index_selected = (self.clock_index_selected+1)%len(self.clock_times)


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        white_is_engine = not white_is_engine
                        print(white_is_engine)
                    elif event.key == pygame.K_b:
                        black_is_engine = not black_is_engine
                        print(black_is_engine)
                    elif event.key == pygame.K_LEFT:
                        self.clock_index_selected = (self.clock_index_selected-1)%len(self.clock_times)
                    elif event.key == pygame.K_RIGHT:
                        self.clock_index_selected = (self.clock_index_selected+1)%len(self.clock_times)
                    elif event.key == pygame.K_p:
                        start_new_game = True
                        exit = True
                        break
            self.draw_screen(screen, white_is_engine, black_is_engine)  # Redraw window and update it
            

        if start_new_game:
            New_Game(white_is_engine, black_is_engine, 1, 1, self.clock_times[self.clock_index_selected])
            # Menu()  # When game finishes return to menu

    def draw_screen(self, surface, white_is_engine, black_is_engine):
        # Draw menu depending on selections onto surface
        RED = (255,0,0)
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
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
        pygame.draw.rect(surface, RED, ((50, 100), (250,50)))
        font = pygame.font.Font('freesansbold.ttf', 25)
        text2 = font.render("White is computer?", True, BLACK)
        surface.blit(text2,(54,115))
        if white_is_engine:
            box_colour = GREEN
        else:
            box_colour = RED
        pygame.draw.rect(surface, box_colour, ((325, 100), (50,50)))
        # Draw black selection
        pygame.draw.rect(surface, RED, ((50, 160), (250,50)))
        font = pygame.font.Font('freesansbold.ttf', 25)
        text2 = font.render("Black is computer?", True, BLACK)
        surface.blit(text2,(54,175))
        if black_is_engine:
            box_colour = GREEN
        else:
            box_colour = RED
        pygame.draw.rect(surface, box_colour, ((325, 160), (50,50)))
        # Draw clock selection
        font = pygame.font.Font('freesansbold.ttf', 32)
        current_clock_selection = font.render(self.clock_times[self.clock_index_selected], True, (0,255,0))
        pygame.draw.rect(surface, BLUE, ((140, 230), (120,50)))  # Clock display box
        clock_selection_position_on_surface = (180,240)
        if self.clock_times[self.clock_index_selected]=='None':
            clock_selection_position_on_surface = (160,240)
        elif self.clock_times[self.clock_index_selected] =='15|10':
            clock_selection_position_on_surface = (160,240)
        elif self.clock_times[self.clock_index_selected]=='10|0':
            clock_selection_position_on_surface = (168,240)
        surface.blit(current_clock_selection, clock_selection_position_on_surface)    # Currenct clock selection
        # Toggle clock selection arrows
        pygame.draw.polygon(surface, BLUE, [(120,270),(120,240),(100,255)])
        pygame.draw.polygon(surface, BLUE, [(280,270), (280,240), (300,255)])
        # Update display
        pygame.display.update()

