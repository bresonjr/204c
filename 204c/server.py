import socket
from threading import Thread
import random

SERVER = None
PORT = 8000
IP_ADDRESS = '127.0.0.1'
clients = {}


def broadcast(message):
    for client in clients:
        client.send(message.encode())


def client_thread(client):
    client.send('name'.encode())
    name = client.recv(2048).decode()
    clients[client] = name
    print(f"Player {name} connected.")

    while True:
        try:
            message = client.recv(2048).decode()
            if message:
                print(f"Broadcasting number: {message}")
                broadcast(message)
            else:
                remove(client)
        except:
            continue


def remove(client):
    if client in clients:
        name = clients[client]
        broadcast(f"Player {name} left the game.")
        print(f"Player {name} left the game.")
        del clients[client]


def start_game():
    global SERVER
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("Server started!")

    while True:
        client, address = SERVER.accept()
        print(f"Connected with {str(address)}")

        client.send("name".encode())

        Thread(target=client_thread, args=(client,)).start()


start_game()
