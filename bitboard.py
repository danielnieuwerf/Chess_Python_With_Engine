from bitarray import bitarray
import bitarray.util
import copy 

class BitBoard:
    """A bit board is a list of 8 bitarrays with bits 0 representing false, 1 representing true. Used for efficiently checking if a board is in check and other uses"""
    def __init__(self):
        array = bitarray.util.zeros(8)
        self.bits = []              # Initialise to a list of 8 bitarrays each '00000000'
        for i in range(8):
            self.bits.append(copy.copy(array))

    def set_true(self,x,y):
        # Set bit at x,y to 1.
        self.bits[x][y] = 1
    
    def set_false(self,x,y):
        # Set bit at x,y to 0
        self.bits[x][y] = 0

    def print(self):
        # Useful for debugging
        for i in range(8):
            print(self.bits[i])



