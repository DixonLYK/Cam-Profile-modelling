while True:
    try:
        file = input("Enter file name: ")
        with open(file,"r") as rf:
            try:
                h = float(rf.readline())
                R_b = float(rf.readline())
                R_f = float(rf.readline())
                N = int(rf.readline())
                ranges = rf.readline().split(", ")
                mo_types = rf.readline().split(", ")
            except ValueError:
                print("ValueError")
        break
    except FileNotFoundError as e:
        print(e)

from turtle import*
import time
import turtle
from math import*
#creating screen
wn = turtle.Screen()
wn.setup(600,600)
wn.tracer(0)
wn.title("Cam Profile Animation")
p = turtle.Turtle()
bc = turtle.Turtle() #follower
base = turtle.Turtle() #true base circle
flw = turtle.Turtle()
bc.hideturtle()
base.hideturtle()
p.hideturtle()
flw.hideturtle()
cam_list = []
f_points = []


try:
    R_o = R_b + R_f
except NameError as e:
    print(e)
try:
    for mem in ranges: #removing escape character '\n' and coverting str to int
        if mem[-1] == "\n":
            ranges[ranges.index(mem)] = int(mem[:-1])
        else:
            ranges[ranges.index(mem)] = int(mem)
except ValueError:
    print("ValueError")
except NameError as e:
    print(e)
try:
    for mo in mo_types:
        if mo[-1] == "\n":
            mo_types[mo_types.index(mo)] = mo[:-1]
except NameError as e:
    print(e)

################################################################
bound = [0] #boundary of inequalities for each angular range
try:
    for i in range(len(ranges)):
        sum = 0
        for num in ranges[:i+1]:
            sum += num
        bound.append(sum)
except TypeError as e:
    print(e)
except NameError as e:
    print(e)

b_pairs = [] #boundary pairs of angular range
for i in range(len(bound)-1):
    b_pairs.append([bound[i],bound[i+1]])
def calc(R,R_p,x_gl): #calculating function that returns coordinates of P
    x_p = R_p * cos(x_gl) - sin(x_gl) * R
    y_p = R_p * sin(x_gl) + cos(x_gl) * R
    mag_N = sqrt((y_p) ** 2 + (x_p) ** 2)
    x_n = -(y_p) / mag_N
    y_n = (x_p) / mag_N
    x_P = R * cos(x_gl) + R_f * x_n
    y_P = R * sin(x_gl) + R_f * y_n
    return (20*x_P, 20*y_P)

def cam_f(mo,x,x_gl,B): #points of cam profile generated
    if mo == 'shm rise':
        y = (h/2)*(1-cos(pi*x/B))
        R = R_o + y
        R_p = ((h * pi) / (2 * B)) * sin((pi * x) / B)
        x_P, y_P = calc(R, R_p, x_gl)
        point = turtle.Vec2D(x_P,y_P)

    elif mo == 'shm return':
        y = (h/2)*(1+cos(pi*x/B))
        R = R_o + y
        R_p = -((h * pi) / (2*B)) * sin(pi * x/B)
        x_P, y_P = calc(R, R_p, x_gl)
        point = turtle.Vec2D(x_P, y_P)

    elif mo == "cycloidal rise":
        y = h*(x/B-(sin(2*pi*x/B)/(2*pi)))
        R = R_o + y
        R_p = (h/B) * (1 - cos(2*pi * x/B))
        x_P, y_P = calc(R, R_p, x_gl)
        point = turtle.Vec2D(x_P, y_P)

    elif mo == "cycloidal return":
        y = h * (1 - x/B + sin(2 * pi * x/B) / (2 * pi))
        R = R_o + y
        R_p = (h / B) * (-1 + cos((2 * pi * x) / B))
        x_P, y_P = calc(R, R_p, x_gl)
        point = turtle.Vec2D(x_P, y_P)

    elif mo == "constant acceleration rise":
        if x<=B/2:
            y = 2*h*(x/B)**2
            R = R_o + y
            R_p = 4*h*x/(B**2)
            x_P, y_P = calc(R, R_p, x_gl)
            point = turtle.Vec2D(x_P, y_P)

        elif x>B/2:
            y = h*(1-2*(1-x/B)**2)
            R = R_o + y
            R_p = 4 * h * (1-x/B)/B
            x_P, y_P = calc(R, R_p, x_gl)
            point = turtle.Vec2D(x_P, y_P)

    elif mo == "constant acceleration return":
        if x<=B/2:
            y = h*(1-2*(x/B)**2)
            R = R_o + y
            R_p = -((h * pi) / (2 * B)) * sin(pi * x/B)
            x_P, y_P = calc(R, R_p, x_gl)
            point = turtle.Vec2D(x_P, y_P)

        elif x>B/2:
            y = 2*h*(1-x/B)**2
            R = R_o + y
            R_p = -4 * h * (1 - x/B) / B
            x_P, y_P = calc(R, R_p, x_gl)
            point = turtle.Vec2D(x_P, y_P)

    elif mo == "up dwell":
        R = R_o + h
        R_p = 0
        x_P, y_P = calc(R, R_p, x_gl)
        point = turtle.Vec2D(x_P, y_P)

    elif mo == "down dwell":
        R = R_o
        R_p = 0
        x_P, y_P = calc(R, R_p, x_gl)
        point = turtle.Vec2D(x_P, y_P)
    cam_list.append(point)

