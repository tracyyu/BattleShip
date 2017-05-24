

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
            #print("{:2s}".format(T[row][col]), sep='', end = '')
            if T[row][col] == '*': #not a zero, ship position for ocean view
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
    L = L[1:]
    L.sort()
    for i in range(len(L)-1):
        if L[i][1] == L[i+1][1]: #if the # are the same
            if ord(L[i][0]) + 1 != ord(L[i+1][0]):#if the letters are not the +1
                return False
        if L[i][0] == L[i+1][0]: #letters are the same
            if int(L[i][1]) + 1 != int(L[i+1][1]): # the # part has to be +1 from each coord
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
    infile.close()
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

def read_ship(x: str) -> 'Ship': #Creating Ship namedtuple
    '''takes in a string and returns it as a Ship namedtuple'''
    fields = x.split(',')
    ship = Ship(fields[0],len(fields)-1, set(fields[1:]))
    return ship


#check_file('p1.txt')

        
def convert_coordinate(s: 'coordinate'): 
    '''convert coordinate into int'''
    s = str(s)
    a = list(s)
    letter_convert = ord(a[0]) - ord('A')
    b = a[1]
    return letter_convert, int(b)

def set_pixel(s: '2D list', rownum: int, colnum: int, value: str) -> None:
    ''' Change the screen so that the specified pixel has the specified
        value
    '''
    s[rownum][colnum] = value
    
#board_print(x)


def create_ocean(file_name: str) -> list:
    '''creates ocean view'''
    p_board = new_screen(10,10)
    infile = open(file_name, 'r')
    data = infile.read()
    lines = data.split('\n')
    infile.close()
    ship_data = []
    for i in lines:
        ship_data.append(i.split(','))
    for i in ship_data:
        for j in i[1:]: #j is every coordinate in the file
            s = convert_coordinate(j)
            set_pixel(p_board, s[0], s[1], '*')
    return p_board

def create_target(file_name: str) -> list:
    '''creates target view'''
    p_board = new_screen(10,10)
    infile = open(file_name, 'r')
    data = infile.read()
    infile.close()
    ####use set_pixel to change when player misses or hits in another function
    return p_board

import sys ##temp solution

def make_player(file_name: 'str') -> 'Player':
    '''creates player profile'''
    if not check_file(file_name):
        print("Problem reading file, Program will terminate")
        sys.exit() ###temp solution
    else:
        infile = open(file_name, 'r')
        data = infile.read()
        lines = data.split('\n')
        infile.close()
        D = {}
        for i in lines:
            D[read_ship(i).type] = read_ship(i)
        return Player(create_target(file_name), create_ocean(file_name), D)
        

######Stage 2#####

#want to check input matches other player's ocean view
#P1 fires at A1, check P2's ocean view if the A1 coordinate value is a *
#use convert coordinate to return coordinate into #'s

def remove_coordinate(c: 'coordinate', p: 'Player') -> None:
    '''remove the coordinate if its a hit in the opponent's ship dictionary'''
    for i in p.ship: #player's dictionary of ships
        if c in p.ship[i].coordinates: #for every coordinate in ship's coord set
            #p.ship[i].coordinates.discard(c)
            p.ship[i] = p.ship[i]._replace(health = p.ship[i].health - 1)
            break
    
    
def check_if_ship(c: 'coordinate', player_id: int, P1: 'Player1', P2: 'Player2') -> bool:
    '''checks if coordinate is in player's ocean view'''
    a = convert_coordinate(c)
    if player_id%2 != 0: #player 1 firing, need to check player 2's ocean view
        return P2.ocean[a[0]][a[1]] == '*'
    if player_id%2 == 0: # player 2 firing, need to check player 1's ocean view
        return P1.ocean[a[0]][a[1]] == '*'

def check_if_hit(c: 'coordinate', player_id: int, P1: 'Player1', P2: 'Player2') -> bool:
    '''checks if coordinate is in player's ocean view'''
    a = convert_coordinate(c)
    if player_id%2 != 0: #player 1 firing, need to check player 2's ocean view
        return P2.ocean[a[0]][a[1]] == 'X'
    if player_id%2 == 0: # player 2 firing, need to check player 1's ocean view
        return P1.ocean[a[0]][a[1]] == 'X'

def check_already_fired(c: 'coordinate', player_id: int, P1: 'Player1', P2: 'Player2') -> bool:
    '''checks if coordinate is 'M' or 'H' for player firing in target view'''
    a = convert_coordinate(c)
    if player_id%2 != 0:
        if P1.target[a[0]][a[1]] == 'M' or P1.target[a[0]][a[1]] == 'H':
            return True
        else:
            return False
    if player_id%2 == 0:
        if P2.target[a[0]][a[1]] == 'M' or P2.target[a[0]][a[1]] == 'H':
            return True
        else:
            return False
    
