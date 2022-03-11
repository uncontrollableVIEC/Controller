import socket
def read_from_server():
    # create socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to 192.168.8.190, port 5000
    server_address = ('192.168.8.205',5000)
    print ('connecting to %s port %s' %server_address)
    sock.connect(server_address)
    sock.settimeout(5)

    try:
        # Send data
        output = "A930BF21"
        print ('Sending: %s' %output)
        sock.sendall(bytearray(output.encode()))

        # wait for response
        bytes_received = 0
        
        while bytes_received <= 0:
            data = sock.recv(5000)
            bytes_received += len(data)
        # print ('received:\n%s' % data.decode())
        return data.decode()

    finally:
        print ('Disconnecting...')
        sock.close()
