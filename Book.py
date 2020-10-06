import csv 
import random

class Book():
    # Store book moves in CSV file
    # Each row in the csv file is an opening variation
    # Store a list of lists of book moves
    def __init__(self):
        self.book_moves = []
        # opening the CSV file in read mode
        with open('files/openingbook.csv', mode ='r') as file: 
            csvFile = csv.reader(file) 
            for lines in csvFile: 
                self.book_moves.append(lines)

    def choose_book_move(self, move_number):
        number_of_moves = len(self.book_moves)
        if number_of_moves >0:
            x = random.randint(0, number_of_moves-1)
            return self.book_moves[x][move_number]
        else:
            return None

    def update_book(self,move,move_number):
        # Given a new move played at move_number update book
        new_book = []
        for row in self.book_moves:
            try:
                if row[move_number]==move and row[move_number+1]!='': # And not end of opening
                    new_book.append(row)
            except:
                pass
        self.book_moves = new_book  # Update book