def fire(c: 'coordinate', player_id: int, P1: 'Player1', P2: 'Player2') -> None:
    '''returns list of opponent's ocean view and turn player's target view'''
    a = convert_coordinate(c)
    if check_if_ship(c, player_id,P1,P2):
        if player_id%2 != 0: #player 1's turn
            set_pixel(P1.target, a[0], a[1], 'H')
            set_pixel(P2.ocean, a[0], a[1], 'X')
            remove_coordinate(c, P2)
        elif player_id%2 == 0: #player 2's turn
             set_pixel(P2.target, a[0], a[1], 'H')
             set_pixel(P1.ocean, a[0], a[1], 'X')
             remove_coordinate(c, P1)
    else:
        if player_id%2 != 0: #player 1's turn
            set_pixel(P1.target, a[0], a[1], 'M')
        elif player_id%2 == 0: #player 2's turn
            set_pixel(P2.target, a[0], a[1], 'M')

def search_ship(c: 'coordinate',player_id: int, P1: 'Player1', P2: 'Player2') -> str:
    '''given a coordinate, find what ship it is for the player'''
    s = str(c)
    if player_id%2 != 0:
        for i in P2.ship:
            if s in P2.ship[i].coordinates:
                return P2.ship[i].type
    if player_id%2 == 0:
        for i in P1.ship:
            if s in P1.ship[i].coordinates:
                return P1.ship[i].type

def convert_str_ship(s: str) -> None:
    '''prints ship name depending on type'''
    if s == 'CAR':
        return 'Carrier'
    elif s == 'BAT':
        return 'Battleship'
    elif s == 'CRU':
        return 'Cruiser'
    elif s == 'SUB':
        return 'Submarine'
    elif s == 'DES':
        return 'Destroyer'
    
        
#P1 = make_player('p1.txt')
#P2 = make_player('p2.txt')
#assert check_if_hit(0,0,1) == False  #check if A0 is in P2's ocean
#assert check_if_hit(2,4,1) == True   #check if C4 is in P2's ocean
            
def ship_health(P1: 'Player1', P2: 'Player2') -> None:
    '''prints each player's ships health'''
    print("Player 1 Ships HP   Player 2 Ships HP")
    print("CAR - {}             CAR - {}".format(P1.ship['CAR'].health,P2.ship['CAR'].health))
    print("BAT - {}             BAT - {}".format(P1.ship['BAT'].health,P2.ship['BAT'].health))
    print("CRU - {}             CRU - {}".format(P1.ship['CRU'].health,P2.ship['CRU'].health))
    print("SUB - {}             SUB - {}".format(P1.ship['SUB'].health,P2.ship['SUB'].health))
    print("DES - {}             DES - {}".format(P1.ship['DES'].health,P2.ship['DES'].health))
    

def valid_coordinate(c: 'coordinate') -> bool:
    '''checks if user input is a valid coordinate'''
    return str(c)[0] in Alphabet[0:len(x)] and int(c[1:]) in range(len(x))

def invalid_coordinate():  # string -> interaction
    """ return response for user to enter a new coordinate.
    """    
    response = input("Invalid coordinate. Please enter coordinate [A-J][0-9]: ")
    return response

def already_hit():
    '''return response for user to enter a new coordinate.
    '''
    response = input("Please enter another coordinate [A-J][0-9]: ")
    return response

def invalid_command(response):  # string -> interaction
    """ Print message for invalid menu command.
    """    
    response = input("Invalid command: Please re-enter command: ")
    return response
    

######Stage 3

def check_total_hits(t: '[Player_target_view]') -> int:
    '''finds how many "H" are in Player's target view'''
    total = 0
    for row in range(len(t)):
        for col in range(len(t[0])):
            if t[row][col] == 'H':
                total += 1
    return total


def check_total_misses(t: '[Player_target_view]') -> int:
    '''finds how many "M" are in Player's target view'''
    total = 0
    for row in range(len(t)):
        for col in range(len(t[0])):
            if t[row][col] == 'M':
                total += 1
    return total

def oceanview_coord(P: 'Player') -> list:
    '''returns list of coordinates which have not been hit'''
    result = []
    for i in P.ship:
        for j in P.ship[i].coordinates:
            result.append(j)
    return result
    




