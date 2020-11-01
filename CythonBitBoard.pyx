from bitarray import bitarray
import bitarray.util
import copy 

class BitBoard:
    """A bit board is a list of 8 bitarrays with bits 0 representing false, 1 representing true. Used for efficiently checking if a board is in check and other uses"""
    def __init__(self):
        cdef int i

        array = bitarray.util.zeros(8)
        self.bits = []              # Initialise to a list of 8 bitarrays each '00000000'
        for i in range(8):
            self.bits.append(copy.copy(array))

    def set_true(self,int x, int y):
        # Set bit at x,y to 1.
        self.bits[x][y] = 1
    
    def set_false(self, int x, int y):
        # Set bit at x,y to 0
        self.bits[x][y] = 0

    def number_of_ones(self):
        # Number of 1s in the bitboard
        cdef int count, i, j

        count = 0
        for i in range(8):
            for j in range(8):
                if self.bits[i][j]==1:
                    count+=1

        return count
