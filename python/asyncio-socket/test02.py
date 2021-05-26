import socket


def main():
    rsock, wsock = socket.socketpair()
    print(rsock, wsock)
    wsock.close()
    rsock2, wsock2 = socket.socketpair()
    print(rsock2, wsock2)
    rsock.close()


main()