def create_gamefile(file_name: str, P1TH: str,P2TH: str, P1TM: str, P2TM: str,P1OM: list, P2OM: list,a: list, b: list, P1: 'Player1',P2: 'Player2',turn: int): ###way w/o passing parameters?
    '''creates txt file of current gamestate'''
    file = open(file_name, 'w')
    #####Player 1
    file.write(",".join(P1TH) + '\n')
    file.write(",".join(P1TM) + '\n')
    file.write(",".join(P2TH) + '\n')
    file.write(",".join(P1OM) + '\n')
    for i in P1.ship:
        ship = []
        ship.append(P1.ship[i].type)
        ship.append(str(P1.ship[i].health))
        for j in P1.ship[i].coordinates:
            ship.append(j)
        file.write(",".join(ship)+'\n')
    P1THM = [str(a[0]),str(a[1]),str(a[2])]
    file.write(",".join(P1THM) + '\n')
    ####Player 2
    file.write(",".join(P2TH) + '\n')
    file.write(",".join(P2TM) + '\n')
    file.write(",".join(P1TH) + '\n')
    file.write(",".join(P2OM) + '\n')
    for i in P2.ship:
        ship = []
        ship.append(P2.ship[i].type)
        ship.append(str(P2.ship[i].health))
        for j in P2.ship[i].coordinates:
            ship.append(j)
        file.write(",".join(ship)+'\n')
    P2THM = [str(b[0]),str(b[1]),str(b[2])]
    file.write(",".join(P2THM) + '\n')
    if turn%2 != 0:
        file.write("P1")
    else:
        file.write("P2")
    


def create_oceanP1(file_name: str) -> list:
    '''creates ocean view'''
    p_board = new_screen(10,10)
    infile = open(file_name, 'r')
    data = infile.read()
    lines = data.split('\n')
    ship_data = []
    for i in lines:
        ship_data.append(i.split(','))

    for i in ship_data[2]:
        if i != '':
            s = convert_coordinate(i)
            set_pixel(p_board, s[0], s[1], 'X')

    for i in ship_data[3]:
        if i != '':
            s = convert_coordinate(i)
            set_pixel(p_board, s[0], s[1], '*')
    return p_board

def create_oceanP2(file_name: str) -> list:
    '''creates ocean view'''
    p_board = new_screen(10,10)
    infile = open(file_name, 'r')
    data = infile.read()
    lines = data.split('\n')
    ship_data = []
    for i in lines:
        ship_data.append(i.split(','))

    for i in ship_data[12]:
        if i != '':
            s = convert_coordinate(i)
            set_pixel(p_board, s[0], s[1], 'X')

    for i in ship_data[13]:
        if i != '':
            s = convert_coordinate(i)
            set_pixel(p_board, s[0], s[1], '*')
    return p_board

def read_ship2(x: str) -> 'Ship': #Creating Ship namedtuple
    '''takes in a string and returns it as a Ship namedtuple'''
    fields = x.split(',')
    ship = Ship(fields[0],int(fields[1]), set(fields[2:]))
    return ship

def read_file(file_name: str):
    '''reads game.txt (saved) and loads file'''
    infile = open(file_name, 'r')
    data = infile.read()
    lines = data.split('\n')
    ship_data = []
    #print(lines)
    for i in lines:
        ship_data.append(i.split(','))
    #print(ship_data)
    #####Player 1
    P1T = create_target(file_name)
    for i in ship_data[0]:
        if i != '':
            a = convert_coordinate(i)
            set_pixel(P1T, a[0],a[1],'H')
    for i in ship_data[1]:
        if i != '':
            a = convert_coordinate(i)
            set_pixel(P1T, a[0],a[1], 'M')
    P1O = create_oceanP1(file_name)
    P1D = {}
    for i in lines[4:9]:
        P1D[read_ship2(i).type] = read_ship2(i)
    P1S = []
    for i in ship_data[9]:
        P1S.append(int(i))
    P1TH = []
    for i in ship_data[0]:
        P1TH.append(i)
    P1TM = []
    for i in ship_data[1]:
        P1TM.append(i)
    P1OM = []
    for i in ship_data[3]:
        P1OM.append(i)
    #####Player 2
    P2T = create_target(file_name)
    for i in ship_data[10]:
        if i != '':
            a = convert_coordinate(i)
            set_pixel(P2T, a[0],a[1],'H')
    for i in ship_data[11]:
        if i != '':
            a = convert_coordinate(i)
            set_pixel(P2T, a[0],a[1], 'M')
    P2O = create_oceanP2(file_name)
    P2D = {}
    for i in lines[14:19]:
        P2D[read_ship2(i).type] = read_ship2(i)
    P2S = []
    for i in ship_data[19]:
        P2S.append(int(i))
    P2TH = []
    for i in ship_data[10]:
        P2TH.append(i)
    P2TM = []
    for i in ship_data[11]:
        P2TM.append(i)
    P2OM = []
    for i in ship_data[13]:
        P2OM.append(i)
    player_turn = 0
    if ship_data[20] == ['P1']:
        player_turn = 1
    else:
        player_turn = 2
    P1 = Player(P1T, P1O, P1D)
    P2 = Player(P2T,P2O,P2D)
    return P1,P2,P1S,P2S,player_turn,P1TH,P1TM,P1OM,P2TH,P2TM,P2OM
    
    #print(P1D)
    #board_print(P1O)
    #board_print(P1T)
    #print(P1S)
    #print(P2D)
    #board_print(P2O)
    #board_print(P2T)
    #print(P2S)
    
    
