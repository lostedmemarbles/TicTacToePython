from tkinter import *
from tkinter import ttk
from tkinter import Tk
from PIL import ImageTk, Image

x = 'X.png'
o = 'O.png'
playerXO = x
botXO = o
currentXO = x
yourTurn = True
spotNames = ['leftTop', 'top', 'rightTop', 'left', 'center', 'right', 'leftBottom', 'bottom', 'rightBottom']
board = None
turnLabel = None
turnLabelValue = None 
boardFrame = None
choiceFrame = None
window = None
newGameButton = None
wins = []
numOfWins = 0
winLabelValue = 'Wins: '
numOfLosses = 0
lossLabelValue = 'Losses: '
colors = {'lightpink': '#ffccf5', 'darkgray': '#696969', 'midpink': '#ffb0ef', 'white': '#ffffff', 'red': '#ff0000', 'darkred': "#7A1010"}

class Win:
    def __init__(this, winName, spots):
        this.winName = winName
        this.spots = spots
        this.possibleForX = True
        this.possibleForO = True
        
class Spot:
    def __init__(this, window, spotName, i , j, h):
        this.spotName = spotName
        this.currentXO = None
        this.frame = ttk.Frame(window, name=spotName, style='pink.TFrame')
        this.frame.grid(column=j, row=i, sticky="nsew")
        this.frame.configure(width=h, height=h, padding=5)
        this.frame.bind('<Button-1>', addXO)

class Board:
    def __init__(this, window, w, h):
        global colors
        this.XOs = {}
        this.spots = {}
        i = 0
        j = -1
        for spotName in spotNames:
            if j <= 1:
                j = j + 1
            else:
                j = 0
                i = i + 1
            #print('{}, {}'.format(i, j))
            this.XOs[spotName] = None
            this.spots[spotName] = Spot(window, spotName, i, j, h)
    def reset(this):
        for spotName in spotNames:
            if this.spots[spotName]:
                babies = this.spots[spotName].frame.winfo_children()
                for baby in babies:
                    baby.destroy()
                this.spots[spotName].frame.destroy()
                this.spots[spotName].frame = None
                this.spots[spotName].currentXO = None

def getXOValue(xoVal):
    print('getXOValue')
    if xoVal == x:
        return 'x'
    return 'o'

def switchTurns():
    global currentXO, yourTurn, turnLabelValue
    print('switchTurns, yourTurn: ', yourTurn)
    if yourTurn:
        currentXO = botXO
        turnLabelValue.set("Bot's turn")
        yourTurn = False
    else:
        currentXO = playerXO
        turnLabelValue.set("Your turn")
        yourTurn = True
    
def updateWins(spotName):
    global currentXO, wins
    print('spotName', spotName)
    for win in wins:
        if spotName in win.spots:
            if currentXO == o:
                win.possibleForX = False
            else:
                win.possibleForO = False
                
def addXO(event):
    global currentXO, colors
    print('addXO')
    spot = event.widget.winfo_name()
    print(event.widget.winfo_name())
    print(board.spots)
    if not board.spots[spot].currentXO:
        canv = Canvas(board.spots[spot].frame, height=147, width=147, bg=colors['lightpink'], borderwidth=0)
        canv.grid(column=0, row=0, sticky='news', padx=0, pady=0)
        image = Image.open(currentXO)
        board.spots[spot].currentXO = currentXO
        canv.image = ImageTk.PhotoImage(image.resize((141, 141)))
        canv.create_image(0, 0, image=canv.image, anchor='nw')
    updateWins(spot)
    switchTurns()
    gameOver = isGameOver()
    match(gameOver):
        case True:
            print('Board is full')
            endGame(None)
        case False:
            print('Game is not over')
        case _:
            if gameOver == o:
                print('O wins')
                endGame(o)
            if gameOver == x:
                print('X wins')
                endGame(x)
        
def chooseX(this):
    global turnLabelValue, playerXO, botXO
    print('chooseX')
    playerXO = x
    botXO = o
    turnLabelValue.set('X goes first!')
    newGameBoard()
def chooseO(this):
    global turnLabelValue, playerXO, botXO
    print('chooseO')
    playerXO = o
    botXO = x
    turnLabelValue.set('X goes first!')
    newGameBoard()

##Add win/lose/tie popup


def isBoardFull():
    global board
    print('isBoardFull')
    for spotName in board.spots.keys():
        #print('spotName, currentXO:', spotName, board.spots[spotName].currentXO)
        if not board.spots[spotName].currentXO:
            return False
    return True
    

