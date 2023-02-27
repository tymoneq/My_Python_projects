import socket
import json
import threading
import sys
import time
import os
import signal


def connect(ip, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ip, port))
    print("[+] Connected to " + ip)
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
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def receive_message(self, command):
        message = ""
        for mess in command:
            message += mess + " "

        print(f"\n> receive from {self.ip} >> " + message, end='')
        # sys.stdout.flush()

    def run(self):
        while True:
            time.sleep(self.delay)
            command = self.reliable_receive()
            if command[0] == 'exit':
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
        command = command.split(' ')
        if command[0] == '--help':
            print('[+] Commands: \n'
                  '\t exit - exit the session - to use type exit')
        elif command[0] == 'exit':
            self.reliable_send(command)
            print("\n>> Exiting")

            os.kill(os.getpid(), signal.SIGINT)

        else:
            self.reliable_send(command)

    def run(self):
        while True:
            time.sleep(self.delay)
            self.send_messages()


ip = '192.168.8.121'
connects = connect(ip, 4444)
receiver = myThread(1, "receive", 0.1, connects, ip)
sender = myThread(2, "send", 0.2, connects, ip)
receiver.start()
sender.start()
receiver.join()
sender.join()
