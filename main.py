import numpy as np

'''
Function rotateMatrixLeft() takes in matrix and width
as input, and returns the new matrix that is rotated counter-clockwise
'''
def rotateMatrixLeft(matrix, width):

    # Initializes new matrix
    newMatrix = []

    # Keeps track of the newMatrix's indexes
    ind = 0

    # Loops through input maxtrix to create left rotated matrix
    for col in reversed(range(width)):
        newMatrix.append([])
        for row in range(width):
            newMatrix[ind].append(matrix[row][col])
        ind += 1

    # Returns the rotates matrix
    return newMatrix



'''
Function rotateMatrixRight() takes in matrix and width
as input, and returns the new matrix that is rotated clockwise
'''
def rotateMatrixRight(matrix, width):

    # Initializes new matrix
    newMatrix = []

    # Loops through input maxtrix to create right rotated matrix
    for col in range(width):
        newMatrix.append([])
        for row in reversed(range(width)):
            newMatrix[col].append(matrix[row][col])

    # Returns the rotates matrix
    return newMatrix



'''
Function gravity() takes in matrix and width as input,
and returns the new matrix.
When the board is rotated, some chips are floating and 
must fall with 'gravity' to the bottom of the board.
'''
def gravity(matrix, width):

    # Array that holds 2d array of all columns
    # with each column in order of bottom to top
    cols = rotateMatrixLeft(matrix, width)
    allColumns = []
    for i in range(width):
        allColumns.append([])
        for j in reversed(cols[i]):
            allColumns[i].append(j)

    # Finds all the 1s or 2s from all columns
    colChips = []
    for i in range(width):
        colChips.append([])
        zeroCount = 0
        for j in range(width):
            if allColumns[i][j] != 0:
                colChips[i].append(allColumns[i][j])
            else:
                zeroCount += 1

        # Handles the 0s at the end
        if zeroCount>0:
            for k in range(zeroCount):
                colChips[i].append(0)

    # Final matrix is created by rotating right in reverse order
    newMatrix = rotateMatrixRight(colChips, width)[::-1]


    return newMatrix



'''
Function dropChip() takes in matrix, width, and player
as input, and returns the board with the new chip
'''
def dropChip(matrix, width, player):

    # User can input which column to drop their chip
    print('\nDrop your chip in one of the columns!')
    dropLocation = input('Type 1, 2, 3, 4, 5, 6, or 7: ')

    # Handles invalid inputs for the dropLocation
    invalid = True
    while invalid:
        # Handles if input is not a number
        if not dropLocation.isdigit():
            print('You must choose a column number!')
            dropLocation = input('Type 1, 2, 3, 4, 5, 6, or 7: ')
        # Handles if input number is invalid
        elif int(dropLocation) > 7 or int(dropLocation) < 1:
            print('You must choose a valid column number!')
            dropLocation = input('Type 1, 2, 3, 4, 5, 6, or 7: ')
        # Handles if column is full
        elif matrix[0][int(dropLocation)-1] != 0:
            print('Cannot drop chip on column', dropLocation)
            dropLocation = input('Type 1, 2, 3, 4, 5, 6, or 7: ')
        else:
            invalid = False

    dropLocation = int(dropLocation)

    # Finds first open spot from the bottom for chip to fall
    for row in reversed(range(width)):
        if matrix[row][dropLocation-1] == 0:
            matrix[row][dropLocation-1] = player
            break

    # Prints the board with the new chip
    print("Chip was dropped: ")
    for i in range(width):
        print(matrix[i])

    return matrix



'''
Function rotateBoard() takes in matrix and width as input
and returns the rotated board
'''
def rotateBoard(matrix, width):

    # User can input if they want to rotate the board left or right
    print('\nRotate the board left or right!')
    rotation = input('Type left or right: ')

    # Handles invalid input for rotations
    invalid = True
    while invalid:
        if rotation == 'left':
            invalid = False
        elif rotation == 'right':
            invalid = False
        else:
            rotation = input('Type left or right: ')

    # Rotates the board left (counter-clockwise) or right (clockwise)
    rotatedMatrix = []
    if rotation == 'left':
        rotatedMatrix = rotateMatrixLeft(matrix, width)
    else:
        rotatedMatrix = rotateMatrixRight(matrix, width)

    return rotatedMatrix



