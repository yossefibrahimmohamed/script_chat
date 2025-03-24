import socket
import pygame
import sys

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.8', 5555))
    answer = input("Enter you need ringtones / message : ")

    if (answer=="message"):

        while True:
            # Get user input
            message = input("Enter message: ")

            # Send the message to the server
            client.send(message.encode('utf-8'))

            # Receive and print the response
            response = client.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")

    elif (answer == "ringtones"):

        while True:

            get_steady = input("Enter 'beb' : ")

            if (get_steady=='beb'):

                pygame.init()  # Initialize pygame

                sound = pygame.mixer.Sound('beep-warning-6387.mp3')

                sound.play()

                while pygame.mixer.get_busy():

                    pygame.time.Clock().tick(10)


if __name__ == "__main__":
    start_client()