import socket
import json
import threading
import time
import os
import signal
from cryptography.fernet import Fernet

key = os.getenv('FERNET_K')
fernet = Fernet(key)


def connect(ip, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ip, port))
    print("[+] Connected to " + ip)
    return connection


def listen(ip, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((ip, port))
    listener.listen(0)
    print("[+] Waiting for incoming connections")
    connection, address = listener.accept()
    print("[+] Got a connection from" + str(address))
    return connection


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, connection, ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.connection = connection
        self.ip = ip

    def run(self):
        if self.name == 'receive':
            receive = Receiver(self.connection, self.ip, self.counter)
            receive.run()

        elif self.name == 'send':
            send = Sender(self.connection, self.ip, self.counter)
            send.run()


class Receiver:

    def __init__(self, connection, ip, delay):
        self.connection = connection
        self.ip = ip
        self.delay = delay

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(2048).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def receive_message(self, command):
        decMessage = fernet.decrypt(command.encode())
        print(f"\r\n> receive from {self.ip} >> " + decMessage.decode() + '\t', end='')

    def run(self):
        while True:
            time.sleep(self.delay)
            command = self.reliable_receive()
            if command == 'exit':
                print("\n>> Exiting")
                self.connection.close()
                os.kill(os.getpid(), signal.SIGINT)

            else:
                self.receive_message(command)


class Sender:
    def __init__(self, connection, ip, delay):
        self.connection = connection
        self.ip = ip
        self.delay = delay

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def send_messages(self):
        command = input(f"> send to {self.ip} >> ")
        if command == '--help':
            print('[+] Commands: \n'
                  '\t exit - exit the session - to use type exit')
        elif command == 'exit':
            self.reliable_send(command)
            print("\n>> Exiting")
            os.kill(os.getpid(), signal.SIGINT)

        else:
            encMessage = fernet.encrypt(command.encode())
            self.reliable_send(encMessage.decode())

    def run(self):
        while True:
            time.sleep(self.delay)
            self.send_messages()


running = True
while running:
    run = input("Do you want listen to incoming connections (Type 'l') or do you want to connect (Type 'c'): ").lower()
    # ip = input("Enter ip: ")
    # port = input("Enter port: ")
    ip = '192.168.8.121'
    port = 4444
    if run == 'l':
        connects = listen(ip, port)
        running = False
    elif run == 'c':
        connects = connect(ip, port)
        running = False

    else:
        print("[-] Wrong input !!!")
receiver = myThread(1, "receive", 0.1, connects, ip)
sender = myThread(2, "send", 0.2, connects, ip)
receiver.start()
sender.start()
# receiver.join()
# sender.join()