########Stage 4

def check_win(P: 'Player') -> bool:
    '''checks which player won'''
    for i in P.ship:
        if P.ship[i].health != 0:
            return False
        else:
            return True



def game_stats(a: 'Player1stats', b: 'Player2stats') -> None:
    '''prints each player's ships health'''
    print("        Player 1 Stats       Player 2 Stats")
    print("{:8s}{:<20d}{:2d}".format('Moves:',a[0],b[0]))
    print("{:8s}{:<20d}{:2d}".format('Misses:',a[2],b[2]))
    print("{:8s}{:<20d}{:2d}".format('Hits:',a[1],b[1]))
    print("{:8s}{:<20.3f}{:6.3f}".format('Hit%:',(a[1]/a[0])*100,(b[1]/b[0])*100))
    print("{:8s}{:<20.3f}{:6.3f}".format('Miss%:',(a[2]/a[0])*100,(b[2]/b[0])*100))




def battleship():  # nothing -> interaction
    """ Main program
    """
    print("--------- BATTLESHIP! ---------")
    handle_commands()
    
START_MENU = """
 L:  Load Game (game.txt)
 N:  New Game
 Q:  Quit
 Enter command:
"""
CONTINUE_MENU = """
 O: Print Ocean View
 F: Fire at player
 S: Save game
 Enter command:
"""

