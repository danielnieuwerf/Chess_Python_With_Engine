import pygame
import copy
SQUARE = 50

# Piece classes
class Piece():
    def __init__(self):
        self.image = None
        self.value = 0.0
        self.white = True
        self.symbol = 'x'

    def __deepcopy__(self,memo):
        cp = Piece()
        cp.value = self.value
        cp.white = self.white
        cp.symbol = self.symbol
        return cp

class Black_Pawn(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/blackpawn.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = -1
        self.white = False
        self.symbol = 'p'

class Black_Rook(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/blackrook.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = -5
        self.white = False
        self.symbol = 'r'

class Black_Knight(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/blackknight.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = -3
        self.white = False
        self.symbol = 'n'

class Black_Bishop(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/blackbishop.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = -3.15
        self.white = False
        self.symbol = 'b'

class Black_Queen(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/blackqueen.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = -9
        self.white = False
        self.symbol = 'q'

class Black_King(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/blackking.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = 0
        self.white = False
        self.symbol = 'k'

class White_Pawn(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/whitepawn.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = 1
        self.white = True
        self.symbol = 'P'

class White_Rook(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/whiterook.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = 5
        self.white = True
        self.symbol = 'R'

class White_Knight(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/whiteknight.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = 3
        self.white = True
        self.symbol = 'N'

class White_Bishop(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/whitebishop.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = 3.15
        self.white = True
        self.symbol = 'B'

class White_Queen(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/whitequeen.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = 9
        self.white = True
        self.symbol = 'Q'

class White_King(Piece):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('files/whiteking.png')
        self.image = pygame.transform.scale(self.image, (SQUARE, SQUARE))
        self.value = 0
        self.white = True
        self.symbol = 'K'