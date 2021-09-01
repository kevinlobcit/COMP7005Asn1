#!/usr/bin/python

#-----------------------------------------------------------------------------
 # SOURCE FILE:    echo-client.py
 #
 # PROGRAM:        echoClient
 #
 # FUNCTIONS:      int main(char** argv)
 #                 bool checkGetSend(string opType)
 #                 bool checkFilePath(string filePath)
 #                 void GETretrieve(socket sock, string destName)
 #                 void SENDsend(socket sock, string filePath)
 #                 void serverConnect(string serverHost, string opType, string filePath, string destName
 #
 # DATE:           October 3, 2020
 #
 # REVISIONS:      N/A
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # NOTES:
 # This file is the client that connects to echo-server.py to GET or SEND a file between
 # the  client and server
# --------------------------------------------------------------------------

import sys
import os.path
from socket import *

#--------------------------------------------------------------------------
 # FUNCTION:       checkGetSend
 #
 # DATE:           October 3th, 2020
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # INTERFACE:      bool checkGetSend(string opType)
 #                      string opType: The operation type to perform on the server (GET/SEND)
 #
 # RETURNS:        bool
 #
 # NOTES:
 # Checks if the input opType is valid (GET/SEND) or it will return false
 # -----------------------------------------------------------------------
def checkGetSend(opType):
    if opType == 'GET' or opType == 'SEND':
        return 'TRUE'
    else:
        return 'FALSE'

#--------------------------------------------------------------------------
 # FUNCTION:       checkFilePath
 #
 # DATE:           October 3th, 2020
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # INTERFACE:      bool checkFilePath(string filePath)
 #				        filePath: The path to the source file
 #
 # RETURNS:        boolean
 #
 # NOTES:
 # Checks if the filepath on the client is valid for SEND to server
 # -----------------------------------------------------------------------
def checkFilePath(filePath):
    return os.path.isfile(filePath)

#--------------------------------------------------------------------------
 # FUNCTION:       GETretrieve
 #
 # DATE:           October 3th, 2020
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # INTERFACE:      void GETretrieve(socket sock, string destName)
 #                      sock: The data socket to use to get data from the server
 #                      destName: The name you want to save the file as on the client
 #
 # RETURNS:        void
 #
 # NOTES:
 # Gets a file from the server and send to the client
 # -----------------------------------------------------------------------
def GETretrieve(sock, destName):
    with open(destName, 'wb') as writeFile:     # Open file to write to
        print ('opened file to write')
        packetCount = 1
        while True:                             # Repeat until no more data sent from server
            data = sock.recv(1024)              # Get 1024 bytes from server
            print('Receiving packet number: ', packetCount)
            if not data: break                  # Break if there is no more data sent f rom server
            writeFile.write(data)               # Write the 1024 bytes from data into buffer
            packetCount += 1
    writeFile.close()                           # Close the write file
    print('finished writing file')

#--------------------------------------------------------------------------
 # FUNCTION:       SENDsend
 #
 # DATE:           October 3th, 2020
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # INTERFACE:      void SENDsend(socket sock, string filePath)
 #				        socket sock: The data socket to send data from client to server
 #                      string filePath: The file to send to the server
 #
 # RETURNS:        void
 #
 # NOTES:
 # Sends a file from the client to the server
 # -----------------------------------------------------------------------
def SENDsend(sock, filePath):
    packetCount = 1;
    readFile = open(filePath, 'rb')     # Open file to read
    l = readFile.read(1024)             # Load first 1024 bytes into buffer
    while l:                            # Repeat until no more to read
        sock.send(l)                    # Send 1024 bytes in buffer to server
        print('Sending Packet number: ', packetCount)
        l = readFile.read(1024)         # Load the next 1024 bytes into buffer
        packetCount += 1
    readFile.close()                    # Close the openfile
    print('done SEND file', filePath)

