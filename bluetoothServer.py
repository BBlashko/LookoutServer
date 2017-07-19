#!/usr/bin/python2

# Websites:
# https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi

from bluetooth import *


while True:
    MAC_Address = '00:02:72:CB:D0:A8'

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind((MAC_Address, PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    print "Listening on port %d" % port

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "Lookout Server",
                       service_id = uuid
                       # service_classes=[uuid, SERIAL_PORT_CLASS],
                       # profiles=[SERIAL_PORT_PROFILE]
                       )

    print "Waiting for connection on RFCOMM channel %d" % port

    client_sock, client_info = server_sock.accept()

    print("Accepted connection from ", client_info)

    # Receive messages from client
    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0: break
            print("received [%s]" % data)

    # raise an exception if there was any error
    except IOError:
        pass

    print("disconnected")

    client_sock.close()
    server_sock.close()