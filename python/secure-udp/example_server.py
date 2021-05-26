import socket
import time
import ssl
import select
from Crypto.Cipher import AES
from Crypto import Random

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain('ssl.everything')


rndfile = Random.new()

CHIPS = []

UDP_IP = "45.76.138.71"
UDP_PORT = 5005
TCP_PORT = 5006
MESSAGE = b"Hello, World2!  "

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

socktcp =  socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socktcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socktcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
socktcp.bind((UDP_IP, TCP_PORT))
socktcp.listen(5)

ssock = context.wrap_socket(socktcp, server_side=True)
conns = []

while True:
	fds = [ssock, sock]
	recv, _, __ = select.select(fds, [], [])
	if ssock in recv:
		conn, addr = ssock.accept()
		#ssock.setblocking(False)
		print("Connected", addr)
		key = rndfile.read(16)
		conn.send(len(CHIPS).to_bytes(2, byteorder='big'))
		CHIPS.append(AES.new(key, AES.MODE_CBC, b'This is an IV456'))
		conn.send(key)
		conns.append(conn)
	if sock in recv:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		print("received message: %s" % data)
		cid = int.from_bytes(data, 'big')
		sock.sendto(CHIPS[cid].encrypt(MESSAGE), addr)
