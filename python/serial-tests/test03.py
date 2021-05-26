import serial
import os


def main():
    master, slave = os.openpty()
    name = os.ttyname(slave)
    ser = serial.Serial(name, timeout=0)
    serial.timeout = 0
    serial.write_timeout = 0
    os.write(master, b"hi\n")
    print(ser.readall())


main()