'''
Function checkWin() takes matrix, width, and winner 
as input, and returns flag and winner as output.
Finds if there is a four in a row found in the 
rows, columns, or diagonals, and which player/s is the winner.
'''
def checkWin(matrix, width, winner):

    # Flag is True while there is no winner
    # Flag becomes False when a winner is found
    flag = True

    # Keeps track of which player/s win
    multiWinners = []

    # Checks rows for a four in a row
    for i in range(width):
        a = ''.join(str(j) for j in matrix[i])
        #allLines.append(a)

        if '1111' in a:
            multiWinners.append(1)
        if '2222' in a:
            multiWinners.append(2)

    # Checks columns for a four in a row
    colMatrix = rotateMatrixLeft(matrix, width)
    for i in range(width):
        b = ''.join(str(j) for j in colMatrix[i])
        if '1111' in b:
            multiWinners.append(1)
        if '2222' in b:
            multiWinners.append(2)
    
    # Checks diagonals for a four in a row
    c = np.array(matrix).reshape(7,7)
    diags = [c[::-1,:].diagonal(i) for i in range(-c.shape[0]+1,c.shape[1])]
    diags.extend(c.diagonal(i) for i in range(c.shape[1]-1,-c.shape[0],-1))
    diagonalList = [n.tolist() for n in diags]
    for i in range(len(diagonalList)):
        d = ''.join(str(j) for j in diagonalList[i])
        if '1111' in d:
            multiWinners.append(1)
        if '2222' in d:
            multiWinners.append(2)
    
    # Determines which player wins or if there's a tie
    if len(multiWinners) > 0:
        flag = False
        if len(multiWinners) > 1:
            winner = 3
        else:
            winner = multiWinners[0]
    

    return flag, winner



'''
Function turn() has matrix, width, player, round, flag, and winner as input and output.
One player's turn consists of dropping a chip and rotating the board, 
then a win is checked if there are four chips in a row found.
'''
def turn(matrix, width, player, round, flag, winner):

    # Shows current round and player
    print('\n----------------------------------------')
    round+=1
    print('Round: ', round)
    print('Turn: Player ', player)

    # Prints the current board
    print()
    print('Current Board: ')
    for i in range(width):
        print(matrix[i])

    # Calls the dropChip() function to place one new chip in a column
    chipMatrix = dropChip(matrix, width, player)

    # Calls the rotateBoard() funciton to rotate the board
    rotatedMatrix = rotateBoard(chipMatrix, width)

    # Calls the gravity() function to allows chips to fall
    finalMatrix = gravity(rotatedMatrix, width)

    # When there is at least 8 chips on the board,
    # Checks if there is a winner with four in a row
    if round > 7:
        flag, winner = checkWin(finalMatrix, width, winner)

    # Switches the player
    if player == 1:
        player = 2
    else:
        player = 1
    
    # Prints the current board
    print()
    print('Current Board: ')
    for i in range(width):
        print(finalMatrix[i])

    return finalMatrix, width, player, round, flag, winner
        
    



def main():
 
    # User can play a game or quit
    playing = True
    while playing:
        print('\n----------------------------------------')
        print("Connect Four with a Twist!")
        mode = input('Play or Quit ? ')
        if mode == 'Quit' or mode == 'quit' or mode == 'q':
            playing = False
            exit(1)

        # Initial empty game board
        gameBoard = [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]]
        
        # Game's starting state
        width = len(gameBoard)
        player = 1
        round = 0
        flag = True
        winner = 0

        # Users take turns until there is a winner
        while flag:
            gameBoard, width, player, round, flag, winner = turn(gameBoard, width, player, round, flag, winner)

        # Prints the winning message
        print()
        if winner == 3:
            print("It's a tie!")
        else:
            print('The winner is Player ', winner, '!')



if __name__ == "__main__":
    main()