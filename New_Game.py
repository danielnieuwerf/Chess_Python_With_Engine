from Game import *
from chessclock import *
import threading
class New_Game():
    def __init__(self,white_is_engine = False, black_is_engine = False, white_engine_depth = 1, black_engine_depth = 1):
        self.game = Game()
        self.clock = chessclock(180,180,2,2)
        # Initialise Pygame
        pygame.init()
        WIDTH, HEIGHT = 400, 400
        ROWS, COLUMNS = 8, 8
        SQUARE = 50
        screen = pygame.display.set_mode((WIDTH+150, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('blackpawn.png')) # Icon
        pygame.display.set_caption("Python Chess")  # Set Caption
        # Load piece images
        self.images = {}
        self.load_images()    # dictionary of piece symbols mapping to their images
        
        clock_thread = threading.Thread(target = self.clock.thread, args = (screen,))   # Run clock on seperate thread
        clock_thread.start()

        # Game loops depending on whose playing
        if not white_is_engine and black_is_engine:
            # Engine is black, player is white
            while self.game.gameover == False:
                # Draw game window
                self.draw_window(screen)

                # Listen for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:    
                        self.game.gameover = True
                    # Player turn 
                    if self.game.white_turn:
                        if event.type == pygame.MOUSEBUTTONDOWN:    
                            x, y = pygame.mouse.get_pos()
                            if x< 8*SQUARE and y<8*SQUARE:      # If click on board    
                                if self.game.selected_SQUARE == None:    # Select SQUARE
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                else:   # If already selected try to make the move
                                    i, j = self.game.selected_SQUARE
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                    # Move request successful
                                    if [i,j,y//SQUARE,x//SQUARE] in self.game.current_legal_moves:
                                        self.game.board.make_move(i,j,y//SQUARE,x//SQUARE)   # Make move
                                        self.game.handle_new_successfully_made_move([i,j,y//SQUARE,x//SQUARE])
                                        print(self.game.previous_move)
                                        self.draw_window(screen)
                                        print(str(self.game.move_number)+" " +str(self.game.previous_move))
                                        print("Score: "+ str(self.game.evaluate_position_score()))
                                        self.game.board.scores.print_totals()
                                        print(self.game.current_legal_moves)
                                        print("out of book?", self.game.out_of_book)
                                        self.clock.move_made()  # Let the clock know a move was made
                                    # Move request unsuccessful
                                    else:
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE

                # Engine move
                if not self.game.white_turn:
                    try:
                        engine_move = self.game.engine_move_decision(depth=black_engine_depth)
                        self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                        self.game.handle_new_successfully_made_move(engine_move)
                        print(str(self.game.move_number)+" " +str(self.game.previous_move))
                        print("Score: "+ str(self.game.evaluate_position_score()))
                        self.game.board.scores.print_totals()
                        self.clock.move_made()  # Let the clock know a move was made
                    except:
                        print('Engine resigns')
                        self.game.resign()
        elif white_is_engine and black_is_engine:
            # 2 engines
            self.clock.PAUSED = True    # Pause clock for 2 engines game
            while self.game.gameover==False:
                # Draw game window
                self.draw_window(screen)

                # Listen for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:    
                        self.game.gameover = True
            
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass

                # Engine move
                if self.game.white_turn:
                    engine_move = self.game.engine_move_decision(depth=white_engine_depth)
                    self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                    self.game.handle_new_successfully_made_move(engine_move)
                    print(str(self.game.move_number)+" " +str(self.game.previous_move))
                else:
                    engine_move = self.game.engine_move_decision(depth=black_engine_depth)
                    self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                    self.game.handle_new_successfully_made_move(engine_move)
                    print(str(self.game.move_number)+" " +str(self.game.previous_move))
        
                # Check for game over
                if self.game.gameover:
                    del self.game
                    self.game = Game()
                    print('GAMEOVER')
        elif white_is_engine and not black_is_engine:
            # Engine is white, player is black
            while self.game.gameover == False:
                # Draw game window
                self.draw_window(screen)

                # Listen for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:    
                        self.game.gameover = True
                    # Player turn 
                    if not self.game.white_turn:
                        if event.type == pygame.MOUSEBUTTONDOWN:    
                            x, y = pygame.mouse.get_pos()
                            if x< 8*SQUARE and y<8*SQUARE:      # If click on board    
                                if self.game.selected_SQUARE == None:    # Select SQUARE
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                else:   # If already selected try to make the move
                                    i, j = self.game.selected_SQUARE
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                    # Move request successful
                                    if [i,j,y//SQUARE,x//SQUARE] in self.game.current_legal_moves:
                                        self.game.board.make_move(i,j,y//SQUARE,x//SQUARE)   # Make move
                                        self.game.handle_new_successfully_made_move([i,j,y//SQUARE,x//SQUARE])
                                        print((self.game.move_number-1)//2, self.game.previous_move)
                                        self.draw_window(screen)
                                        self.clock.move_made()  # Let the clock know a move was made
                                    # Move request unsuccessful
                                    else:
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE

                # Engine move
                if self.game.white_turn:
                    engine_move = self.game.engine_move_decision(depth=white_engine_depth)
                    self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                    self.game.handle_new_successfully_made_move(engine_move)
                    print(str(self.game.move_number//2)+" " +str(self.game.previous_move))
                    self.clock.move_made()  # Let the clock know a move was made

        elif not white_is_engine and not black_is_engine:
            # 2 Players
            while self.game.gameover == False:
                # Draw game window
                self.draw_window(screen)

                # Listen for events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:    
                        self.game.gameover = True
            
                    if event.type == pygame.MOUSEBUTTONDOWN:    
                        x, y = pygame.mouse.get_pos()
                        if x< 8*SQUARE and y<8*SQUARE:      # If click on board    
                            if self.game.selected_SQUARE == None:    # Select SQUARE
                                self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                            else:   # If already selected try to make the move
                                i, j = self.game.selected_SQUARE
                                self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                # Move request successful
                                if [i,j,y//SQUARE,x//SQUARE] in self.game.current_legal_moves:
                                    self.game.board.make_move(i,j,y//SQUARE,x//SQUARE)   # Make move
                                    self.game.handle_new_successfully_made_move([i,j,y//SQUARE,x//SQUARE])
                                    print(self.game.previous_move)
                                    print("Legal moves: ", self.game.current_legal_moves)
                                    print("Score: ", self.game.board.scores.get_total())
                                    self.clock.move_made()  # Let the clock know a move was made
                                # Move request unsuccessful
                                else:
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE
         

                # Check for game over
                if self.game.gameover:
                    del self.game
                    self.game = Game()
                    print('GAMEOVER')

        clock_thread._delete
    def load_images(self):
        # Dictionary of piece symbols to their correctly resized images
        self.images = {}
        for piece in [Black_Pawn(), Black_Knight(), Black_Bishop(), Black_Rook(), Black_Queen(), Black_King(), White_Pawn(), White_Knight(), White_Bishop(), White_Rook(), White_Queen(), White_King()]:
            self.images[piece.symbol]=copy.copy(piece.image)
        return

    def draw_window(self, surface):
        # Draw empty board
        WHITE = (238,238,210)
        DARK = (118,150,86)
        for i in range(0,8):
            for j in range(0,8):
                if (i+j) % 2 ==1:
                    pygame.draw.rect(surface, DARK, ((i*SQUARE, j*SQUARE), (SQUARE,SQUARE))) # dark squares
                else:
                    pygame.draw.rect(surface, WHITE, ((i*SQUARE, j*SQUARE), (SQUARE,SQUARE))) # light squares
        
        # Highlight selected SQUARE
        if self.game.selected_SQUARE!= None:
            i, j = self.game.selected_SQUARE
            if (i+j)%2 ==1:
                pygame.draw.rect(surface, (100,100,100), ((j*SQUARE, i*SQUARE), (SQUARE,SQUARE)))
            else:
                pygame.draw.rect(surface, (150,150,150), ((j*SQUARE, i*SQUARE), (SQUARE,SQUARE)))

        # Draw pieces on board
        for i in range(8):
            for j in range(8):
                if self.game.board.pieces[i][j]!='.':
                    surface.blit(self.images[self.game.board.pieces[i][j]], (j*SQUARE, i*SQUARE))

        # Draw clock
        self.clock.display_clock(surface)
        pygame.display.update()