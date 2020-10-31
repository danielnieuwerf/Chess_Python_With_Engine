from Game import *
from chessclock import *
import threading

class New_Game():
    def __init__(self,white_is_engine = False, black_is_engine = False, white_engine_depth = 2, black_engine_depth = 2, clock_string = '3|2', is_replay = False, replay_moves = None):
        self.game = Game()
        self.clock = chessclock()
        self.clock.set_chess_clock(clock_string)    # Set the chess clock to the correct setting
        self.moves = [] # Store the moves made in the game so the game may be saved if user requests it
        self.board_flipped = True # Used for view of board (user may flip the board in game)

        # Initialise Pygame
        pygame.init()
        WIDTH, HEIGHT = 400, 400
        ROWS, COLUMNS = 8, 8
        SQUARE = 50
        pygame.display.set_icon(pygame.image.load('files/blackpawn.png')) # Icon
        pygame.display.set_caption("Python Chess")  # Set Caption
        MOVE_SOUND = pygame.mixer.Sound("files/move_sound.wav") # Load sound to play when a move is made
        

        # Load piece images
        self.images = {}
        self.load_images()    # dictionary of piece symbols mapping to their images

        # Disable the clock if it is a replay
        if is_replay:   
            self.clock.disabled = True

        # Provide additional width if there is a clock enabled
        if not self.clock.disabled: # When there is a clock add some additional width to the display
            ADDITIONAL_CLOCK_WIDTH = 150
        else:
            ADDITIONAL_CLOCK_WIDTH = 150
        screen = pygame.display.set_mode((WIDTH+ADDITIONAL_CLOCK_WIDTH, HEIGHT), pygame.RESIZABLE)

        # Start clock thread
        if not self.clock.disabled:
            clock_thread = threading.Thread(target = self.clock.thread, args = (screen,))   # Run clock on seperate thread
            clock_thread.start()
        else:
            print("NO CLOCK")

        # If game is a replay
        if is_replay:
            TIME_FOR_MOVE = 0.8
            self.draw_window(screen)    # Display game initially
            time.sleep(TIME_FOR_MOVE)   # Sleep until next move
            exit = False
            move_index = 0
            while not exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit = True
                        break
                move = replay_moves[move_index]
                i = int(move[1])
                j = int(move[4])
                x = int(move[7])
                y = int(move[10])
                self.game.board.make_move(i, j, x, y)
                self.draw_window(screen)    # Display game after each move was made
                time.sleep(TIME_FOR_MOVE)   # Sleep until next move
                if move_index + 1 == len(replay_moves):
                    exit = True
                    break

                move_index += 1
            
        # If game is not a game replay
        else:   
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
                                if x > 8*SQUARE+40 and x < 8*SQUARE + 110 and y < 4*SQUARE + 15 and y > 4*SQUARE - 15:  # Clicked on resign button
                                    self.game.resign()
                                elif x > 460 and x < 491 and y>369 and y<399: # Press flip board button
                                    self.flip_board()
                                if x< 8*SQUARE and y<8*SQUARE:      # If click on board    
                                    if self.game.selected_SQUARE == None:    # Select SQUARE
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                    else:   # If already selected try to make the move
                                        i, j = self.game.selected_SQUARE
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                        xpos = y//SQUARE
                                        ypos = x//SQUARE
                                        if self.board_flipped:
                                            i = 7 - i
                                            j = 7 - j
                                            xpos = 7 - xpos
                                            ypos = 7 - ypos
                                        # Move request successful
                                        if [i,j,xpos,ypos] in self.game.current_legal_moves:
                                            self.game.board.make_move(i,j,xpos,ypos)   # Make move
                                            pygame.mixer.Sound.play(MOVE_SOUND) # Play move sound
                                            self.game.handle_new_successfully_made_move([i,j,xpos,ypos])
                                            self.moves.append([i,j,xpos,ypos])
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
                            pygame.mixer.Sound.play(MOVE_SOUND) # Play move sound
                            self.game.handle_new_successfully_made_move(engine_move)
                            self.moves.append(engine_move)
                            print(str(self.game.move_number)+" " +str(self.game.previous_move))
                            print("Score: "+ str(self.game.evaluate_position_score()))
                            self.game.board.scores.print_totals()
                            self.clock.move_made()  # Let the clock know a move was made
                        except:
                            print('Engine resigns')
                            self.game.resign()

                    # Check if either player has ran out of time
                    if self.clock.black_flagged:
                        self.game.white_won = True
                        self.game.gameover = True
                    if self.clock.white_flagged:
                        self.game.black_won = True
                        self.game.gameover = True
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
                        try:
                            engine_move = self.game.engine_move_decision(depth=white_engine_depth)
                            self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                            pygame.mixer.Sound.play(MOVE_SOUND) # Play move sound
                            self.game.handle_new_successfully_made_move(engine_move)
                            self.moves.append(engine_move)  # Add engine move to moves
                            print(str(self.game.move_number)+" " +str(self.game.previous_move))
                        except:
                            print('Engine resigns')
                            self.game.resign()
                    else:
                        try:
                            engine_move = self.game.engine_move_decision(depth=black_engine_depth)
                            self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                            pygame.mixer.Sound.play(MOVE_SOUND) # Play move sound
                            self.game.handle_new_successfully_made_move(engine_move)
                            self.moves.append(engine_move)  # Add engine move to moves
                            print(str(self.game.move_number)+" " +str(self.game.previous_move))
                        except:
                            print('Engine resigns')
                            self.game.resign()
                
                
                    # Check for game over
                    if self.game.gameover:
                        print('GAMEOVER')
                        print("white won?:", self.game.white_won)
                        print("Draw?: ", self.game.gameIsDraw)
                        print("Black won?:", self.game.black_won)
            elif white_is_engine and not black_is_engine:
                self.board_flipped = False  # View board from black's perspective initially
                self.clock.flipped = False
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
                                if x > 8*SQUARE+40 and x < 8*SQUARE + 110 and y < 4*SQUARE + 15 and y > 4*SQUARE - 15:  # Clicked on resign button
                                    self.game.resign()
                                elif x > 460 and x < 491 and y>369 and y<399: # Press flip board button
                                    self.flip_board()
                                if x< 8*SQUARE and y<8*SQUARE:      # If click on board    
                                    if self.game.selected_SQUARE == None:    # Select SQUARE
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                    else:   # If already selected try to make the move
                                        i, j = self.game.selected_SQUARE
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                        xpos = y//SQUARE
                                        ypos = x//SQUARE
                                        if self.board_flipped:
                                            i = 7 - i
                                            j = 7 - j
                                            xpos = 7 - xpos
                                            ypos = 7 - ypos
                                        # Move request successful
                                        if [i,j,xpos,ypos] in self.game.current_legal_moves:
                                            self.game.board.make_move(i,j,xpos,ypos)   # Make move
                                            pygame.mixer.Sound.play(MOVE_SOUND) # Play move sound
                                            self.game.handle_new_successfully_made_move([i,j,xpos,ypos])
                                            self.moves.append([i,j,xpos,ypos])
                                            print((self.game.move_number-1)//2, self.game.previous_move)
                                            self.draw_window(screen)
                                            self.clock.move_made()  # Let the clock know a move was made
                                        # Move request unsuccessful
                                        else:
                                            self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE

                    # Engine move
                    if self.game.white_turn:
                        try:
                            engine_move = self.game.engine_move_decision(depth=white_engine_depth)
                            self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                            pygame.mixer.Sound.play(MOVE_SOUND) # Play move sound
                            self.game.handle_new_successfully_made_move(engine_move)
                            print(str(self.game.move_number//2)+" " +str(self.game.previous_move))
                            self.clock.move_made()  # Let the clock know a move was made
                            self.moves.append(engine_move)
                        except:
                            print('Engine resigns')
                            self.game.resign()
                    # Check if either player has ran out of time
                    if self.clock.black_flagged:
                        self.game.white_won = True
                        self.game.gameover = True
                    if self.clock.white_flagged:
                        self.game.black_won = True
                        self.game.gameover = True
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
                            if x > 8*SQUARE+40 and x < 8*SQUARE + 110 and y < 4*SQUARE + 15 and y > 4*SQUARE - 15:  # Clicked on resign button
                                self.game.resign()
                            elif x > 460 and x < 491 and y>369 and y<399: # Press flip board button
                                self.flip_board()
                            if x< 8*SQUARE and y<8*SQUARE:      # If click on board    
                                if self.game.selected_SQUARE == None:    # Select SQUARE
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                else:   # If already selected try to make the move
                                    i, j = self.game.selected_SQUARE
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE
                                    xpos = y//SQUARE
                                    ypos = x//SQUARE
                                    if self.board_flipped:
                                        i = 7 - i
                                        j = 7 - j
                                        xpos = 7 - xpos
                                        ypos = 7 - ypos
                                    # Move request successful
                                    if [i,j,xpos,ypos] in self.game.current_legal_moves:
                                        self.game.board.make_move(i,j,xpos,ypos)   # Make move
                                        pygame.mixer.Sound.play(MOVE_SOUND) # Play move sound
                                        self.game.handle_new_successfully_made_move([i,j,xpos,ypos])
                                        self.moves.append([i,j,xpos,ypos])
                                        print(self.game.previous_move)
                                        print("Legal moves: ", self.game.current_legal_moves)
                                        # print("Score: ", self.game.board.scores.get_total())
                                        print("Eval: ", self.game.evaluate_position_score())
                                        self.clock.move_made()  # Let the clock know a move was made
                                        self.flip_board()   # Flip board
                                    # Move request unsuccessful
                                    else:
                                        self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE
         

                    # Check for game over
                    if self.game.gameover:
                        print('GAMEOVER')
                    # Check if either player has ran out of time
                    if self.clock.black_flagged:
                        self.game.white_won = True
                        self.game.gameover = True
                    if self.clock.white_flagged:
                        self.game.black_won = True
                        self.game.gameover = True

            # Handle game over
            self.clock.PAUSED = True    # End clock thread as game is over
            self.draw_window(screen)    # Display game in it's final state
            time.sleep(0.3)

            end_session = False
            display_game_over_screen = True
            game_saved = False
            rematch_request = False     # If user requests rematch set this to true
            return_to_menu_request = False  # If user requests to return to menu set this to true
            while not end_session:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:    
                        end_session = True
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:    
                        x, y = pygame.mouse.get_pos()
                        if display_game_over_screen and y>109 and y<131 and x>270 and x<291: # If presses on close button for gameover screen
                            display_game_over_screen = False
                        elif display_game_over_screen and not game_saved and x>119 and x<191 and y>249 and y<291: # If press save game
                            game_saved = True
                            # Save the game here too
                            self.save_game()
                        elif display_game_over_screen and y>249 and y<291 and x>209 and x<281: # If press on rematch
                            rematch_request = True
                            end_session = True
                        elif display_game_over_screen and x>119 and x<281 and y>189 and y<231: # If press return to menu
                            return_to_menu_request = True
                            end_session = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            display_game_over_screen = not display_game_over_screen
            
                # Display game over screen if display_game_over_screen == True
                if display_game_over_screen:
                    self.gameover_screen(screen, game_saved)
                else:
                    self.draw_window(screen)
            
            if rematch_request:
                New_Game(white_is_engine, black_is_engine, 1, 1, clock_string)

            if return_to_menu_request:
                del self
                from menu import Menu
                Menu()

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
            if (i+j)%2 == 1:
                pygame.draw.rect(surface, (100,100,100), ((j*SQUARE, i*SQUARE), (SQUARE,SQUARE)))
            else:
                pygame.draw.rect(surface, (150,150,150), ((j*SQUARE, i*SQUARE), (SQUARE,SQUARE)))

        # Draw pieces on board
        if not self.board_flipped:
            for i in range(8):
                for j in range(8):
                    if self.game.board.pieces[i][j]!='.':
                        surface.blit(self.images[self.game.board.pieces[i][j]], (j*SQUARE, i*SQUARE))
        else:
            for i in range(8):
                for j in range(8):
                    if self.game.board.pieces[i][j]!='.':
                        surface.blit(self.images[self.game.board.pieces[i][j]], ((7 - j)*SQUARE, (7 - i)*SQUARE))


        # Draw clock
        if not self.clock.disabled:
            self.clock.display_clock(surface, self.board_flipped)

        # Draw resign button
        pygame.draw.rect(surface, (255, 0, 0), ((SQUARE*8 + 40, SQUARE*3.7), (70, 30)))
        font = pygame.font.SysFont('comicsansms', 18)
        text = font.render("Resign", True, (255,255,255))
        surface.blit(text, (450, 190))
        pygame.display.update()

        # Draw Flip board button
        flipboard_image= pygame.image.load('files/flipboard.png')
        flipboard_image = pygame.transform.scale(flipboard_image, (30, 30))
        surface.blit(flipboard_image, (460,370))

    def flip_board(self):
        self.board_flipped = not self.board_flipped
        self.clock.flipped = self.board_flipped

    def gameover_screen(self, surface, game_saved = False):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        ORANGE = (255, 165, 0)
        GREY = (112,128,144)
        GREEN = (0, 255, 0)

        # Draw gameover screen box
        pygame.draw.rect(surface, WHITE, ((100, 100), (200,200)))

        # Draw game result into the gameover box
        
        game_result = ""
        FONT_SIZE = 32
        if self.game.white_won:
            game_result = "White won"
        elif self.game.black_won:
            game_result = "Black won"
        else:
            game_result = "Game is draw"
            FONT_SIZE = 26

        font = pygame.font.SysFont('comicsansms', FONT_SIZE)
        text = font.render(game_result, True, BLACK)
        surface.blit(text,(116,140))

        # Draw close button in box
        pygame.draw.line(surface, RED, (270,110), (290,130), 5)
        pygame.draw.line(surface, RED, (270,130), (290,110), 5)

        # Draw return to menu box
        pygame.draw.rect(surface, ORANGE, ((120, 190), (160,40)))
        font = pygame.font.SysFont('comicsansms', 18)
        text = font.render("Return to menu", True, WHITE)
        surface.blit(text, (137, 196))

        # Draw save game box     
        if not game_saved:
            font = pygame.font.SysFont('comicsansms', 12)
            pygame.draw.rect(surface, GREY, ((120, 250), (70, 40)))
            text = font.render("Save game", True, BLACK)
            surface.blit(text, (125, 262))
        else:
            font = pygame.font.SysFont('comicsansms', 12)
            pygame.draw.rect(surface, GREEN, ((120, 250), (70, 40)))
            text = font.render("Game saved", True, BLACK)
            surface.blit(text, (122, 262))
       
        # Draw rematch box
        pygame.draw.rect(surface, GREY, ((210, 250), (70, 40)))
        font = pygame.font.SysFont('comicsansms', 14)
        text = font.render("Rematch", True, BLACK)
        surface.blit(text, (215, 260))

        # Update display
        pygame.display.update()

    def save_game(self):
        if len(self.moves)==0: # If no moves in game do not save it
            return
        # Create a new csv file in saved_games folder
        import os

        files = os.listdir("saved_games")  # Count number of saved games
        num_files = len(files)

        import csv 
        with open("saved_games/game_id"+str(num_files+1),"w",newline="") as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter='\n')
            wr.writerow(self.moves)

class New_Game_Replay():
    def __init__(self, moves):
        # Given a list of moves in the form "[i ,j ,x ,y]"
        New_Game(is_replay = True, replay_moves = moves)

"""
New Game_Test used for testing where you pass in the game object and continue playing from there
"""

class New_Game_Test():
    def __init__(self, game, white_is_engine = False, black_is_engine = False, white_engine_depth = 1, black_engine_depth = 1, clock_string = '3|2'):
        self.game = game
        self.clock = chessclock()
        self.clock.set_chess_clock(clock_string)    # Set the chess clock to the correct setting
        # Initialise Pygame
        pygame.init()
        WIDTH, HEIGHT = 400, 400
        ROWS, COLUMNS = 8, 8
        SQUARE = 50
        if not self.clock.disabled: # When there is a clock add some additional width to the display
            ADDITIONAL_CLOCK_WIDTH = 150
        else:
            ADDITIONAL_CLOCK_WIDTH = 0
        screen = pygame.display.set_mode((WIDTH+ADDITIONAL_CLOCK_WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_icon(pygame.image.load('files/blackpawn.png')) # Icon
        pygame.display.set_caption("Python Chess")  # Set Caption
        # Load piece images
        self.images = {}
        self.load_images()    # dictionary of piece symbols mapping to their images
        
        if not self.clock.disabled:
            clock_thread = threading.Thread(target = self.clock.thread, args = (screen,))   # Run clock on seperate thread
            clock_thread.start()
        else:
            print("NO CLOCK")

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

                # Check if either player has ran out of time
                if self.clock.black_flagged:
                    self.game.white_won = True
                    self.game.gameover = True
                if self.clock.white_flagged:
                    self.game.black_won = True
                    self.game.gameover = True
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
                    time.sleep(0.5)
                    print(str(self.game.move_number)+" " +str(self.game.previous_move))
                else:
                    engine_move = self.game.engine_move_decision(depth=black_engine_depth)
                    self.game.board.make_move(engine_move[0],engine_move[1],engine_move[2],engine_move[3])   # Make move
                    self.game.handle_new_successfully_made_move(engine_move)
                    time.sleep(0.5)
                    print(str(self.game.move_number)+" " +str(self.game.previous_move))
        
                # Check for game over
                if self.game.gameover:
                    # del self.game
                    # self.game = Game()
                    print('GAMEOVER')
                    print('white won?: ', self.game.white_won)
                    print('black won?:', self.game.black_won)
                    print('Last move: ', self.game.previous_move)
                    print("draw?:", self.game.gameIsDraw)
                    print("stalemate? :", self.game.is_stalemate())
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

                # Check if either player has ran out of time
                if self.clock.black_flagged:
                    self.game.white_won = True
                    self.game.gameover = True
                if self.clock.white_flagged:
                    self.game.black_won = True
                    self.game.gameover = True
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
                                    # print("Score: ", self.game.board.scores.get_total())
                                    print("Eval: ", self.game.evaluate_position_score())
                                    self.clock.move_made()  # Let the clock know a move was made
                                # Move request unsuccessful
                                else:
                                    self.game.selected_SQUARE = y//SQUARE, x//SQUARE     # Select new SQUARE
         

                # Check for game over
                if self.game.gameover:
                    del self.game
                    self.game = Game()
                    print('GAMEOVER')
                # Check if either player has ran out of time
                if self.clock.black_flagged:
                    self.game.white_won = True
                    self.game.gameover = True
                if self.clock.white_flagged:
                    self.game.black_won = True
                    self.game.gameover = True

        self.clock.PAUSED = True    # End clock thread as game is over
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
        if not self.clock.disabled:
            self.clock.display_clock(surface, self.board_flipped)
        pygame.display.update()