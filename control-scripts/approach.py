#!/usr/bin/python

from __future__ import print_function
import nxt.locator, sys, serial
from nxt.motor import *
from nxt.sensor import *
from math import pi
from datetime import datetime
from time import sleep

TagBot = nxt.locator.find_one_brick()   # connect to nxt
horiz_axis = Motor(TagBot, PORT_A)      # motor & sensor port mapping
vert_axis = Motor(TagBot, PORT_B)
tracks = Motor(TagBot, PORT_C)
rear = Touch(TagBot, PORT_2)
front = Touch(TagBot, PORT_3)
infra = MSDIST(TagBot, PORT_4)

tag = sys.argv[1]   # arguments from script call
grid = sys.argv[2]

repeats = 5     # number of times to measure with same settings
step_cm = 1     # distance moved each step
divisions = 6   # number of orientations in 180 degrees
# some unit conversions
step_rad = 2*step_cm/3.7    # could have done this in 1 step but I like radians
step_deg = 180*step_rad/pi
d_angle = 180/divisions

addr  = '/dev/ttyUSB0'  # serial port to read data from
baud  = 115200            # baud rate for serial port
pt=serial.Serial(addr,baud) # setup port

try:
    for x in range(divisions):
        if x!=0:
            vert_axis.turn(100, d_angle)
        for y in range(divisions):
            if y!=0:
                horiz_axis.turn(100, d_angle)
            elif x!=0:
                continue    # this stops TagBot repeating the vertical measurement
            for n in range(repeats):
                print(datetime.now(), tag, grid, str(x*d_angle).zfill(3) ,str(y*d_angle).zfill(3), str(n), sep=",", end=",")
                pt.flushInput()
                tracks.run(-72)
                while not front.is_pressed():
                    if pt.inWaiting()>0:   # checks for messages
                        data=pt.readline()
                        if data[:3] == "TAG":   # checks if message is a tag...
                            tracks.brake()
                            print(str(infra.get_distance()).zfill(3))
                            break   # ...and stops advancing if it is
                else:
                    tracks.brake()
                    if pt.inWaiting()>0:   # checks for messages
                        data=pt.readline()
                        if data[:3] == "TAG":   # checks if message is a tag...
                            print(str(infra.get_distance()).zfill(3))
                        else:
                            print("not found")
                    else:
                        print("not found")
                if n!=repeats-1:
                    tracks.run(72)
                    pt.flushInput()
                    sleep(0.5)
                    while pt.inWaiting()>0:
                        pt.flushInput()
                        sleep(0.05)
                    else:
                        tracks.brake()
            tracks.run(120)
            sleep(0.2)  #waits to start checking touch sensor in case TagBot tips forwards enough to release it when it starts reversing. May need adjusting (secs)
            while rear.is_pressed():
                pass
            else:
                tracks.brake()
        try:
            horiz_axis.turn(-32, 180-d_angle)   # runs into block and gets stopped
        except BlockedException:
            pass
    try:
        vert_axis.turn(-32, 180-d_angle)
    except BlockedException:
        pass
    horiz_axis.idle()
    vert_axis.idle()
    tracks.idle()
except:
    tracks.brake()
    horiz_axis.idle()
    vert_axis.idle()
    tracks.idle()
    raise