def isGameOver():
    global wins, board, x, o
    #{vertLeft, vertMiddle, vertRight, horizTop, horizMiddle, horizBottom, diagTopLeft, diagTopRight}
    if isBoardFull():
        return True
    for win in wins:
        if win.possibleForO:
            matches = 0
            for spotName in win.spots:
                #print('spotName, o', spotName, board.spots[spotName].currentXO)
                if board.spots[spotName].currentXO == o:
                    matches += 1
                    if matches == 3:
                        return o
        if win.possibleForX:
            matches = 0
            for spotName in win.spots:
                if board.spots[spotName].currentXO == x:
                    matches += 1
                    if matches == 3:
                        return x
    return False

def newGame():
    global choiceFrame
    print('newGame')
    if choiceFrame:
        choiceFrame.destroy()
        choiceFrame = None
    resetGameBoard()
    createXOFrame()

def createXOFrame():
    global boardFrame, choiceFrame, colors, newGameButton
    newGameButton.configure(state='disabled')
    print('boardFrame.grid_propagate(False)')
    boardFrame.grid_propagate(False)
    choiceFrame = ttk.Frame(boardFrame, padding=10, width=300, height=200, style='outer.TFrame')
    choiceFrame.grid(column=0, row=0, sticky='news', padx=90, pady=150)
    choiceFrame.focus_set()
    questionLabel = ttk.Label(choiceFrame, style='white.TLabel', text='Choose your icon:')
    questionLabel.grid(column=0,row=0)
    optionsFrame = ttk.Frame(choiceFrame, borderwidth=0, style='within.TFrame')
    optionsFrame.grid(column=0, row=1, pady=10, padx=10)
    optionXCanvas = Canvas(optionsFrame, bg=colors['darkgray'], borderwidth=0, height=130, width=130)
    optionOCanvas = Canvas(optionsFrame, bg=colors['darkgray'], borderwidth=0, height=130, width=130)
    xImage = Image.open(x)
    oImage = Image.open(o)
    optionXCanvas.image = ImageTk.PhotoImage(xImage.resize((130, 130)))
    optionOCanvas.image = ImageTk.PhotoImage(oImage.resize((130, 130)))
    optionXCanvas.create_image(0,0, image=optionXCanvas.image, anchor='nw')
    optionOCanvas.create_image(0,0, image=optionOCanvas.image, anchor='nw')
    optionXCanvas.grid(column=0, row=0, pady=10, padx=10)
    optionOCanvas.grid(column=1, row=0, pady=10, padx=10)
    optionXCanvas.bind('<Button-1>', chooseX)
    optionOCanvas.bind('<Button-1>', chooseO)

def createEndGameFrame(winner):
    global boardFrame, choiceFrame, colors, newGameButton
    newGameButton.configure(state='disabled')
    #print('boardFrame.grid_propagate(False)')
    boardFrame.grid_propagate(False)
    #boardFrame.update_idletasks()
    choiceFrame = ttk.Frame(boardFrame, padding=10, width=300, height=200, style='outer.TFrame')
    choiceFrame.grid(column=0, row=0, sticky='news', padx=126, pady=190)
    choiceFrame.focus_set()
    gameOverText = 'It\'s a Tie!'
    if winner == playerXO:
        gameOverText = 'You Win!'
    elif winner == botXO:
        gameOverText = 'You Lose!'
    questionLabel = ttk.Label(choiceFrame, style='white.TLabel', text=gameOverText)
    questionLabel.grid(column=0,row=0)
    optionsFrame = ttk.Frame(choiceFrame, borderwidth=0, style='within.TFrame')
    optionsFrame.grid(column=0, row=1, pady=10, padx=10)
    closeButton = ttk.Button(optionsFrame, text='Close', command=window.destroy)
    closeButton.grid(column=1,row=0,pady=10,padx=10)
    playAgainButton = ttk.Button(optionsFrame, text='Play Again', command=newGame)
    playAgainButton.grid(column=0,row=0,pady=10,padx=10)
    #choiceFrame.update_idletasks()
    #252 - mid
    #116 - midendgame
    #136
    #print('choiceFrame size:', choiceFrame.winfo_width(), choiceFrame.winfo_height())
    #print('boardFrame size:', boardFrame.winfo_width(), boardFrame.winfo_height())

