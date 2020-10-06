import time
import pygame

class chessclock:
    """contains clocks for white and black and data about the clock"""
    def __init__(self, white_time, black_time, WHITE_INCREMENT = 0, BLACK_INCREMENT = 0, white_turn = True):
        self.PAUSED = False     # Control whether or not the clock is paused
        self.white_clock = clock(white_time)
        self.black_clock = clock(black_time)
        self.white_increment = WHITE_INCREMENT
        self.black_increment = BLACK_INCREMENT
        self.white_clock_is_running = white_turn
        self.black_clock_is_running = not white_turn

    def update_clock(self):
        if self.PAUSED:
            return
        time_now = time.time()
        time.sleep(0.07)
        t1 = time.time() - time_now
        if self.white_clock_is_running:
            self.white_clock.update_clock(t1)
        elif self.black_clock_is_running:
            self.black_clock.update_clock(t1)

    def display_clock(self, surface):
        # Display clock on a pygame surface
        BACKGROUND_COLOUR = (111,111,111)
        pygame.draw.rect(surface, BACKGROUND_COLOUR, ((420, 50), (100,50))) # White time background
        pygame.draw.rect(surface, BACKGROUND_COLOUR, ((420, 300), (100,50))) # Black time background

        # Draw times onto screen in these boxes
        font = pygame.font.Font('freesansbold.ttf', 30)
        white_time = font.render(self.white_clock.print_clock(), True, (0,0,0))
        black_time = font.render(self.black_clock.print_clock(), True, (0,0,0))
        surface.blit(white_time,(430,60))     # Display white time
        surface.blit(black_time,(430,310))     # Display black time

        pygame.display.update() # Update window
        
    def move_made(self):
        """ If a move was made update clock is running and add increment"""
        if self.white_clock_is_running:
            self.white_clock.update_clock(-self.white_increment)
        else:
            self.black_clock.update_clock(-self.black_increment)
        self.white_clock_is_running = not self.white_clock_is_running
        self.black_clock_is_running = not self.black_clock_is_running

    def thread(self, surface):
        while self.PAUSED == False:
            self.update_clock()
            self.display_clock(surface)

class clock:
    def __init__ (self, seconds=None):
        if seconds is not None:
            self.seconds = seconds

    def print_clock(self):
        if self.seconds<0:
            return "00:00"
        seconds = self.seconds % 60
        minutes = self.seconds % 3600 // 60
        hours = self.seconds // 3600
        if hours == 0:
            clk = self.to_string(int(minutes))+":"+self.to_string(int(seconds))
            if minutes==0 and seconds<10:   # Less than 10 seconds left
                deciseconds = str(round(self.seconds%1,2))
                return(self.to_string(int(seconds))+"."+deciseconds[2:])
        else:
            clk = self.to_string(int(hours))+":"+self.to_string(int(minutes))   # Print hours and minutes only
        return clk
            
    def to_string(self, x: int):
        "Returns string for displaying clock component h/m/s"
        string =''
        if x<10:
            string+='0'
        string+=str(x)
        return string

    def update_clock(self, x: float):
        """Given a time in seconds x subtract it from self.seconds"""
        self.seconds -= x



