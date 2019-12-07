import socket
import select
import time
import sys

IP = 'localhost'
PORT = 8218
username = input("Enter your username: ")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((IP, PORT))
server_socket.setblocking(0)

socket_list = [server_socket]

server_socket.send(bytes(username, 'utf8'))
error1 = None
while not error1:
    try:
        while not error1:
            error1 = server_socket.recv(1024).decode('utf-8')
            print('1',error1)
    except IOError as e:
        pass
    if error1 == 'error1':
        username = input("Enter other username: ")
        server_socket.send(bytes(username, 'utf8'))
        error1 = None

else:
    audience = input("Enter audience username: ")
    server_socket.send(bytes(audience, 'utf-8'))
    error2 = None
    while not error2:
        try:
            while not error2:
                error2 = server_socket.recv(1024).decode('utf-8')
        except IOError as e:
            pass
        if error2 == 'error2':
            audience = input('{} is offline enter other audience username: '.format(audience))
            server_socket.send(bytes(audience, 'utf-8'))
            error2 = None

while True:
    read_socket, write_socket, excepted_socket = select.select(socket_list, socket_list, socket_list)
    if read_socket:
        for s in read_socket:
            print(s.recv(1024).decode('utf-8'))
    if write_socket:
        for s in write_socket:
            message = input('->')
            s.send(bytes(message, 'utf-8'))
    else:
        for s in excepted_socket:
            socket_list.remove(s)
            print("Connection Closed!")

#    time.sleep(5)
