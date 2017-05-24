def new_screen(rows: int, columns: int) -> '2D list':
    '''
    Create and return an empty screen: a list of rows with each row
    being a list of pixels going across that row. Initially, all pixels will be 0
    (black).
    '''
    result = []
    for r in range(rows):
        result.append([0] * columns)
    return result

assert new_screen(4,2) == [ [0,0], [0,0], [0,0], [0,0] ]

screen = new_screen(10,5)
#print(screen)

def print_screen(s: '2D list') -> None:
    ''' print the 2D list in a matrix-like format
    '''
    for row in range(len(s)):
        for col in range(len(s[0])):
            if s[row][col] == 0:
                pixel = '#'
            else:
                pixel = ' '
            print(pixel, sep='', end='')
        print() # newline for the end of row
    return

print_screen(screen)
print()
screen[2][3] = 1
print_screen(screen)


def set_row(s: '2D list', rownum: int, value: int) -> None:
    ''' Change the screen so that the specified row has the specified
        value across
    '''
    for col in range(len(s[rownum])):
        s[rownum][col] = value
    return

print()
print()
print_screen(screen)
print()
set_row(screen, 7, 1)
print_screen(screen)
print()
