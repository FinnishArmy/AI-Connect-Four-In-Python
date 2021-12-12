import random
from tkinter import *
import math

class Connect4:
    """
    The initialize function is the function that creates the information
    that goes inside my board created in the __repr__ function.
    """
    def __init__(self, width, height, window):
        self.blue = 'blue'
        self.red = 'red'
        self.width = width #Defining a width to reference
        self.height = height #Defining a height to reference
        self.data = [] #This will be our board of X's and O's.
        self.aiplayer = 'O'
        self.wWidth = 1000 #Canvas Size
        self.wHeight = 950 #Canvas Size
        self.col_select = -1

        self.done = False

        #self.row_count =  7 #Number of rows
        #self.col_count = 7 #Number of columns
        self.diameter = self.wWidth / self.width #Making it so that the size of the circles will scale along with the width and height of the board called.

        self.diff_value = 0 #Ply numebr which will by called by the Player AI.

        self.window = window
        self.frame = Frame(window)
        self.frame.pack() #Packing the frame INTO the Window.

        self.label = Label(self.window, text='Yellows Turn', font = ('Helvetica', 25)) #Prints a Label into the window frame.
        self.label.pack()

        self.label2 = Label(self.window, text='', font = ('Helvetica', 25))
        self.label2.pack()

        self.slide1 = Scale(self.frame, from_= 0, to = 7, resolution = 1, orient = HORIZONTAL, length = 300, command = self.print_diff) #Puts a slider scale into the frame which ranges from 0 to 7.
        self.slide1.pack()
        self.init_color = 'black'

        self.circles = [] #Making a list of circles to append to when I start creating the board in the frame.
        self.colors = [] #Same with the color list, I will also use this to itterate from to figure out when I can change/add a token.


        self.quitButton = Button(window, text = 'QUIT', fg = 'red', command = quit) #Creates a quit button, basically just destroys the window.
        self.quitButton.pack(side = TOP)

        self.draw = Canvas(window, width = (self.width-1) * 170, height = self.height*180, bg = 'blue', borderwidth = 0) #This is the canvas where I will add all the circles to.
        self.draw.bind('<Button-1>', self.mouseInput)
        #self.draw.bind('<Button-1>', self.playGameWith)
        self.draw.pack()
        y = 0 + 2 #My y will be my y value I set in the circleRow when I create them. +2 because I want space between the circles.
        for c in range(self.height):
            circleRow = []
            colorRow = []
            x = 0 + 2 #My x will be my x value I set in the circleRow when I create them. +2 because I want space between the circles.
            for r in range(self.width):
                circleRow += [self.draw.create_oval(x, y, x+self.diameter, y+self.diameter, fill = self.init_color)] #Plus self.diameter because I want the ovals to scale with the board size being called.
                colorRow += [self.init_color] #They will initially be black, so I append black for every oval created.
                x += self.diameter + 2 #Adding the circle size so that the next oval created will be right self.diameter pixels over.
                # if self.data [r][c] == ' ':
                #     circleRow += [self.draw.create_oval(x, y, x+self.diameter, y+self.diameter, fill = "black")]
                # elif self.data [r][c] == 'X':
                #     circleRow += [self.draw.create_oval(x, y, x+self.diameter, y+self.diameter, fill = "red")]
                # else:
                #     circleRow += [self.draw.create_oval(x, y, x+self.diameter, y+self.diameter, fill = "blue")]

            self.circles += [circleRow]
            y += self.diameter + 2 #Adding the circle size so that the next oval created will be right self.diameter pixels over.

            self.circles += [circleRow]
            self.colors += [colorRow]

            #print(self.colors) #Printing out just so I can see what's happening.

            # print(self.circles)
            # print(self.colors)
        """
        This will creates what is inside the board, the 'X' or the 'O'.
        """
        for row in range(height): #Itterates through the columns
            boardRow = [] #Creates a list for each column
            for col in range(width): #Itterates through each row of each column
                boardRow += [' '] #Adds an empty string for each row in each column
            self.data += [boardRow]

    def __repr__(self):
        s = '' #Creating an empty string to add to later.
        for row in range(self.height):
            s += '|' #Creates a '|' for each column.
            for col in range(self.width):
                s += self.data[row][col] + '|' #Then creates a '|' for each row in each column.
            s += '\n' #Making a new line after iterateing through each column.

        s += '--' * self.width + '-\n' #This creates the bars below all the rows.

        for col in range(self.width):
            s += ' ' + str(col % 10) #Creating an empty space inside each row and column, using mod 10 so we only get single digit numbers.
        s += '\n'

        return s

        """
        This function will return the difficuly or ply number that is set by the slider.
        """
    def print_diff(self, val):
        print('Difficulty = ' + val)
        self.diff_value = int(val) #Because the slider returns a string value, I set the difficulty equal to the integer of the returned string.

        """This function will be called in the mouseInput function to
        actually add the colour onto the board.
        """
    def changeColour(self, colorRow, col): #Rather than actually changing the colour, this will just add the colour.
        flag = 0
        for i in range(len(colorRow)): #Grabs the length of the colorRow defined in init, then takes the range of values of the length.
            if colorRow[i][col] == 'black': #Itereates through each column given by the mouseInput function until it finds a black circle.
                flag = i #once it finds a black circle, set the value of flag equal to the row number in that column.

        print(flag)
        return flag #Returns the row number of the column selected.
        """
        Clearing the board is technically just making a whole new board, rather than
        removing each string because that is faster than itterating through each row/column.
        So I copied the code from the __init__ function that created the board.
        """
    def clear(self):
        self.data = [] #This will be our board
        for row in range(self.height): #Itterates through the columns
            boardRow = [] #Creates a list for each column
            for col in range(self.width): #Itterates through each row of each column
                boardRow += [' '] #Adds an empty string for each row in each column
            self.data += [boardRow]

            """
            addMove function is the function that actually adds the move into the __init__ function.
            First it checks if the desired input passes the allowsMove function.
            If so, then it will go through each row until it finds an 'X' or 'O' then add a 'X' or 'X' into the row above it,
            hence the '-1' on row.
            """
    def addMove(self,col,ox):
        if self.allowsMove(col):
            for row in range(self.height):
                if self.data[row][col] != ' ':
                    self.data[row-1][col] = ox
                    return
            self.data[self.height-1][col] = ox

        """
        Allows move checks if the column is full to see if you
        are allowed to proceed with the move.
        """
    def allowsMove(self,col):
        if 0 <= col < self.width:
            return self.data[0][col] == ' ' #Goes through the rows of the column, if there's nothing (empty string) then return True, and allow the move.
        return False #If there is something other than an empty string, then return False and dissalow the move.

        """
        The delete move function does the oppoosite of
        addMove.
        """
    def delMove(self,col):
        for row in range(self.height):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' ' #Add an empty string in place of the 'X' or 'O'. Hence why there is no '-1' in this line.
                return
        self.data[self.height - 1][col] = ' '

        """
        This function will itterate through each column and row.
        It checks if each row in each column is either empty list or contains something inside of it.
        If there is any part of the board that has an empty list, then the board is not full and it will
        return False. If every single row in each column has anything other than an empty list, the board is full
        then return True.
        """
    def isFull(self):
        for row in range(self.width):
            for col in range(self.height):
                if self.data[row][col] == ' ':
                    return False
            return True

            """
            This function tests if the player has won by checking for '4 in a row'.
            """
    def winsFor(self,ox):
        d = self.diameter/2
        #Horizontal Test!:
        for col in range(self.width-3): #Using '-3' because after column 3, a 4 in a row would not be possible.
            for row in range(self.height):
                """ This will add 1 to the column until +3 as then it will be 4 in a row. But only if all 4 are either all 'X' or all 'O', (The previous selected move)."""
                if self.data[row][col] == ox and \
                self.data[row][col+1] == ox and \
                self.data[row][col+2] == ox and \
                self.data[row][col+3] == ox:
                    #print('Win!')
                    # self.draw.create_line(((self.diameter+2)*col)+d, ((self.diameter+2)*row)+d, ((self.diameter+2)*(col+3)+d), ((self.diameter+2)*row)+d, fill = 'black')
                    return True #Return True if it passes horizontal test.

        #Vertical Test!:
        for col in range(self.width):
            for row in range(self.height-3): #Using the '-3' on the height instead of the width since we are checking the vertical test.
                """This will add 1 to the row until +3 as then it will be a 4 in a row. But only if all 4 are either all 'X' or all 'O', (The previous selected move.)"""
                if self.data[row][col] == ox and \
                self.data[row+1][col] == ox and \
                self.data[row+2][col] == ox and \
                self.data[row+3][col] == ox:
                    #print('Win!')
                    # self.draw.create_line(((self.diameter+2)*col)+d, ((self.diameter+2)*row)+d, ((self.diameter+2)*(col)+d), ((self.diameter+2)*(row+3))+d, fill = 'black')
                    return True #Return True if it passes horizontal test.

        #Right Slope Test!:
        for col in range(self.width-3): #Now I'm using -3 on both the width and height because it's a sloped line.
            for row in range(self.height-3):
                """This will add 1 to the row AND column because we are checking a slope of 1. So up 1, right 1. Until +3 as then it will be 4 in a row."""
                if self.data[row][col] == ox and \
                self.data[row+1][col+1] == ox and \
                self.data[row+2][col+2] == ox and \
                self.data[row+3][col+3] == ox:
                    #print('Win!')
                    # self.draw.create_line(((self.diameter+2)*col)+d, ((self.diameter+2)*row)+d, ((self.diameter+2)*(col+3)+d), ((self.diameter+2)*(row+3))+d, fill = 'black')
                    return True #Return True if it passes horizontal test.

        #Left Slope Test!:
        for col in range(3, self.width):
            for row in range(self.height-3): #3rd row up, 3rd index of the list.
                """This will add 1 to just the column and subtract 1 from the row. So up 1, left 1. Until +3 as then it will be  in a row."""
                if self.data[row][col] == ox and \
                self.data[row+1][col-1] == ox and \
                self.data[row+2][col-2] == ox and \
                self.data[row+3][col-3] == ox:
                    #print('Win!')

                    # self.draw.create_line(((self.diameter+2)*col)+d, ((self.diameter+2)*row)+d, (self.diameter+2)*(col-3)+d, (self.diameter+2)*(row+3)+d, fill = 'black')
                    return True #Return True if it passes slope test.

        #False Win Statement:
        #print('No Win')
        return False #I return a false if it does not pass any of the tests.

        """
        Here...
        This is how to actually play the game through the terminal.
        I created 2 functions (basically) inside of this function.
        my if statement acts as my player 1, and my else statement acts as my player 2.
        """
    def hostGame(self):
        board = Connect4(7,6) #Just to reference later. #This will indicate if the game is over, (False = Not over, True = Is Over).
        turn_count = 0 #This will keep track of how many turns are played
        while not self.winsFor('X') or \
        self.winsFor('O'): #Keep playing the game while game_state is False.

        #Player 1 Inputs:
            if turn_count == 0: #If the turn count is 0, then player 1 will go, otherwise, that means it's player 2's turn.
                print(board)
                select_token = int(input('Player 1, pick 0 - 6:')) #Setting this to call later. This must be an int.
                if self.allowsMove(select_token): #If the desired move passes the allowsMove function, then continue... otherwise, line 178.
                    self.addMove(select_token, 'X') #See here, I'm adding a move to the board I created in my hostGame and the actual board.
                    board.addMove(select_token, 'X')
                    print(board) #Prints the board after your move has been placed.
                    if self.winsFor('X'): #This will check for a win, and if you do win, it tells you that player 1 wins, then stops the function.
                        self.message.config(text= 'Player Yellow Wins! Nice Job!')
                        print(board)
                        print('Yellow Wins!')
                        break
                    turn_count +=1 #Adds one to the turn count so that the function knows to switch to player 2, since it's != to 0.

                if self.isFull(): #All this does is check if the board is full, if so, show the board again and say it's a tie.
                    print(board)
                    print('It is a tie!')
                    break
                if not board.allowsMove(select_token):
                    print('Illegal Move, pick something else.')

        #Player 2 Inputs:

            else: #Everything here is the same as the if statement otherthan a couple minor changes.
                print(board)
                select_token = int(input('Player 2, pick 0 - 6:'))
                if self.allowsMove(select_token):
                    self.addMove(select_token, 'O')
                    board.addMove(select_token, 'O')
                    print(board)
                    if self.winsFor('O'):
                        print(board)
                        print('Red Wins!')
                        break
                    turn_count = 0

                if self.isFull():
                    print(board)
                    print('It is a tie!')
                    break

                if not board.allowsMove(select_token):
                    print('Illegal Move, pick something else.')
    def getNextColour(self, row, col):
        colour = self.colors[row][col]
        if colour == 'black':
            colour == 'blue'
        else:
            colour == 'black'


    def mouseInput(self, event):
        AI = Player('O', 'Random', self.diff_value)
        #col_select = int(event.x/self.diameter)
        col = int(event.x/self.diameter)
        row = int(event.y/self.diameter)
        # frame = Tk()
        # frame.title('Connect 4')
        flag = True
        print(col)
        #board = Connect4(7,6, frame) #Just to reference later. #This will indicate if the game is over, (False = Not over, True = Is Over).
        newColour = self.getNextColour(row, col)
        turn_count = 0 #This will keep track of how many turns are played
        if flag == True and \
        self.done == False: #Keep playing the game while game_state is False.
            if self.allowsMove(col) == False:
                return
        #Player 1 Inputs:
            self.label.config(text = 'Yellows Turn')
            if turn_count == 0: #If the turn count is 0, then player 1 will go, otherwise, that means it's player 2's turn.
                print(self)
                self.label.config(text = 'Yellows Turn')
                select_token = col #Setting this to call later. This must be an int.
                if self.allowsMove(select_token): #If the desired move passes the allowsMove function, then continue... otherwise, line 178.
                    self.addMove(select_token, 'X') #See here, I'm adding a move to the board I created in my hostGame and the actual board.
                    y = self.changeColour(self.colors, select_token)
                    self.draw.create_oval((self.diameter+2)*(select_token), (self.diameter+2)*y, (self.diameter+2)*(select_token+1), (self.diameter+2)*(y+1), fill = 'yellow')
                    #y += self.draw.create_oval(select_token*self.diameter, row*self.diameter, select_token*self.diameter, row*self.diameter, fill = 'blue')
                    self.draw.itemconfig(self.circles[row][col], fill=newColour)
                    self.colors[y][select_token] = 'yellow'
                    self.label.config(text = 'Reds Turn')
                    print(y)
                    print(self)
                    if self.winsFor('X'): #This will check for a win, and if you do win, it tells you that player 1 wins, then stops the function.
                        print(self)
                        self.done = True
                        self.label.config(text = 'Yellow Wins!')
                        print('Yellow Wins!')
                        flag = False
                        return
                        #Set false to stop taking moves. self variable.
                    turn_count +=1 #Adds one to the turn count so that the function knows to switch to player 2, since it's != to 0.

                if self.isFull(): #All this does is check if the board is full, if so, show the board again and say it's a tie.
                    #self.draw.itemconfig(self.circles[row][col], fill=newColour)
                    print(self)
                    self.done = False
                    self.label.config(text = "Full Board, it's a tie")
                    print("Full Board, it's a tie")
                    return
                if not self.allowsMove(select_token):
                    print('Illegal Move, pick something else.')
                #self.label.config(text = 'Reds Turn'
            if turn_count != 0:
                self.label.config(text = 'Reds Turn')

        #AI Player Inputs:
            # else: #Everything here is the same as the if statement otherthan a couple minor changes.
            print(self)
            select_token = AI.nextMove(self)#I am making the token equal to the best spot given by nextMove.
            if self.allowsMove(select_token):
                self.addMove(select_token, self.aiplayer)
                y = self.changeColour(self.colors, select_token)
                self.draw.create_oval((self.diameter+2)*(select_token), (self.diameter+2)*y, (self.diameter+2)*(select_token+1), (self.diameter+2)*(y+1), fill = 'red')
                self.draw.itemconfig(self.circles[row][col], fill=newColour)
                self.colors[y][select_token] = 'blue'
                # if timer == 1:
                #     self.label.config(text='Yellows Turn')
                print(self)

                if self.winsFor('O'): #If the computer wins then it will print
                    print(self)
                    self.done = True
                    self.label.config(text = 'Computer Wins!')
                    print('Computer Wins!')
                    flag = False
                    return
                turn_count = 0

            if turn_count == 0:
                self.label.config(text = 'Yellows Turn')

            if self.isFull(): #If the whole board becomes full then it's a tie
                print(self)
                self.done = True
                self.label.config(text = "It's a tie!")
                print('It is a tie!')
                return

            if not self.allowsMove(select_token): ##If the column is full, it is illegal
                print('Illegal Move, pick something else.')



    def playGameWith(self, aiplayer):
        print(self.col_select)
        #board = Connect4(7,6, frame) #Just to reference later. #This will indicate if the game is over, (False = Not over, True = Is Over).
        turn_count = 0 #This will keep track of how many turns are played
        while not self.winsFor('X') or \
        self.winsFor('O'): #Keep playing the game while game_state is False.

        #Player 1 Inputs:
            if turn_count == 0: #If the turn count is 0, then player 1 will go, otherwise, that means it's player 2's turn.
                print(board)
                select_token = int(input('Player 1, pick 0 - 6:')) #Setting this to call later. This must be an int.
                if self.allowsMove(select_token): #If the desired move passes the allowsMove function, then continue... otherwise, line 178.
                    self.addMove(select_token, 'X') #See here, I'm adding a move to the board I created in my hostGame and the actual board.
                    #board.addMove(select_token, 'X') #Prints the board after your move has been placed.
                    if self.winsFor('X'): #This will check for a win, and if you do win, it tells you that player 1 wins, then stops the function.
                        print(self)
                        print('Player 1 Wins')
                        break
                    turn_count +=1 #Adds one to the turn count so that the function knows to switch to player 2, since it's != to 0.

                if self.isFull(): #All this does is check if the board is full, if so, show the board again and say it's a tie.
                    print(board)
                    print('It is a tie!')
                    break
                if not board.allowsMove(select_token):
                    print('Illegal Move, pick something else.')

        #AI Player Inputs:

            else: #Everything here is the same as the if statement otherthan a couple minor changes.
                print(board)
                select_token = aiplayer.nextMove(board)#I am making the token equal to the best spot given by nextMove.
                if self.allowsMove(select_token):
                    self.addMove(select_token, self.aiplayer)
                    board.addMove(select_token, self.aiplayer)

                    if self.winsFor(self.aiplayer): #If the computer wins then it will print
                        print(board)
                        print('Computer Wins!')
                        break
                    turn_count = 0

                if self.isFull(): #If the whole board becomes full then it's a tie
                    print(board)
                    print('It is a tie!')
                    break

                if not board.allowsMove(select_token): ##If the column is full, it is illegal
                    print('Illegal Move, pick something else.')


    """
    This is my Player class. This is what defines what the computer will choose based on the board and future boards.
    My init function just initializes the class with definitions. Scores for will be the function that gives a score for each
    column depending on its chances of winning. The tieBreaker funciton is used to pick from Left side, Right side or a random
    column in case there is multiple columns with the same score. The final nextMove function will actually choose the column with
    the maximum score (depending on the tieBreaker function).
    """

