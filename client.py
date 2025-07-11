import threading
import socket
import argparse
import os
import sys
import tkinter as tk

class Send(threading.Thread):

    #listens for user input from command line

    #sock the connected sock object
    #name(str) : The user provided by the user

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        # Listen for user input from the command line and send it to the server
        # Typing "Quit" will close the connection and exit the app

        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # if we type "QUIT" we leave the chatroom

            if message == "QUIT":
                self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
                break

            # send message to server for broadcasting

            else:
                self.sock.sendall('{}: {} '.format(self.name, message).encode('ascii'))
        
        print('\nQuitting...')
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):

    # Listens to incoming messages from the server

    def __init__(self, sock, name):
        
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
         
         # Receiving data from the server and displays it in the gui

        while True:
            message = self.sock.recv(1024).decode('ascii')

            if message:

                if self.messages:
                    self.messages.insert(tk.END, message)
                    print('hi')
                    print('\r{}\n{}: '.format(message, self.name), end='')

                else:
                    print('\r{}\n{}: '.format(message, self.name), end='')

            else:
                print('\n No. We have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

class Client:

    # Management of the client server connection and integration of GUI

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.message = None
        

    def start(self):

        print('Trying to connect to {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Succesfully connected to {}:{}'.format(self.host, self.port))
        print()
        self.name = input('Your name: ')
        print()
        print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

        # Create send and message threads

        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        #Start send and receive thread

        send.start()
        receive.start()

        self.sock.sendall('Server: {} has joined the chat. say whatsup!'.format(self.name).encode('ascii'))
        print("\rReady! Leave the chatroom anytime by typing 'QUIT'\n")
        print('{}: '.format(self.name),end='')

        return receive
    
    def send(self, textInput):
        #Send textinput data from the GUI
        message = textInput.get()
        textInput.delete(0, tk.END)
        if self.messages:
            self.messages.insert(tk.END, '{}: {}'.format(self.name, message))
        # Type "QUIT" to leave the chatroom
        if message == "QUIT":
            self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('ascii'))
            print('\nQuitting...')
            self.sock.close()
            os._exit(0)

        #SEND message to the server for broadcasting
        else:
            self.sock.sendall('{}: {}'.format(self.name, message).encode('ascii'))
    

def main(host, port):
    #initialize and run the GUI application

    client = Client(host, port)
    receive = client.start()

    window = tk.Tk()
    window.title("Chatroom")

    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    messages = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    client.messages = messages
    receive.messages = messages

    fromMessage.grid(row=0, column=0, columnspan=2, sticky="nsew")
    fromEntry = tk.Frame(master=window)
    textInput = tk.Entry(master=fromEntry)

    textInput.pack(fill=tk.BOTH, expand=True)
    textInput.bind("<Return>", lambda event: client.send(textInput))
    textInput.insert(0, "Write your message here.")

    btnSend = tk.Button(
        master=window,
        text='Send', 
        command=lambda: client.send(textInput)
    )
    fromEntry.grid(row=1, column=0, padx=10, sticky="ew")
    btnSend.grid(row=1, column=1, padx=10, sticky="ew")

    window.rowconfigure(0, minsize=500, weight=1)
    window.rowconfigure(1, minsize=50, weight=0)
    window.columnconfigure(0, minsize=500, weight=1)
    window.columnconfigure(1, minsize=200, weight=0)

    window.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument('host', nargs='?', default='127.0.0.1', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port(default 1060)')

    args = parser.parse_args()

    main(args.host, args.p)