import tkinter as tk
import socket
import select
import time
import sys

IP = '192.168.1.53'
PORT = 8220
username = input("Enter your username: ")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((IP, PORT))
server_socket.setblocking(1)

socket_list = [server_socket]





server_socket.send(bytes(username, 'utf8'))
error1 = None
while not error1:
    try:
        while not error1:
            error1 = server_socket.recv(1024).decode('utf-8')
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
        if error2 == 'wait':
            print('please wait')

while True:
    read_socket, write_socket, excepted_socket = select.select(socket_list, socket_list, socket_list)
    print(read_socket)
    for s in read_socket:
        msg = s.recv(1024)
        if msg:
            print(msg.decode('utf-8'))
        if not msg:
            socket_list.remove(s)
            print("Connection Closed!")

    for s in write_socket:
        message = input('->')
        s.send(bytes(message, 'utf-8'))

#    time.sleep(5)
