'''
Created on May 2, 2010

@author: Hussein
'''
import select
import socket
import sys
import threading
from modules.user import User

'------------------------------------------ServerApp----------------------------------------'

class ServerApp:

    'ServerApp class creates a server with custom parameters and responsible for server start/stop'

    def __init__( self, port, host = '', msgSize = 1024, backlog = 5 ):

        self.serverSocket = None       # Create server socket to listen for incoming connections.
        self.host = host               # Hostname of server.
        self.port = port               # Port number that server will listen to new connections on.
        self.backlog = backlog         # Number of pending connections that can be queued up at one time.
        self.msgSize = msgSize         # Number of bytes that can be recieved in a single message.
        self.threads = []              # List of all currently open threads.
        self.running = 1

    def createListenerSocket( self ):

        try:
            self.serverSocket = socket.socket( socket.AF_INET, # Initialize a socket that will be used in listening to new connection. AF_INET: IPv4 protocols family (both TCP and UDP)
                                        socket.SOCK_STREAM )                 # socket.SOCK_STREAM means that socket/connection type is TCP.
            self.serverSocket.setsockopt( socket.SOL_SOCKET, # Set Socket options     level: socket.SOL_SOCKET means socket-level options
                                        socket.SO_REUSEADDR, 1 )             # socket.SO_REUSEADDR: ensure reusability of this socket
            self.serverSocket.bind( ( self.host, self.port ) )               # Bind socket to hostname and port number.
            self.serverSocket.listen( self.backlog )                         # set maximum number of pending connections that can be queued.

        except socket.error, ( errorno, description ):                       # Catch socket exception.
            if self.serverSocket:                                            # Check if socket was created or not (null value check).
                self.serverSocket.close()                                    # Close Socket in case of error.
            print `errorno` + " - socket init error : " + description        # Print socket error.
            print "Server was closed"
            sys.exit( 1 )                                                    # Exit application (sys means system).
        print "Server Started"


    def startServer( self ):

        self.createListenerSocket()                                     # Call a function that creates the listener socket.
        input = [self.serverSocket]                                     # List of sockets that can be used as an input to server.

        while self.running:
            inputReady = select.select( input, [], [] )[0]              # Select a list of ready sockets from input list.
            for soc in inputReady:                                      # Select each item in inputReady list and assign it to soc.
                if soc == self.serverSocket:
                    clientThread = ClientHandler( self.msgSize,         # Create a new ClientHandler which extends thread.
                                        self.serverSocket.accept() )    # accept() returns ("socket" that was assigned to client, "address" is client's IP).
                    clientThread.start()                                # start() calls run() in thread class to start excuting the thread.
                    self.threads.append( clientThread )                 # Add clientThread to end of self.threads list.
                    

    def stopServer( self ):                     # This function is useless, can't be called.
        self.running = 0                        # Set to 0 to end loop in startServer.
        self.serverSocket.close()               # Close listening port.
        for clientThread in self.threads:       # Select each item in self.threads list and assign it to clientThread
            clientThread.join()                 # join() waits for the thread to terminate.


'------------------------------------------ClientHandler----------------------------------------'

class ClientHandler( threading.Thread ):

    'ClientHandler class extends Threading.thread and handles communication with client'

    def __init__( self, msgSize, ( client_socket, address ) ):
        threading.Thread.__init__( self )

        self.client_socket = client_socket           
        self.address = address                     
        self.msgSize = msgSize
        self.loggedin = False                    

    def run( self ):
        running = 1
        while running:
            data = self.client_socket.recv( self.msgSize )       
            if data == "close" :
                self.client_socket.close()                        
                running = 0                                      
            else :
                self.parse_request(data)
    
    def parse_request(self, data):
        tokenz = data.split("#")
        code = tokenz[0]
        args = tokenz[1:]
        if not self.loggedin:
            if code == "LGN_REQ":
                self.user = User.login(args[0], args[1])
                #self.client_socket.send()
            elif code == "REG_REQ":
                User.register(args[0], args[1])
                pass
                #self.client_socket.send()
            elif code == "VER_REQ":
                self.user = User.verify(args[0], args[1])
                #self.client_socket.send()
        else:
            pass


if __name__ == "__main__":
    server = ServerApp( 50000 )         # Create a new ServerApp that listens on port 50000.
    server.startServer()                # Start server.
