
Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#Stage 1

def new_screen(rows: int, columns: int) -> '2D list':
    '''
    Create and return an empty screen: a list of rows with each row
    being a list of pixels going across that row. Initially, all pixels will be 0
    (black).
    '''
    result = []
    for r in range(rows): #for every row, you're going to have 'x' columns
        result.append([0] * columns)
    return result

x = new_screen(10,10)
#print(x)

def board_print(T: '2D table') -> None:
    '''Print out table in nice format'''
    s = "   " #3 spaces
    for i in range(len(T[0])):
        s += str(i) + " "
    print(s)
    for row in range(len(T)):
        print("{:1s} ".format(Alphabet[row]), end = "")
        for col in range(len(T[0])):
            print("{:2d}".format(T[row][col]), sep='', end = '')
        print()
    return

from collections import namedtuple

Ship = namedtuple('Ship', 'type health coordinates')
Player = namedtuple('Player', 'target ocean ship')



def ship_length(L: 'list') -> bool:
    '''checks for correct ship length'''
    if L[0] == 'CAR':
        if len(L) - 1 == 5:
            return True
    elif L[0] == 'BAT':
        if len(L) - 1 == 4:
            return True
    elif L[0] == 'CRU':
        if len(L) - 1 == 3:
            return True
    elif L[0] == 'SUB':
        if len(L) - 1 == 3:
            return True
    elif L[0] == 'DES':
        if len(L) - 1 == 2:
            return True
    else:
        return False


def check_horizontal_vertical(L: 'list') -> bool:
    '''checks if ship is horizontal'''
    A = list(L[1:])
    B = A[0][0]
    C = A[0][1]
    for a in A:
        if a[0] != B and a[1] != C:
            return False
    return True

        
def check_valid_points(L: 'list') -> bool:
    '''checks if coordinates are valid positions'''
    A = list(L[1:])
    for a in A:
        B = a[0] #letter
        C = a[1] #number
        if B not in Alphabet[0:len(x)] or int(C) not in range(len(x)):
            return False
    else:
        return True
    

def check_key(L: 'list') -> bool:
    '''checks if keys (ship names) are valid'''
    if L[0] == 'CAR' or L[0] == 'BAT' or L[0] == 'CRU' or L[0] == 'SUB' or L[0] == 'DES':
        return True
    else:
        return False


def check_overlap(L: 'ship_data') -> bool:
    '''checks if ship coordinates overlap'''
    big_set = {}
    big_list = []
    for i in L: ##accesses the player's dictionary of ships
        big_list.extend(list(i[1:]))
        big_set = set(big_list)
    if len(big_set) < len(big_list):
        return False
    else:
        return True
    
def check_duplicate_ship(L: 'ship_data') -> bool:
    '''checks for multiple of the same ship'''
    type_list = []
    type_set = {}
    for i in L:
        type_list.append(i[0])
        type_set = set(type_list)
    if len(type_set) < len(type_list):
        return False
    else:
        return True

def check_file(file_name: 'str') -> bool:
    '''check file for conditions so it can be used in battleship game'''
    infile = open(file_name, 'r')
    data = infile.read()
    lines = data.split('\n')
    ship_data = []
    for i in lines:
        ship_data.append(i.split(','))
    for i in ship_data:
        if not ship_length(i):
            return False
        if not check_horizontal_vertical(i):
            return False
        if not check_valid_points(i):
            return False
        if not check_key(i):
            return False
    if not check_overlap(ship_data):
        return False
    if not check_duplicate_ship(ship_data):
        return False
    else:
        return True

check_file('p1.txt')
'''
infile = open('p1.txt', 'r')
data = infile.read()
lines = data.split('\n')
ship_data = []
for i in lines:
    ship_data.append(i.split(','))
print(ship_data)
'''
def views (rows:int, cols: int)->'2D table':
    '''Create the ocean view and target view for both players'''
    Table = []
    for row in range(rows):
        Table.append(["_"]*cols)
    return Table

#print (views(10,10))

