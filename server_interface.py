# Server Test Script

import socket
def Import_JSON_From_Server(RFID_value):
    #Connect
    # create socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to 192.168.8.190, port 5000
    server_address = ('192.168.8.205',5000)
    print ('connecting to %s port %s' %server_address)
    sock.connect(server_address)
    # sock.settimeout(5)

    #Send RFID Info
    inData = bytearray()
    outData = bytearray()
   # try:
    # Send data
    print ('Sending: %s' %RFID_value)
    sock.sendall(bytearray(RFID_value.encode()))

    # wait for response
    bytes_received = 0
    total = sock.recv(256)
    print (total.decode())
    total = int(total,10)
    while bytes_received < total:
        inData = inData + sock.recv(256)
        bytes_received = len(inData)
    print ('received:\n%s' % inData.decode())
    #except RuntimeError:
    
    
    bytes_received = 0
    total = sock.recv(256)
    print (total.decode())
    total = int(total,10)
    while bytes_received < total:
        outData = outData + sock.recv(256)
        bytes_received = len(outData)
    print ('received:\n%s' % outData.decode())

#  finally:
    print ('Disconnecting...')
    sock.close()
    # print ("data:\n" + inData.decode() + "\n")
    return inData, outData;