#--------------------------------------------------------------------------
 # FUNCTION:       serverConnect
 #
 # DATE:           October 3th, 2020
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # INTERFACE:      void serverConnect(string serverHost, string opType, string filePath, string destName)
 #				        string serverHost: Ip address to the server
 #                      string opType: GET/SEND command of what operation to do
 #                      string filePath: The source file to copy from
 #                      string destName: The filename to save as
 #
 # RETURNS:        void
 #
 # NOTES:
 # Connects to the server, and performs the specified opType operation to GET/SEND the
 # filePath file and to save it as destName
 # -----------------------------------------------------------------------
def serverConnect(serverHost, opType, filePath, destName):
    # Connect to listen server and send base data opType, filePath
    sockListenObj = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket object
    sockListenObj.connect((serverHost, serverListenPort))  # connect to server IP + port

    sockListenObj.send(opType.encode())  # send what type of operation to do GET/SEND
    data = sockListenObj.recv(1024)  # read server response
    print('Received From Server:', data.decode())

    if opType == 'GET':
        sockListenObj.send(filePath.encode())  # send the filePath
    elif opType == 'SEND':
        sockListenObj.send(destName.encode())  # send the filePath

    data = sockListenObj.recv(1024)  # read server response
    print('Received From Server:', data.decode())

    if not data.decode() == 'ERROR': # Proceed only if server did not send 'ERROR' for getting file
        # Connect to Data server and prepare
        sockDataObj = socket(AF_INET, SOCK_STREAM)
        sockDataObj.connect((serverHost, serverDataPort))

        # Choose which operation to do
        if opType == 'GET':
            GETretrieve(sockDataObj, destName)  # GET file from server
        elif opType == 'SEND':
            SENDsend(sockDataObj, filePath)

        # close sockets once done
        sockDataObj.close()
    else:
        print('File does not exist on server')
    sockListenObj.close()

#globals
serverListenPort = 7005  # Server listen port number
serverDataPort = 7006  # Server data port number

#--------------------------------------------------------------------------
 # FUNCTION:       main
 #
 # DATE:           October 3th, 2020
 #
 # REVISIONS:      N/A (Date and explanation of revisions if applicable)
 #
 # DESIGNER:       Kevin Lo
 #
 # PROGRAMMER:     Kevin Lo
 #
 # INTERFACE:      main(char** argv)
 #                      char** argv: 4 command line arguments containing serverHost, opType, filePath, destName
 #
 # RETURNS:        void
 #
 # NOTES:
 # The main function that takes 4 commandline arguments containing the
 # ip address of server, operation to do, source file to copy, name to save the file as
 # to contact the server to GET or SEND a file from either client or server
 # -----------------------------------------------------------------------
def main():
    serverHost = 'localhost'  # Default IP to connect to
    opType = ''     # Operation Type GET/SEND
    filePath = ''   # Source Filename to GET/SEND
    destName = ''   # Destination Filename for GET/SEND

    # Example command line run of the program
    # python echo-client.py 192.168.1.72 GET bigdog.jpg servertoclient.jpg
    # python echo-client.py serverHost opType filePath destName
    if len(sys.argv) > 3:           # User defined arguments provided at launch
        serverHost = sys.argv[1]    # User has provided a server IP at cmd line arg 1
        opType = sys.argv[2]        # User provided operation GET/SEND
        filePath = sys.argv[3]      # User provided filename
        destName = sys.argv[4]
    else:
        serverHost = input('Enter Server IP address: ')
        opType = input('Enter operation type (GET/SEND): ')
        filePath = input('Enter the filepath to read from: ')
        destName = input('Enter the name to save the file as')

    print('Preparing')
    ready = 0
    if checkGetSend(opType) == 'TRUE':
        ready += 1
        if opType == 'GET':
            ready += 1
        elif opType == 'SEND' and checkFilePath(filePath):
            ready += 1
        else:
            print('ERROR in locating file to SEND:', filePath)
    else:
        print('ERROR bad operation type:', opType)

    if ready == 2:
        serverConnect(serverHost, opType, filePath, destName)

main()
