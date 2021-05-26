import socket
import time
import ssl
import select
from Crypto.Cipher import AES
from Crypto import Random

hostname = "elfiny.top"
UDP_PORT = 5005
TCP_PORT = 5006

print("UDP target IP: %s" % hostname)
print("UDP target port: %s" % UDP_PORT)

context = ssl.create_default_context()

with socket.create_connection((hostname, TCP_PORT)) as sock:
	with context.wrap_socket(sock, server_hostname=hostname) as ssock:
		#ssock.setblocking(False)
		cid = ssock.recv(2)
		key = ssock.recv(16)
		chip = AES.new(key, AES.MODE_CBC, b'This is an IV456')

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(cid, (hostname, UDP_PORT))
print(chip.decrypt(sock.recvfrom(1024)[0]))
