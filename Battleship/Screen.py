Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def new_screen(rows: int, columns: int) -> '2D list':
    '''
    Create and return an empty screen: a list of rows with each row
    being a list of pixels going across that row. Initially, all pixels will be 0
    (black).
    '''
    result = []
    for r in range(rows): #for every row, you're going to have 'x' columns
        result.append([' _'] * columns)
    return result

x = new_screen(10,10)
print(x)

def board_print(T: '2D table') -> None:
    '''Print out table in nice format'''
    s = "   " #3 spaces
    for i in range(len(T[0])):
        s += str(i) + " "
    print(s)
    for row in range(len(T)):
        print("{:1s} ".format(Alphabet[row]), end = "")
        for col in range(len(T[0])):
            if T[row][col] == 'O': #not a zero, ship position for ocean view
                pixel = ' *'
            elif T[row][col] == 'X': #hit for ocean view
                pixel = ' X'
            elif T[row][col] == 'H': #hit for target view
                pixel = ' H'
            elif T[row][col] == 'M': #miss for target view
                pixel = ' M'
            else:
                pixel = T[row][col]
            print(pixel, sep='', end='')
        print()
    return

x = new_screen(10,10)
              
def set_pixel(s: '2D list', rownum: int, colnum: int, value: str) -> None:
    ''' Change the screen so that the specified pixel has the specified
        value
    '''
    s[rownum][colnum] = value
    return

#namedtuple Player(Target, Ocean, Ships(namedtuple))
#Collection of ships
#Ships(Name, health, coordinates)
#Use dictionaries for ships

from collections import namedtuple

Ship = namedtuple('Ship', 'type health coordinates')
Player = namedtuple('Player', 'target ocean ship')

def ship_length(s: 'Ship') -> bool:
    '''checks for correct ship length'''
    if s.type == 'CAR':
        if len(s.coordinates) == 5:
            return True
    elif s.type == 'BAT':
        if len(s.coordinates) == 4:
            return True
    elif s.type == 'CRU':
        if len(s.coordinates) == 3:
            return True
    elif s.type == 'SUB':
        if len(s.coordinates) == 3:
            return True
    elif s.type == 'DES':
        if len(s.coordinates) == 2:
            return True
    else:
        return False

def check_horizontal_vertical(s: 'Ship') -> bool:
    '''checks if ship is horizontal'''
    A = list(s.coordinates)
    B = A[0][0]
    C = A[0][1]
    for i in s.coordinates:
        if i[0] != B and i[1] != C:
            return False
    return True

def check_valid_points(s: 'Ship') -> bool:
    '''checks if coordinates are valid positions'''
    A = list(s.coordinates)
    for i in A:
        B = i[0] #letter
        C = i[1] #number
        if B not in Alphabet[0:len(x)] or int(C) not in range(len(x)):
            return False
    else:
        return True

def check_key(s: 'Ship') -> bool:
    '''checks if keys (ship names) are valid'''
    if s.type == 'CAR' or s.type == 'BAT' or s.type == 'CRU' or s.type == 'SUB' or s.type == 'DES':
        return True
    else:
        return False

def check_overlap(D: '{Ship}') -> bool:
    '''checks if ship coordinates overlap'''
    big_set = {}
    big_list = []
    for i in D: ##accesses the player's dictionary of ships
        big_list.extend(list(D[i].coordinates))
        big_set = set(big_list)
    if len(big_set) < len(big_list):
        return False
    else:
        return True
    
def check_duplicate_ship(D: '{Ship}') -> bool:
    '''checks for multiple of the same ship'''
    type_list = []
    type_set = {}
    for i in D:
        type_list.extend(D[i].type)
        type_set = set(type_list)
    if len(type_set) < len(type_list):
        return False
    else:
        return True
    
def read_menu_with_ship(file_name: str) -> '{Ship}':
    '''reads a file and returns a  Ship'''
    infile = open(file_name, 'r')
    data = infile.read()
    lines = data.split('\n')
    D = {}
    for i in lines:
        D[read_ship(i).type] = read_ship(i)#creates dictionary for each ship
    for i in D:
        if not ship_length(D[i]):
            print('Error. Probelm reading the file.')
        if not check_valid_points(D[i]):
            print('Error. Probelm reading the file.')
        if not check_horizontal_vertical(D[i]):
            print('Error. Probelm reading the file.')
        if not check_key(D[i]):
            print('Error. Probelm reading the file.')
    if not check_overlap(D):
        print('Error. Probelm reading the file.')
    if not check_duplicate_ship(D):
        print('Error. Probelm reading the file.')
    return Player(board_print(x), board_print(x), D)
        

def read_ship(x: str) -> 'Ship': #Creating Ship namedtuple
    '''takes in a string and returns it as a Ship namedtuple'''
    fields = x.split(',')
    ship = Ship(fields[0],len(fields)-1, set(fields[1:]))
    return ship



#P1_ships = read_menu_with_ship('p1.txt')

#P1 = Player(P1_target, P1_ocean, P1_ships)


CRU = Ship(type='CRU', health=3, coordinates={'C2', 'C3', 'C1'})