class Player:
    def __init__(self, ox, tbt, ply):
        self.ox = ox
        self.ply = ply
        self.tbt = tbt

    """
    The scoreFor takes the ply number and does something depending on that number.
    If the ply is 0, basically the computer will just pick a random available column.
    Ply 0 just looks at the current board and not any future moves. If it's a ply greater
    than 0, then it will add a move if its allowed, then check if it is a winning move; if so,
    score that column a 100. If it doesn't give a 100, then just give it a 50.
    """

    def scoreFor(self, board, ox, ply):
        """
        This part is making it so I can
        flip between X and O while I recurse through
        my function during plys other than 0.
        """
        if ox == 'X': #If I start as X, recurse with O then X.
            oponent = 'O'
        else:
            oponent = 'X' #Otherwise recruse with X then O.

        scores = [] #Represents a score for each column
        if ply == 0:
            for col in range(board.width): #Itterates through each column.
                if board.allowsMove(col) == False: #If the moove isn't allowed (full column)
                    scores.append(-1) #Then add a -1
                else:
                    scores.append(50) ##Otherwise make it 50. Because it's ply 0, basically only 50's and -1's can be a thing.

        else:
            for col in range(board.width): #Itterates through each column.
                if board.allowsMove(col):
                    board.addMove(col, ox)
                    if board.winsFor(ox):
                        scores.append(100) #If it;s a winning move, then score the column a 100.
                    elif ply > 1: #Any other ply greater than 1
                        scores.append((100 - max(self.scoreFor(board, oponent, ply-1))))
                    else:
                        scores.append(50)
                    board.delMove(col) #Removing the move made because it was just a test, I will add the move in nextMove.
                else:
                    scores.append(-1) #If none of those are valid, return -1 to my scores, so basically if the column is full.
        return scores #Return my scores list.

    """
    All tieBreaker simply does is, take the list from scores and if it's left, choose the first
    value, if right, choose the last value (-1), if random, just choose a value inside it.
    """
    def tieBreaker(self, i):
        if self.tbt == 'Left':
            return i[0] #Left most maximum value.

        elif self.tbt == 'Right':
            return i[-1] #Right most maximum value.
        else:
            return random.choice(i) #Just choose any value from the maximum values.

    """
    next move will choose the maximum value (in accordance to tieBreaker) and
    return the value(s) in a list.
    """
    def nextMove(self, board):
        validLocation = self.scoreFor(board, self.ox, self.ply) #validLocation takes on the values that scoreFor returns.
        big = max(validLocation) #big will take on the value that is the max value of validLocation.
        scoreList = [] #Creating an empy list
        for i in range(board.width): #i will take on the values of the width of the board. So all the columns
                if validLocation[i] == max(validLocation):
                    scoreList.append(i) #Add the maximum value that is given from validLocation[i]
                else:
                    continue #Continue doing this for loop until the maximum value is found.
        #print(scoreList)
        return self.tieBreaker(scoreList) #Returns the value into the list, but through the tieBreak function.




