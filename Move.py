from bitarray import bitarray
import bitarray.util

class Move:
    """A bit board is a list of 8 bitarrays with bits 0 representing false, 1 representing true. Used for efficiently checking if a board is in check and other uses"""
    def __repr__(self):
        try:
            print(self.bits)
        except:
            print("None")
    def __init__(self, i: int, j: int, x: int, y: int):
        # A move moving the piece at square i,j to x,y is represented in binary as bit array like "010111000101"
        # where i is first 3 digits, j is the next 3 and so on ... 
        # in this example i = 010   j=111   x=000   y=101
        self.bits = self.convert_ints_to_bitarray(i, j, x, y)

    def convert_ints_to_bitarray(self, i: int, j:int, x:int, y:int):
        move = bitarray.util.zeros(12)
        if i == 0:    # 000
            pass
        elif i == 1:  # 001
            move[2] = 1
        elif i == 2:    # 010
            move[1] = 1
        elif i == 3:  # 011
            move[1] = 1
            move[2] = 1
        elif i == 4:    # 100
            move[0] = 1
        elif i == 5:  # 101
            move[0] = 1
            move[2] = 1
        elif i == 6:    # 110
            move[0] = 1
            move[1] = 1
        elif i == 7:  # 111
            move[0] = 1
            move[1] = 1
            move[2] = 1
        if j == 0:    # 000
            pass
        elif j == 1:  # 001
            move[5] = 1
        elif j == 2:    # 010
            move[4] = 1
        elif j == 3:  # 011
            move[4] = 1
            move[5] = 1
        elif j == 4:    # 100
            move[3] = 1
        elif j == 5:  # 101
            move[3] = 1
            move[5] = 1
        elif j == 6:    # 110
            move[3] = 1
            move[4] = 1
        elif j == 7:  # 111
            move[3] = 1
            move[4] = 1
            move[5] = 1
        if x == 0:    # 000
            pass
        elif x == 1:  # 001
            move[8] = 1
        elif x == 2:    # 010
            move[7] = 1
        elif x == 3:  # 011
            move[7] = 1
            move[8] = 1
        elif x == 4:    # 100
            move[6] = 1
        elif x == 5:  # 101
            move[6] = 1
            move[8] = 1
        elif x == 6:    # 110
            move[6] = 1
            move[7] = 1
        elif x == 7:  # 111
            move[6] = 1
            move[7] = 1
            move[8] = 1
        if y == 0:    # 000
            pass
        elif y == 1:  # 001
            move[11] = 1
        elif y == 2:    # 010
            move[10] = 1
        elif y == 3:  # 011
            move[10] = 1
            move[11] = 1
        elif y == 4:    # 100
            move[9] = 1
        elif y == 5:  # 101
            move[9] = 1
            move[11] = 1
        elif y == 6:    # 110
            move[9] = 1
            move[10] = 1
        elif y == 7:  # 111
            move[9] = 1
            move[10] = 1
            move[11] = 1

        return move

    def convert_move_to_ints(self):
        # Given bitarray describing move return indexes of pieces in charboard i,j,x,y
        i = self.bitarray_to_int(self.bits[0:3])
        j = self.bitarray_to_int(self.bits[3:6])
        x = self.bitarray_to_int(self.bits[6:9])
        y = self.bitarray_to_int(self.bits[9:12])
        return i, j, x, y

    def bitarray_to_int(self, x):
        # Given a bit array x, of length 3, return the integer it represents
        if x[0] == 1:   # 4-7
            if x[1] == 1:   # 6-7
                if x[2] == 1:   #7
                    return 7
                return 6
            else:   # 4 - 5
                if x[2] == 1:   # 5
                    return 5
                return 4
        else:   # 0-3
            if x[1] == 1:   # 2-3
                if x[2] == 1:   #3
                    return 3
                return 2
            else:   # 0 - 1
                if x[2] == 1:   # 1
                    return 1
                return 0