def initWins():
    global wins
    allWins = {'vertLeft': ['leftTop', 'left', 'leftBottom'], 'vertMiddle': ['top', 'center', 'bottom'], 'vertRight': ['rightTop', 'right', 'rightBottom'], 'horizTop': ['leftTop', 'top', 'rightTop'], 'horizMiddle': ['left', 'center', 'right'], 'horizBottom': ['leftBottom', 'bottom', 'rightBottom'], 'diagTopLeft': ['leftTop', 'center', 'rightBottom'], 'diagTopRight': ['rightTop', 'center', 'leftBottom']}
    for winName in allWins.keys():
        print(winName)
        wins.append(Win(winName, allWins[winName]))
    
def newGameBoard():
    print('newGameBoard')
    global boardFrame, board, newGameButton
    newGameButton.configure(state='enabled')
    if not board:
        choiceFrame.destroy()
        boardFrame.grid_propagate(True)
        #print('boardFrame.grid_propagate(True)')
        board = Board(boardFrame, 161, 161)
        initWins()
    else:
        resetGameBoard()
        
def resetGameBoard():
    global board, turnLabelValue, wins, currentXO
    currentXO = x
    if turnLabelValue:
        turnLabelValue.set('               ')
    if board:
        board.reset()
        board = None
    if len(wins) > 0:
        wins = []

def endGame(winner):
    global playerXO, numOfLosses, numOfWins, winLabelValue, lossLabelValue
    if winner == playerXO:
        numOfWins += 1
        winLabelValue.set('Wins: '+str(numOfWins))
    elif winner == botXO:
        numOfLosses += 1
        lossLabelValue.set('Losses: '+str(numOfLosses))

        
    #newGame()
    resetGameBoard()
    createEndGameFrame(winner)

def setupWindow():
    global window, colors
    window = Tk()
    window['bg']=colors['midpink']
    window.title('Tic-Tac-Toe')
    window.geometry("500x500")
    window.resizable(False, False)
    window.update_idletasks()

def setupStyles():
    global colors
    style = ttk.Style()
    style.configure('white.TLabel', foreground=colors['white'], background=colors['darkgray'])
    style.configure('outer.TFrame', background=colors['darkgray'], relief='groove', bordercolor=colors['darkgray'], borderwidth=20)
    style.configure('red.TFrame', background=colors['red'], relief='ridge', bordercolor=colors['darkred'], borderwidth=10)
    style.configure('within.TFrame', background=colors['darkgray'], relief='flat', bordercolor=colors['darkgray'], borderwidth=0)
    style.configure('pink.TFrame', background=colors['lightpink'], borderwidth=20, bordercolor=colors['darkgray'], relief='sunken')
    #print('STYLE CONFIG',ttk.Style().layout('TButton'))

def setupBoardFrame(windWidth, windHeight):
    global boardFrame, window
    boardFrame = ttk.Frame(window, padding=10, width=windWidth, height=windHeight, style='outer.TFrame')
    boardFrame.grid(sticky="nsew", row=0, column=0)

def setupBottomFrame(windWidth):
    global turnLabelValue, colors, winLabelValue, lossLabelValue, newGameButton
    bottomFrame = ttk.Frame(window, padding=10, width=windWidth, height=100, style='outer.TFrame')
    bottomFrame.grid(sticky="nsew", row=1, column=0)
    newGameButton = ttk.Button(bottomFrame, text='New Game', command=newGame)
    newGameButton.grid(column=0, row=0, padx=10, pady=3)
    turnLabelValue = StringVar(value='   ')
    winLabelValue = StringVar(value='Wins: '+str(numOfWins))
    lossLabelValue = StringVar(value='Losses: '+str(numOfLosses))
    turnLabel = ttk.Label(bottomFrame, textvariable=turnLabelValue, background=colors['darkgray'], style='white.TLabel')
    turnLabel.grid(column=0, row=1, padx=10, pady=3)
    wLabel = ttk.Label(bottomFrame, textvariable=winLabelValue, style='white.TLabel')
    wLabel.grid(column=3, row=2, padx=10, pady=3)
    lLabel = ttk.Label(bottomFrame, textvariable=lossLabelValue, style='white.TLabel')
    lLabel.grid(column=3, row=1, padx=10, pady=3)

def beginning():
    print('beginning')
    global boardFrame, turnLabelValue, window
    setupWindow()
    windWidth = window.winfo_width()
    windHeight = window.winfo_height()
    #print('{} x {}'.format(windWidth, windHeight))
    setupStyles()
    setupBoardFrame(windWidth, windHeight)
    setupBottomFrame(windWidth)
    newGame()
    window.geometry("507x609")
    #print(newGameButton.configure().keys())


beginning()
window.mainloop()