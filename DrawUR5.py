# Author: Angelica Bonilla (@monacuca on Github, @abfominaya elsewhere)
# Simple python program for UR5 control over TCP/IP. 
import socket
import time

# Note: There is an actual python interface that calculates IK and poses through RoboDK
# and an RDTE protocol for TCP/IP control of the robot. This is in case you want to directly
# write/read instructions over TCP using UR5Script. 

# ----- URScript parsing helpers -----
# MoveL: Moves using unverse kinematics
def moveL(x, y, z, rx, ry, rz, a, v, s):
    # Format pose for moveL command. 
    pose = ("p[" + str(x) + ", " \
            + str(y) + ", " \
            + str(z) + ", " \
            + str(rx) + ", " \
            + str(ry) + ", " \
            + str(rz) + "]")
    
    # Format message for moveL command: 
    message = ("movel(" + pose + ", a=" + str(a) + ", v=" + str(v) + ")" + "\n")
    # Send message (i.e. pose) through socket and encode
    print(message)
    s.send((message).encode('utf8'))

# MoveJ: Directly controls joint rotation of the UR5
def moveJ(x, y, z, rx, ry, rz, a, v, s):
    # Format pose for moveJ command. 
    pose = ("p[" + str(x) + ", " \
            + str(y) + ", " \
            + str(z) + ", " \
            + str(rx) + ", " \
            + str(ry) + ", " \
            + str(rz) + "]")
    
    # Format message for moveJ command: 
    message = ("movej(" + pose + ", a=" + str(a) + ", v=" + str(v) + ")"+ "\n")
    # Send message (i.e. pose) through socket and encode
    print(message)
    s.send((message).encode('utf8'))


# Sample usage:
# map(10, 1, 100, 1, 1000) => 100
# map(10, 2, 5, 0, 10 ) => 10
# map(10, 5, 20, 1, 2) => 1.25 
def mapV(v, min_sv, max_sv, min_dv, max_dv):
    if (v >= max_sv):
        return max_dv
    if (v <= min_sv):
        return min_dv
    res = ((v - min_sv)/(max_sv-min_sv))*(max_dv - min_dv) + min_dv 
    print(res)
    return res

# ----- Acceleration and Velocity specs for machine -----
a=1.39626
v=1.04719

# Parameters to toggle pen. 
max_z = 0.2 
min_z = 0.1

# Limits for X, Y Coordinates. 
min_x = -0.5
max_x = -0.1
min_y = -0.4
max_y = -0.1

# Limits for canvas size while parsing JSON Coordinates. 
canvas_min_x = 0
canvas_max_x = 0
canvas_min_y = 200
canvas_max_y = 200

# Pen orientation parameters. 
rx = 0.0
ry = 1.75
rz = 0.0

# ----- Basic movement commands -----
def togglePen(X, Y, Z):
    if (Z == max_z):
        moveJ(X, Y, min_z, rx, ry, rz, a, v, s)
        return min_z
    else: 
        moveJ(X, Y, max_z, rx, ry,rz, a, v, s)
        return max_z

# ----- Basic movement commands -----
def MoveTo(X, Y, Z):
    Xi = mapV(X,canvas_min_x, canvas_max_x, min_x, max_x)
    Yi = mapV(Y,canvas_min_y, canvas_max_y, min_y, max_y)
    moveJ(Xi,Yi,Z,rx,ry,rz, a, v, s)

# ----- Machine Set Up -----
# Robot IP Address. 
# Note that to control the robot, it must have the corresponding DNS connection!
HOST = "169.254.154.223"

# UR5 R/obot port. DO NOT CHANGE THIS. 
PORT = 30002

# Set up socket. 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send(("set_digital_out(0,True)" + "\n").encode('utf8'))
s.send(("set_digital_out(0,False)" + "\n").encode('utf8'))

# CONTROL GROUP
# Home base:
x = -0.1
y = -0.1
z =  0.2 # Pen is toggled up 

moveJ(-0.1, -0.1, 0.2, 0, 1.75, 0, a, v, s)
time.sleep(4)

# Rectangle:
moveJ(-0.5, -0.1, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.2, -0.1, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.2, -0.4, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.5, -0.4, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.5, -0.1, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(4)

# EXPERIMENTAL GROUP 
# Home base:
moveJ(-0.5, -0.1, 0.2, 0, 1.75, 0, a, v, s)
time.sleep(4)

# Rectangle:
moveJ(-0.5, -0.1, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.2, -0.1, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.2, -0.4, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.5, -0.4, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
moveJ(-0.5, -0.1, 0.1, 0, 1.75, 0, a, v, s)
time.sleep(2)
data = s.recv(1024)

s.close()

print ("Received", repr(data))