M = ['shm rise',"shm return","cycloidal rise","cycloidal return","constant acceleration rise","constant acceleration return","up dwell","down dwell"]
try: #generating cam profile points each degree
    for i in range(0,361): #global angle
        for bp in b_pairs:
            if bp[0]<=i<=bp[1]: #check global angle
                if i == 0:
                    seg_no = b_pairs.index(bp)
                    if not mo_types[seg_no] in M:
                        print("Error: Type of motion not recognised.")
                        break
                    else:
                        p.pu()
                        x_gl = radians(i)
                        x_lc = x_gl - radians(bp[0]) #finding angle x local to segment
                        cam_f(mo_types[seg_no], x_lc, x_gl, radians(ranges[seg_no]))
                        p.pd()
                else:
                    x_gl = radians(i)
                    x_lc = x_gl - radians(bp[0]) #finding angle x local to segment
                    seg_no = b_pairs.index(bp)
                    cam_f(mo_types[seg_no],x_lc,x_gl,radians(ranges[seg_no]))
except IndexError as e:
    print(e)

def disp(mo,x,B): #function to generate coordinates of follower
    p.pencolor("blue")
    if mo == 'shm rise':
        y = (h/2)*(1-cos(pi*x/B))
        f_coor = turtle.Vec2D(20*y+20*R_b,0)
        f_points.append(f_coor)
    elif mo == 'shm return':
        y = (h/2)*(1+cos(pi*x/B))
        f_coor = turtle.Vec2D(20 * y+20*R_b, 0)
        f_points.append(f_coor)
    elif mo == "cycloidal rise":
        y = h*(x/B-(sin(2*pi*x/B)/(2*pi)))
        f_coor = turtle.Vec2D(20 * y+20*R_b, 0)
        f_points.append(f_coor)
    elif mo == "cycloidal return":
        y = h * (1 - x/B + sin(2 * pi * x/B) / (2 * pi))
        f_coor = turtle.Vec2D(20 * y+20*R_b, 0)
        f_points.append(f_coor)
    elif mo == "constant acceleration rise":
        if x<=B/2:
            y = 2*h*(x/B)**2
        elif x>B/2:
            y = h*(1-2*(1-x/B)**2)
        f_coor = turtle.Vec2D(20 * y+20*R_b, 0)
        f_points.append(f_coor)
    elif mo == "constant acceleration return":
        if x<=B/2:
            y = h*(1-2*(x/B)**2)
        elif x>B/2:
            y = 2*h*(1-x/B)**2
        f_coor = turtle.Vec2D(20 * y+20*R_b, 0)
        f_points.append(f_coor)
    elif mo == "up dwell":
        y = h
        f_coor = turtle.Vec2D(20 * y+20*R_b, 0)
        f_points.append(f_coor)
    elif mo == "down dwell":
        y = 0
        f_coor = turtle.Vec2D(20 * y+20*R_b, 0)
        f_points.append(f_coor)

try: #generating follower displacement each angle
    for i in range(0,361): #global angle
        for bp in b_pairs:
            if bp[0]<=i<=bp[1]: #check global angle
                x_gl = radians(i)
                x_lc = x_gl - radians(bp[0]) #angle local to segment
                seg_no = b_pairs.index(bp)
                disp(mo_types[seg_no],x_lc,radians(ranges[seg_no]))
except IndexError as e:
    print(e)

for point in cam_list:
    if cam_list.index(point) ==0:
        p.goto(point)
        base.pu()
        flw.goto(point)
        flw.pd()
        flw.setheading(-90)
        flw.circle(20*R_f)
        base.goto(point)
        base.pd()
        base.setheading(90)
        base.circle(20*R_b)
    else:
        p.goto(point)
    wn.update()

while True:
    for i in range(0,360):
        newlist = []
        for point in cam_list:
            newlist.append(point.rotate(-i))
        for new_p in newlist:
            p.goto(new_p)
        flw.clear()
        flw.goto(f_points[i])
        flw.circle(20*R_f)
        wn.update()
        time.sleep(0.001)
        if i != 359:
            p.clear()
        else:
            pass
        p.pu()
        p.home()
        p.pd()

turtle.done()