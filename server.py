# Title to go here
"""Server for all main request will be processed here"""
import socket
s_host = "0.0.0.0"
s_port = 5000
buffer = 4096

"""Connection and global variables for the server"""

print("Awaiting a connection from client")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 #create a socket
s.bind((s_host, s_port))                                              #bind the socket to the port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)               #set the socket options
s.listen(5) # listen
s, addr = s.accept() #connect to the
print("Connected to client at ", addr)
"""Function for server"""

def server():
    from sfunctions import ListCMD
    global client
    global buffer
    global s
    ListCMD(s, buffer)
if __name__ == '__main__':
    server()