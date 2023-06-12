import socket
from tkinter import *
import tkinter as tk
from threading import Thread
import random
from PIL import ImageTk, Image

import platform

screen_width = None
screen_height = None

SERVER = None
PORT = 8000
IP_ADDRESS = '127.0.0.1'
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

ticketGrid = []
currentNumberList = []
flashNumberList = []
flashNumberLabel = None


def createTicket():
    global gameWindow
    global ticketGrid
    # Ticket Frame
    mianLable = Label(
        gameWindow,
        width=65,
        height=16,
        relief='ridge',
        borderwidth=5,
        bg='white'
    )
    mianLable.place(x=95, y=119)

    xPos = 105
    yPos = 130
    for row in range(0, 3):
        rowList = []
        for col in range(0, 9):
            if platform.system() == 'Darwin':
                # For Mac users
                boxButton = Button(
                    gameWindow,
                    font=("Chalkboard SE", 18),
                    borderwidth=3,
                    pady=23,
                    padx=-22,
                    bg="#fff176",  # Initial Yellow color
                    highlightbackground='#fff176',
                    activebackground='#c5e1a5'  # onPress Green Color
                )
                boxButton.place(x=xPos, y=yPos)
            else:
                # For windows users
                boxButton = tk.Button(
                    gameWindow,
                    font=("Chalkboard SE", 30),
                    width=3,
                    height=2,
                    borderwidth=5,
                    bg="#fff176"
                )
                boxButton.place(x=xPos, y=yPos)

            rowList.append(boxButton)
            xPos += 64
        # Creating nested array
        ticketGrid.append(rowList)
        xPos = 105
        yPos += 82


def placeNumbers():
    global ticketGrid
    global currentNumberList

    # Number Container Dictionary
    numberContainer = {
        0: [1, 10, 19, 28, 37, 46, 55, 64, 73],
        1: [2, 11, 20, 29, 38, 47, 56, 65, 74],
        2: [3, 12, 21, 30, 39, 48, 57, 66, 75],
        3: [4, 13, 22, 31, 40, 49, 58, 67, 76],
        4: [5, 14, 23, 32, 41, 50, 59, 68, 77],
        5: [6, 15, 24, 33, 42, 51, 60, 69, 78],
        6: [7, 16, 25, 34, 43, 52, 61, 70, 79],
        7: [8, 17, 26, 35, 44, 53, 62, 71, 80],
        8: [9, 18, 27, 36, 45, 54, 63, 72, 81]
    }

    for row in range(0, 3):
        randomColList = []
        counter = 0
        # Getting random 5 cols
        while counter <= 4:
            randomCol = random.randint(0, 8)
            if randomCol not in randomColList:
                randomColList.append(randomCol)
                counter += 1

        for col in randomColList:
            series = numberContainer[col]
            randomNum = random.choice(series)
            currentNumberList.append(randomNum)

        currentNumberList.sort()

        # Print the random numbers for testing
        print(currentNumberList)


def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winingMessage
    global resetButton
    global flashNumberLabel

    gameWindow = Tk()
    gameWindow.title("Tambola Family Fun")
    gameWindow.geometry('800x600')

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="./assets/background.png")

    canvas2 = Canvas(gameWindow, width=500, height=500)
    canvas2.pack(fill="both", expand=True)

    # Display image
    canvas2.create_image(0, 0, image=bg, anchor="nw")

    # Add Text
    canvas2.create_text(
        screen_width / 4.5,
        50,
        text="Tambola Family Fun",
        font=("Chalkboard SE", 50),
        fill="#3e2723"
    )

    createTicket()
    placeNumbers()

    # Flash Number Label
    flashNumberLabel = canvas2.create_text(
        400,
        screen_height / 2.3,
        text="Waiting for other players to join...",
        font=("Chalkboard SE", 30),
        fill="#3e2723"
    )

    gameWindow.resizable(True, True)
    gameWindow.mainloop()


def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()


def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.geometry('800x600')

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="./assets/background.png")

    canvas1 = Canvas(nameWindow, width=500, height=500)
    canvas1.pack(fill="both", expand=True)
    # Display image
    canvas1.create_image(0, 0, image=bg, anchor="nw")
    canvas1.create_text(
        screen_width / 4.5,
        screen_height / 8,
        text="Enter Name",
        font=("Chalkboard SE", 60),
        fill="#3e2723"
    )

    nameEntry = Entry(
        nameWindow,
        width=15,
        justify='center',
        font=('Chalkboard SE', 30),
        bd=5,
        bg='white'
    )
    nameEntry.place(x=screen_width / 7, y=screen_height / 5.5)

    button = tk.Button(
        nameWindow,
        text="Save",
        font=("Chalkboard SE", 30),
        width=11,
        command=saveName,
        height=2,
        bg="red",
        activebackground='#0052cc',
        bd=5,
        relief='ridge'
    )
    button.place(x=screen_width / 4.8, y=screen_height / 3.5)

    nameWindow.mainloop()


def receive():
    while True:
        try:
            message = SERVER.recv(2048).decode()
            if message == 'name':
                askPlayerName()
            else:
                # Display the received message in the flashNumberLabel
                canvas2.itemconfig(flashNumberLabel, text=message)
        except:
            print("An error occurred!")
            SERVER.close()
            break


def startGame():
    global SERVER

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=receive)
    thread.start()


startGame()
