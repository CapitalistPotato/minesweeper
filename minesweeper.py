import random
import re

class Field:
    def __init__(self, dimension_size, num_bombs):
        self.dimension_size = dimension_size
        self.num_bombs = num_bombs
        
        self.field = self.make_new_field()
        self.assign_to_field()
        
        self.clicks = set()
        
    def assign_to_field(self):
        for r in range(self.dimension_size):
            for c in range(self.dimension_size):
                if self.field[r][c] == '*':
                    continue
                self.field[r][c] = self.get_number_of_neighboring(r, c)
                
    def get_number_of_neighboring(self, row, col):
        number_neighboring = 0
        for r in range(max(0, row-1), min(self.dimension_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dimension_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.field[r][c] == '*':
                    number_neighboring += 1
        return number_neighboring
    
    def make_new_field(self):
        field = [[' ' for _ in range(self.dimension_size)] for _ in range(self.dimension_size)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            location = random.randint(0, self.dimension_size ** 2 - 1)
            row = location // self.dimension_size
            col = location % self.dimension_size
            
            if field[row][col] == '*':
                continue
            field[row][col] = '*'
            bombs_planted += 1
        return field
    
    def click(self, row, col):
        self.clicks.add((row, col))
        if self.field[row][col] == '*':
            return False
        elif self.field[row][col] > 0:
            return True
        
        for r in range(max(0, row-1), min(self.dimension_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dimension_size-1, col+1)+1):
                if (r, c) in self.clicks:
                    continue
                self.click(r, c)
        return True
    
    def __str__(self):
        visible_field = [[' ' for _ in range(self.dimension_size)] for _ in range(self.dimension_size)]
        for row in range(self.dimension_size):
            for col in range(self.dimension_size):
                if (row, col) in self.clicks:
                    visible_field[row][col] = str(self.field[row][col])
                else:
                    visible_field[row][col] = ' '
        return '\n'.join([' | '.join(row) for row in visible_field])

def play(dimension_size=10, num_bombs=10):
    field = Field(dimension_size, num_bombs)
    safe = True
    while len(field.clicks) < field.dimension_size ** 2 - num_bombs:
        print(field)
        user_input = re.split(',(\\s)*', input("Choose where to click. Write as row, col:"))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= field.dimension_size or col < 0 or col >= dimension_size:
            print("Invalid location, try again.")
            continue
        
        safe = field.click(row, col)
        if not safe:
            break
        
    if safe:
        print("You win.")
    else:
        print("Game over.")
        field.clicks = [(r, c) for r in range(field.dimension_size) for c in range(field.dimension_size)]
        print(field)

play()
