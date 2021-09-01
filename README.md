# COMP7005Asn1
Basic TCP/IP client/server program that can send a GET or SEND to a remote server files

The server listens on TCP port 7005 and once the server recieves a GET/SEND message the lient will connect on TCP port 7006
and the server will get/send data from the client until there is no more data to read from and close the sockets
