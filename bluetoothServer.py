#!/usr/bin/python2

# informational Website:
# https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi

from bluetooth import *

MAC_Address = '00:02:72:CB:D0:A8'
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

while True:
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind((MAC_Address, PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    print "Listening on port %d" % port

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
            with open("settings.json", "a+") as file:
                data = client_sock.recv(1024)
                if len(data) == 0:
                    break
                print data
                if (data == "request current settings"):
                    message = file.read()
                    if len(message) > 0:
                        content = file.read()
                        client_sock.send(message)
                    else:
                        client_sock.send("")
                elif (data == "checking connection"):
                    client_sock.send("connection exists")
                else:
                    # in case of duplicate data transmission
                    if data.count('{') > 1:
                        data = data.split("{")[1]
                        data = "{" + data
                        print "split data"
                    file.seek(0)
                    file.truncate()
                    file.write(data)
                file.flush()

    # raise an exception if there was any error
    except IOError as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        error = template.format(type(ex).__name__, ex.args)
        print error

    print("disconnected")

    client_sock.close()
    server_sock.close()