def handle_commands():
    '''displays commands and menu'''
    player_turn = 1
    response = input(START_MENU)
    while True:
        if response.lower() == "n":
            P1 = make_player('p1.txt')
            P2 = make_player('p2.txt')
            P1TH = [] #keep track of P1 coordinates that were 'hits' in target view
            P2TH = []
            P1TM = [] #keep track of P1 coordinates that were 'miss' in target view
            P2TM = [] 
            P1OM = oceanview_coord(P1) #all coordinates in ocean view that haven't been hit
            P2OM = oceanview_coord(P2)
            a = [0,0,0] #[moves,hit,misses]
            b = [0,0,0]
            #For ocean view hit/miss, P1 ocean hits = P2 target hits, vice versa
            #can use ",".join() to make A1,A2,A3 etc...
            while True:
                if player_turn % 2 != 0:
                    print("Player {}'s Turn".format(1))
                    board_print(P1.target)
                else:
                    print("Player {}'s Turn".format(2))
                    board_print(P2.target)
                ship_health(P1,P2)
                #print("P1 hits: ", P1TH) ##testing statements
                #print("P1 misses: ", P1TM)
                #print(a)
                #print(P1OM)
                #print(P2OM)

                while True:             
                    response = input(CONTINUE_MENU)
                    if response.lower() == "s":
                        create_gamefile('game.txt', P1TH, P2TH,P1TM,P2TM,P1OM,P2OM,a,b,P1,P2,player_turn)
                        
                    if response.lower() == "o":
                        if player_turn %2 !=0:
                            board_print(P1.ocean)
                        if player_turn %2 == 0:
                            board_print(P2.ocean)
                            
                    if response.lower() == "f":
                        target = input("Enter target's coordinate [A-J][0-9] to fire at: ")
                        while True:
                            if valid_coordinate(target):
                                if not check_already_fired(target, player_turn,P1,P2): #if coord != 'M','H'
                                    ship = convert_str_ship(search_ship(target,player_turn,P1,P2)) #find ship first
                                    fire(target, player_turn, P1, P2)
                                    print(ship)
                                    if check_if_hit(target, player_turn,P1,P2):
                                        print("{} hit!".format(ship))
                                        if player_turn %2 !=0:
                                            P2OM.remove(target) #removes coord in P2's oceanview coord. list
                                            P1TH.append(target)
                                            a[0] += 1 #add 1 to total moves
                                            a[1] += 1 #add 1 to total hits
                                            if check_win(P2):
                                                print("Player 1 wins!")
                                                game_stats(a,b)
                                                sys.exit()
                                                
                                        if player_turn %2 ==0:
                                            P1OM.remove(target)
                                            P2TH.append(target)
                                            b[0] += 1
                                            b[1] += 1
                                            if check_win(P1):
                                                print("Player 2 wins!")
                                                game_stats(a,b)
                                                sys.exit()
                                        
                                            
                                    else:
                                        print("Missed!")
                                        if player_turn %2 !=0:
                                            P1TM.append(target)
                                            a[0] += 1 
                                            a[2] += 1 #add 1 to total misses
                                            
                                        if player_turn %2 ==0:
                                            P2TM.append(target)
                                            b[0] += 1
                                            b[2] += 1
                                            
                                    
                                    player_turn += 1
                                    break
                            
                                elif check_already_fired(target, player_turn,P1,P2):
                                    target = already_hit()
        
                            else:
                                target = invalid_coordinate()
                        break
                                
        if response.lower() == "l":
            file = input("Please type in file name: ")
            P1 = read_file(file)[0]
            P2 = read_file(file)[1]
            a = read_file(file)[2]
            b = read_file(file)[3]
            player_turn = read_file(file)[4]

            P1TH = read_file(file)[5]
            #print(P1TH)
            #P1TH.append('A2')
            #print(P1TH)
            P2TH = read_file(file)[8]
            P1TM = read_file(file)[6]
            P2TM = read_file(file)[9]
            P1OM = read_file(file)[7]
            P2OM = read_file(file)[10]
            #print(P1TH)
            #print(P1TM)
            #print(P2TH)
            #print(P2TM) 
            #print(P1OM)
            #print(P2OM)
            
            while True:
                if player_turn % 2 != 0:
                    print("Player {}'s Turn".format(1))
                    board_print(P1.target)
                else:
                    print("Player {}'s Turn".format(2))
                    board_print(P2.target)
                ship_health(P1,P2)
                

                while True:             
                    response = input(CONTINUE_MENU)
                    if response.lower() == "s":
                        create_gamefile('game.txt', P1TH, P2TH,P1TM,P2TM,P1OM,P2OM,a,b,P1,P2,player_turn)
                        
                    if response.lower() == "o":
                        if player_turn %2 !=0:
                            board_print(P1.ocean)
                        if player_turn %2 == 0:
                            board_print(P2.ocean)
                            
                    if response.lower() == "f":
                        target = input("Enter target's coordinate [A-J][0-9] to fire at: ")
                        while True:
                            if valid_coordinate(target):
                                if not check_already_fired(target, player_turn,P1,P2): #if coord != 'M','H'
                                    ship = convert_str_ship(search_ship(target,player_turn,P1,P2)) #find ship first
                                    fire(target, player_turn, P1, P2)
                                    print(ship)
                                    if check_if_hit(target, player_turn,P1,P2):
                                        print("{} hit!".format(ship))
                                        if player_turn %2 !=0:
                                            P2OM.remove(target) #removes coord in P2's oceanview coord. list
                                            P1TH.append(target)
                                            a[0] += 1 #add 1 to total moves
                                            a[1] += 1 #add 1 to total hits
                                            if check_win(P2):
                                                print("Player 1 wins!")
                                                game_stats(a,b)
                                                sys.exit()
                                            
                                        if player_turn %2 ==0:
                                            P1OM.remove(target)
                                            P2TH.append(target)
                                            b[0] += 1
                                            b[1] += 1
                                            if check_win(P1):
                                                print("Player 2 wins!")
                                                game_stats(a,b)
                                                sys.exit()
                                            
                                    else:
                                        print("Missed!")
                                        if player_turn %2 !=0:
                                            P1TM.append(target)
                                            a[0] += 1 
                                            a[2] += 1 #add 1 to total misses
                                            
                                        if player_turn %2 ==0:
                                            P2TM.append(target)
                                            b[0] += 1
                                            b[2] += 1
                                            
                                    
                                    player_turn += 1
                                    break
                            
                                elif check_already_fired(target, player_turn,P1,P2):
                                    target = already_hit()
        
                            else:
                                target = invalid_coordinate()
                        break
                        
          
        elif response.lower() == "q":
            sys.exit()
        else:
            response = invalid_command(response)
            

    
battleship()

