'''
Created on Mar 10, 2010

@author: Hussein
'''
import socket

client_socket = socket.socket(socket.AF_INET,           # Initialize a socket that will be used to communicate client to server.
                               socket.SOCK_STREAM)      # socket.SOCK_STREAM means that socket/connection type is TCP.
client_socket.connect(("localhost", 50000))             # Connects client socket to a host "localhost" that listens on port (50000).

running = 1                                             # Flag shows program status (Running/closed).
while running:
    data = raw_input ( "SEND( TYPE close to quit):" )   # Program waits until it reads input from user.
    if data == "close" :
        client_socket.send(data)                        # Send a close command to server to close assigned socket on the server.
        client_socket.close()                           # Close client socket.
        running = 0                                     # Set "running" flag to false to exit the loop.
    elif data == "r" :
        rsp = client_socket.recv( 1024 )
        print "RESP : " + rsp
    else:
        client_socket.send(data)                        # Send input data to server.