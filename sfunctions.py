def GetFile(s, buffer):
    s.send("getfile".encode())        ##1 
    filename = s.recv(buffer).decode()    ##2    #cGetfile returned
    if filename == "inputfilename":
        filename = input("Enter the file name with correct extension: ")
        s.send(filename.encode())  ##3
        found = s.recv(buffer).decode()  ##4
        print(found)
        if found[:5] == 'FOUND':                                                                        #Check if the files exists from the client response
            filesize = int(found[5:])
            download = input("File exists, " + str(filesize) + "Bytes, download (Y/N)? -> ")                #User asked for download confirmation
            if download == 'Y' or download == 'y':
                s.send('ok'.encode())   ##5
                contents = s.recv(buffer).decode() ##6
                totalRecv = len(contents)
                print(totalRecv)                                       #Checks used to see response from client were valid, remove for production
                with open('new__' + filename,'wb') as f:
                    f.write(contents.encode())
                    f.close()
                    print("Download of " + filename + " is complete")
                    
        else:
            print("File does not exist!")                           #If file does not exist the connection is closed.

def PutFile(s, buffer):
    import os
    filename = input("Enter the file name with correct extension: ")
    print(filename)
    if os.path.isfile(filename):                            #Checks filepath and name to see if it exists
        data = 'FOUND' + str(os.path.getsize(filename))
        print(data)    
        if data[:5] == 'FOUND':                                                                        
            #filesize = int(data[5:])
            #print(filesize)
            data = input(str(filename) + " found upload (Y/N)? -> ")             
            if data == 'Y' or data == 'y':
                s.send("putfile".encode()) #1
                data = s.recv(buffer).decode()
                if data == 'SEND':
                    s.send(filename.encode()) #2
                    data = s.recv(buffer).decode()
                    if data == 'SENDC':
                        with open(filename) as f:
                            contents = f.read(buffer)
                            s.sendall(contents.encode()) #3
                            f.close()
                #with open(filename) as f:
                    #confile = f.read(sBuffer)
                    #client.sendall(confile.encode())
        else:
            print("File not recognised, try running from from correct directory, or using full a file path")

def ListCMD(s, buffer):
    from sfunctions import GetFile , PutFile
    my_list = ['-g', '-p', '-h','exit']
    print ("For list of supported commands and help enter -h ")
    while True:
        commands = input("-> ")
        if commands not in my_list:
            print("Invalid command")
        elif commands == "-g":
            GetFile(s, buffer)
        elif commands == "-p":
            PutFile(s, buffer)
        elif commands == "-h":
            help()
        elif commands == "exit":
            s.send("exit".encode())
            print("Shuttting down any live clients and server")
            s.close()
            break

def help():
    print(""" The following list of commands are available, all commmands must be run from the server, passing multiple arguments is not supported at this time:
Command list:

    -g   -   Get / download file from client.

    -p   -   Put / upload file to client.

    -h   -   Show the help message.

    exit -  Stops the server, alternatively ctrl + c to exit the server
    """)
