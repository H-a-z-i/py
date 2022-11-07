"""Server for all main request will be processed here"""
import socket
s_host = "0.0.0.0"
s_port = 5001
s_buffer = 4096

def server():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 #create a socket
    soc.bind((s_host, s_port))                                              #bind the socket to the port
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)               #set the socket options
    soc.listen(5)                                                           #listen for connections
    client, addr = soc.accept()                                             #accept the connection
    print("Connection from: " + str(addr))                                  #print the connection address
    os = client.recv(s_buffer).decode()                                     #get the os name
    print(os)
    input("Server connected to client,  for list of useful commands type 'help', press Enter to continue...")
    while True:
        commands = input("-> ")                                             #get the command from the user
        if commands == "-gf":                                               #-gf command will send the GetFile command to the client, a prompt will ask for the file name.
            client.send("GetFile".encode())
            data = client.recv(1024).decode()
            if data == "filename":
                filename = input("Enter the file name with correct extension: ")
                client.send(filename.encode())
                data = client.recv(1024).decode()
                if data[:6] == 'EXISTS':                                                                        #Check if the files exists from the client response
                    filesize = int(data[6:])
                    data = input("File exists, " + str(filesize) + "Bytes, download (Y/N)? -> ")                #User asked for download confirmation
                    if data == 'Y' or data == 'y':
                        client.send("ok".encode())
                        data = (client.recv(1024).decode())
                        totalRecv = len(data)
                        #print(totalRecv)                                       #Checks used to see response from client were valid, remove for production
                        #print(data)                                            #Checks used to see response from client were valid, remove for production
                        with open('new_' + filename,'w') as file:
                            file.write(data)
                            print("Download of " + filename + " is complete")
                            #while totalRecv < filesize:
                                #totalRecv += len(data)
                                #file.write(data)
                                #print("{0:.2f}".format((float(totalRecv) / float(filesize)) * 100) + "% Done, Download" + filename + "is complete") #To do download %


            else:
                print("File does not exist!")                           #If file doenst exsist the connection is closed.
                client.close()                                          #TO-DO: Connection closed, replace with loop, user feedback to check file name and correct path
                break
        #client.send(commands.encode())
        #data = client.recv(1024).decode()
        #print((data))
    #conn.close()
if __name__ == '__main__':
    server()