def main():
    frame = Tk()
    frame.title('Connect 4')
    myScreen = Connect4(7, 6, frame)
    #print(self.circles)
    #print(myScreen)
    #myScreen.playGameWith(AI)
    frame.mainloop()
    # frame.mainloop()
    #myScreen.draw_board(myScreen)
    #frame.bind('<Button-1>', myScreen.playGameWith)
    # myScreen.addMove(0, 'O')
    # myScreen.addMove(0, 'X')
    # myScreen.addMove(0, 'X')
    # myScreen.addMove(0, 'X')
    # myScreen.addMove(0, 'X')
    # myScreen.addMove(0, 'O')
    # myScreen.addMove(1, 'O')
    # myScreen.addMove(1, 'X')
    # myScreen.addMove(1, 'O')
    # myScreen.addMove(1, 'O')
    # myScreen.addMove(2, 'O')
    # myScreen.addMove(2, 'X')
    # myScreen.addMove(2, 'O')
    # myScreen.addMove(6, 'X')
    # myScreen.addMove(6, 'X')
    # myScreen.addMove(6, 'X')
    # print(myScreen)
    # AI = Player('O', 'Left', 7) #'Left', 'Right', 'Random'
    # print(AI.scoreFor(board, 'O', 3))
    # print(AI.nextMove(board))
    # print(AI.tieBreaker([1,2,3,4,5]))
    #board.playGameWith(AI)


if __name__ == '__main__':
    main()
