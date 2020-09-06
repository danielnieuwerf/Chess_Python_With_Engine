from Game import *

class New_Game():
    def __init__(self,white_is_engine = False, black_is_engine = False, white_engine_depth = 1, black_engine_depth = 1):
        self.game = Game()
        # Initialise Pygame
        pygame.init()
        WIDTH, HEIGHT = 400, 400
        ROWS, COLUMNS = 8, 8
        SQUARE = 50
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('blackpawn.png')) # Icon
        pygame.display.set_caption("Python Chess")  # Set Caption
        # Game loops depending on whose playing
        if not white_is_engine and black_is_engine:
            # Engine is black, player is white
            while self.game.gameover == False:
                # Draw game window
                self.game.draw_window(screen)

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
                                        self.game.draw_window(screen)
                                        print(str(self.game.move_number)+" " +str(self.game.previous_move))
                                        print("Score: "+ str(self.game.evaluate_position_score()))
                                        self.game.board.scores.print_totals()
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
                    except:
                        print('Engine resigns')
                        self.game.resign()
        elif white_is_engine and black_is_engine:
            # 2 engines
            while self.game.gameover==False:
                # Draw game window
                self.game.draw_window(screen)

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
                self.game.draw_window(screen)

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
                                        print(self.game.previous_move)
                                        self.game.draw_window(screen)
                                    # Move request unsuccessful
                                    else:
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE

                # Engine move
                if self.game.white_turn:
                    engine_move = self.game.engine_move_decision(depth=white_engine_depth)
                    self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                    self.game.handle_new_successfully_made_move(engine_move)
                    print(str(self.game.move_number)+" " +str(self.game.previous_move))
        elif not white_is_engine and not black_is_engine:
            # 2 Players
            while self.game.gameover == False:
                # Draw game window
                self.game.draw_window(screen)

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
                                # Move request unsuccessful
                                else:
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE
         

                # Check for game over
                if self.game.gameover:
                    del self.game
                    self.game = Game()
                    print('GAMEOVER')