def views_print (T:'2D table')->list:
    '''print out the view in a format
    '''
    s = '   '# 4 space
    for rows in range(len(T[0])):
        s += str(rows)+' '
    print(s)
    
    for row in range(len(T)):
        print ("{:2s}:".format(Alphabet[row]),end='')
        for col in range(len(T[0])):
            print ("{:2s}".format(T[row][col]), sep='', end='')
        print()
    return T

x=views(10,10)
#views_print(x)

def ship_location (T:list, order: str, rows:str, cols:str)-> bool:
    ''' replace '_' to '*' in the 2D table'''
    
    r = ord(rows) - 65
    c = int(cols)
    if r > 9:
        print ('Error. Invalid rows. Must be between A and J')
        return False
    if c > 9:
        print ('Error. Invalid cols. Must be between 0 and '+ str(len(T[0])-1))
        return False

    T[r][c] = order
    views_print(T)
    return True
#ship_location (x,'*', 5, 5)
#ship_location (x,'*',6,5)
#views_print(x)

def get_location (F:'file')->list:
    '''Read ship locations from a specific file
    '''
    C=[]
    infile = open(F,'r')
    data = infile.readlines()
    for ships in data:
        a=ships.split(',')
        for coordinates in a[1:]:
            C.append(coordinates)
    infile.close()
    return C

def read_location(l:list):
    for i in l:
        row=str(i[0])
        column=str(i[1])
        ship_location(x,'*',row,column)
    return

def player1_OV (n:'file')->list:
    '''print player 1's ocean view
    '''
    list1=get_location(n)
    read_location(list1)
    return views_print(x)

def player2_OV (n:'file')->list:
    '''print player 2's ocean view
    '''
    list2=get_location('p2.txt')
    read_location(list2)
    return views_print(x)

#Stage 2

def Game_new() -> list:
    '''return a new list
    '''
    return []

def Battleship (): # similar to lab 6 part G (The restaurants program)
    '''Main Program
    '''
    print ()
    print('--------- BATTLESHIP! ---------')
    ship = Game_new()
    ship = handle_commands1(ship)

MENU1="""
N:    New Game
Q:    Quit
Enter command:
"""

def handle_commands1 (L:list) -> list:
    '''Display menu, accept and process commands
    '''
    while True:
        response = input (MENU1)
        if response.upper() == 'Q':
            print ('\nThank you. Good-bye')
            break
        elif response.upper() == 'N':
            n = views_print(x)
            m = ship_health('p1.txt','p2.txt')
            ship = Game_new()
            q = handle_commands2(ship)
        else:
            invalid_command(response)
            
def invalid_command(response):
    '''Print message for invalid menu command
    '''
    print ('Invalid command: Please re-enter command. ')

MENU2='''

O: Print Ocean View
F: Fire at player

'''

def handle_commands2 (L:list)->list:
    '''Display Menu2, accept and process commands
    '''
    while True:
        response = input (MENU2)
        if response.upper() == 'O':
            n = player1_OV ('p1.txt')
        elif response.upper() == 'F':
            n = attack_ship()
        else:
            invalid_command(response)


def ship_health (p1:'file', p2:'file')->list:
    '''return a list contains ship health for each ship'''
    print('Player 1 Ships HP   Player 2 Ships HP')
    A=[]
    B=[]
    infile1 = open (p1,'r')
    data1 = infile1.readlines()
    for i in data1:
        l=i.split(',')
        A.append("{:3s} - {:2d}".format(l[0],len(l)-1))
    infile2 = open (p2,'r')
    data2 = infile2.readlines()
    for x in data2:
        n=x.split(',')
        B.append("{:3s} - {:2d}".format(n[0],len(n)-1))
    for ii in range(len(A)):
        print("{:7s}              {:7s}".format(A[ii], B[ii]))
    
def attack_ship ()->list:
    '''input the coordinates that player wants to attack, and mark on the ocean view with
    a "X"
    '''
    A = input("Enter target's coordinate [A-J][0-9] to fire at: ")
    B = A.upper().split()
    for i in B:
        rows = i[0]
        cols = i[1]
    return ship_location (x,'X',rows,cols)
    
Battleship()
