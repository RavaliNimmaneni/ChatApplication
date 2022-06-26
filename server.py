"""python program to implement chat application!

This file code is  specific in implementation of server side of chat application """

import socket
import sys

from thread import *

""" IP address and port values"""
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

# IP_address = "0.0.0.0"
# Port = 5002 # port we want to use


"""First initializing the socket connection with corresponding address domain(family)[Internet Domain in this scenario]
 as first argument and the type of data flow(In this case continuous/stream flow) as second argument"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""set the protocol levels of the socket and re-use the local address specified"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""binding the socket object server to the above specified IP_address host and port,
These arguments has to be known even to the client side of the application"""
server.bind((IP_address, Port))

"""list of active users(clients)"""
users_list = []


def handle_client(conn_soc, addr):
    """ This function handles each client(user) that establishes connection and broadcasts the message or
    removes the user if the message is not received"""
    print("[New connection],{}".format(addr))
    connected = True
    while connected:
        try:
            """keep listening the messages from the connection socket , 2048 - specifies the bytes 
            (of the message received)"""
            message = conn_soc.recv(2048)
            if message:

                """prints the message and address of the
                user who just sent the message on the server
                terminal"""
                print ("<" + addr[0] + "> " + message)

                # Calls broadcast function to send message to all other users
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, conn_soc)

            else:
                """message may have no content if the connection
                is broken, in this case we remove the connection"""
                remove(conn_soc)
        except:
            """This can be handled easy here or if there is an exception the active connection can be removed from 
            the active user list"""
            continue


"""Below function sends the message to all the other active clients except the connection object 
from the one it is received """


def broadcast(message, connection):
    for clients in users_list:
        if clients != connection:
            try:
                clients.send(message)
            except:
                """If the connection is lost that particular client is removed from the users list"""
                clients.close()
                remove(clients)


"""This function removes the client/user from the list that is created so that the particular client gets 
    disconnected and will no longer receive the message"""


def remove(conn_soc):
    if conn_soc in users_list:
        users_list.remove(conn_soc)


def start():
    """listen for upcoming connections,(This number can be increased as per the convenience).
    This is set to a lower limit for now"""
    server.listen(10)
    print("[SERVER] IS LISTENING {}", IP_address)

    while True:
        """Accepts a connection request and stores two parameters,
        conn_soc which is a socket object for that user, and addr
        which contains the IP address of the client user that just
        connected"""
        """ It keeps listening to the messages and accepts"""
        conn_soc, addr = server.accept()

        """Maintains a list of user for ease of broadcasting
        a message to all available people in the chat application"""
        users_list.append(conn_soc)

        """ Address of the user/client connected"""
        print (addr[0] + " connected")

        """ Individual thread for each client handling with specified connection socket object and corresponding address"""
        start_new_thread(handle_client, (conn_soc, addr))

    conn_soc.close()
    server.close()


start()

