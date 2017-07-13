import serial
import pynmea2
import re
from io import StringIO
import atexit
"""
Wrapper for the NMEA GPS device
"""


class GPS:
    def __init__(self, port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            timeout=self.timeout
        )
        atexit.register(self.close)
    def close(self):
        self.ser.close()

    def read(self):
        # read until the next $ and check if its a GPGGA
        buff = StringIO()
        while 1:
            ins = self.ser.read()
            ins = re.sub(r'[\x00-\x1F]|\r|\n|\t', '', ins.decode('ASCII'))
            if ins == '$':
                break
            buff.write(ins)
        try:
            msg = pynmea2.parse(buff.getvalue())
            return repr(msg)
            return {
                'time': msg.time,
                'lat': msg.latitude,
                'lng': msg.longitude,
                'alt': msg.altitude,
                'spd': msg.speed
            }
        except pynmea2.ParseError as e:
            print("Parse error:", e)
            return {'err': str(e)}
