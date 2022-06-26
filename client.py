"""python program to implement chat application!

This file code is  specific in implementation of client side of chat application """

import socket
import select
import sys


"""First initializing the socket connection with corresponding address domain(family)[Internet Domain in this scenario]
 as first argument and the type of data flow(In this case continuous/stream flow) as second argument"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# IP_address = "127.0.0.1"
# Port = 5002 # server's port
server.connect((IP_address, Port))


def send_message():
    while True:

        """ List of possible inputs"""
        sockets_list = [sys.stdin, server]

        """ Evaluating the two possible conditions if the connection soclet client is the same as server 
        then print the message else, select returns the sockets_list which is reader for input, Based on the read socket if and else are executed
        If the server wants to send the message then it evaluates to if condition , 
        if the user/client wants to send then it would go with the else condition"""
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                print (message)
            else:
                message = sys.stdin.readline()
                server.send(message)
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
    server.close()


send_message()