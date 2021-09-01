#!/usr/bin/python

'''
-----------------------------------------------------------------------------
SOURCE FILE:    echo-server.py

PROGRAM:        echo-server

FUNCTIONS:      void main()
                void GETsend()
                void SENDretrieve()

DATE:           October 3th, 2020

REVISIONS:      N/A

DESIGNER:       Kevin Lo

PROGRAMMER:     Kevin Lo

NOTES:
The server side of echo-client.py which communicates with a client to either GET or SEND files
GET being get a file from server and send to client
SEND being get a file from client and send to server
-----------------------------------------------------------------------------
'''

import os.path
from socket import *

myHost = ''                 # '' to set the default IP to localhost
clientListenPort = 7005     # Listening port number
clientDataPort   = 7006     # Data port number

'''
/*--------------------------------------------------------------------------
FUNCTION:       GETsend
 
DATE:           October 3th, 2020 (Date function writtten)
 
REVISIONS:      N/A (Date and explanation of revisions if applicable)
 
DESIGNER:       Kevin Lo
 
PROGRAMMER:     Kevin Lo
 
INTERFACE:      void GETsend(connection connection, string filePath)
                    connection connection: the connection to the client using data socket
                    string filePath: The file to send to the client

RETURNS:        void

NOTES:
Using the data connection connection, it sends the specified filePath file to the client
in the form of 1024 byte packets until file is completely read and sent the client
-----------------------------------------------------------------------------
'''
def GETsend(connection, filePath):
    packetCount = 1;
    readFile = open(filePath, 'rb')     # open file to read in binary
    line = readFile.read(1024)          # load the first 1024 bytes into buffer
    while line:                         # repeat until there are still lines to read
        connection.send(line)           # send 1024 byte buffer to client
        print('Sending Packet number: ', packetCount)
        line = readFile.read(1024)      # load the next 1024 bytes into buffer
        packetCount += 1
    readFile.close()                    # close the open file
    print('done GET file', filePath)

'''
/*--------------------------------------------------------------------------
FUNCTION:       SENDretrieve

DATE:           October 3th, 2020 (Date function writtten)

REVISIONS:      N/A (Date and explanation of revisions if applicable)

DESIGNER:       Kevin Lo

PROGRAMMER:     Kevin Lo

INTERFACE:      SENDretrieve(connection connection, string destName)
                    connection connection: the connection to the client using the data socket
                    string destName: the name you want to save the file as from the client
 
RETURNS:        void

NOTES:
Using the data connection connection, it receives the file in 1024byte packets until completed
and saves the file as destName
-----------------------------------------------------------------------------
'''
def SENDretrieve(connection, destName):
    print('Writing to:', destName)
    with open(destName, 'wb') as writeFile:
        print ('opened file to write')
        packetCount = 1
        while True:
            data = connection.recv(1024)
            print('Receiving packet number: ', packetCount)
            if not data: break
            writeFile.write(data)
            packetCount += 1
    writeFile.close()
    print('finished writing file')


'''
/*--------------------------------------------------------------------------
FUNCTION:       main

DATE:           October 3th, 2020 (Date function writtten)

REVISIONS:      N/A (Date and explanation of revisions if applicable)

DESIGNER:       Kevin Lo

PROGRAMMER:     Kevin Lo

INTERFACE:      void main()

RETURNS:        void

NOTES:
The main loop of the server, it waits for the client to connect on the listenSocket.
Performs actions once a client connects to the server with SEND or GET opTypes
-----------------------------------------------------------------------------
'''
def main():
    # listen socket setup
    print('listensocket Setup')
    sockListenObj = socket(AF_INET, SOCK_STREAM)        # Create a TCP socket for listening
    sockListenObj.bind((myHost, clientListenPort))      # Bind to listen port 7005
    sockListenObj.listen(5)                             # Max 5 connections

    # data socket setup
    print('datasocket Setup')
    sockDataObj = socket(AF_INET, SOCK_STREAM)          # Create a TCP socket for listening
    sockDataObj.bind((myHost, clientDataPort))          # Bind to listen port 7006
    sockDataObj.listen(5)                               # Max 5 connections

    while True:                                         # listen until process killed
        # ListenConnection control setup
        print('listenConnection Setup')
        listenConnection, address = sockListenObj.accept()
        print('listenConnection Connected:', address)   # Print the connected client address

        while True:
            opType = ''

            # Setting up opType
            listenData = listenConnection.recv(1024)    # Read the operation data GET/SEND
            if not listenData: break                    # Break out if its not data
            if listenData.decode() == 'GET':            # Assign GET if its GET
                opType = 'GET'
            elif listenData.decode() == 'SEND':         # Assign SEND if its SEND
                opType = 'SEND'
            listenConnection.send(listenData)           # Send back operation type to client to notify
            print('opType: ', opType)

            # Setting and checking filePath (no checking if its a SEND command
            listenData = listenConnection.recv(1024)    # Read the filepath sent
            if not listenData: break                    # Break out if its not data
            filePath = listenData.decode()              # Decode the filepath
            if opType == 'GET':
                fileExists = os.path.isfile(filePath)   # Check if filePath is valid path to a file
                if not fileExists:                      # If file does not exist, send ERROR message to client and break
                    listenConnection.send('ERROR'.encode())
                    break
            listenConnection.send(listenData)           # Send back filepath
            print('filePath: ', filePath)

            print('dataConnection Setup')
            dataConnection, address = sockDataObj.accept()
            print('dataConnection Connected:', address)  # Print the connected client address

            if opType == 'GET':
                GETsend(dataConnection, filePath)
            elif opType == 'SEND':
                SENDretrieve(dataConnection, filePath)

            print('Closing dataConnection')
            dataConnection.close()  # Close the finished dataConnection


        print('Closing listenConnection')
        listenConnection.close()
        print('')
    print('connection closed')

main()
