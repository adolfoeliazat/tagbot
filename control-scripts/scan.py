#!/usr/bin/python

from __future__ import print_function
import nxt.locator, sys, serial
from nxt.motor import *
from nxt.sensor import *
from math import pi
from datetime import datetime
from time import sleep

TagBot = nxt.locator.find_one_brick()   # connect to nxt
lift = Motor(TagBot, PORT_A)      # motor & sensor port mapping
drive = Motor(TagBot, PORT_B)
infra = MSDIST(TagBot, PORT_4)

tag = sys.argv[1]   # arguments from script call

repeats = 5     # number of times to measure with same settings
divisions = 4   # number of orientations in 100 degrees
# some unit conversions
d_angle = 100/divisions

addr  = '/dev/ttyUSB0'  # serial port to read data from
baud  = 115200            # baud rate for serial port
pt=serial.Serial(addr,baud) # setup port

try:
    for y in range(divisions):
        if y!=0:
            lift.turn(-100, d_angle)
        for n in range(repeats+1):
            print(datetime.now(), tag ,str(y*d_angle).zfill(3), str(n), sep=",", end=",")
            pt.flushInput()
            drive.run(-128)
            while infra.get_distance()>200:
                if pt.inWaiting()>0:   # checks for messages
                    data=pt.readline()
                    if data[:3] == "TAG":   # checks if message is a tag...
                        drive.brake()
                        print(str(infra.get_distance()).zfill(3))
                        break   # ...and stops advancing if it is
            else:
                drive.brake()
                if pt.inWaiting()>0:   # checks for messages
                    data=pt.readline()
                    if data[:3] == "TAG":   # checks if message is a tag...
                        print(str(infra.get_distance()).zfill(3))
                    else:
                        print("not found")
                else:
                    print("not found")
            drive.run(127)
            while infra.get_distance()<900:
                pass
            drive.brake()
            pt.flushInput()
    try:
        lift.turn(16, 100)   # runs into block and gets stopped
    except BlockedException:
        pass
    lift.idle()
    drive.idle()
except:
    drive.brake()
    lift.idle()
    drive.idle()
    raise
