import socket, ssl

bindsocket = socket.socket()
bindsocket.bind(('127.0.0.1', 10023))
bindsocket.listen(5)

def deal_with_client(connstream):
    data = connstream.read()
    # null data means the client is finished with us
    while data:
        #if not do_something(connstream, data):
            # we'll assume do_something returns False
            # when we're finished with client
            #break
        data = connstream.read()
    # finished with client



while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key",
                                 ssl_version=ssl.PROTOCOL_TLSv1)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
