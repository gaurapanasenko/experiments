import asyncio
import socket


async def main():
    loop = asyncio.get_running_loop()
    rsock, wsock = socket.socketpair()
    def read():
        data = rsock.recv(1)
        print(data)
        # if not data:
            # rsock.close()
    loop.add_reader(rsock.fileno(), read)
    loop.add_writer(rsock.fileno(), lambda: print(rsock.send(b"hi")))

    # wsock.send(b"hi")
    rsock.close()
    wsock.close()

    await asyncio.sleep(5)


asyncio.run(main(), debug=True)
