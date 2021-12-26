from turtle import RawTurtle, TurtleScreen
from tkinter import *
import turtle
from math import*

# File reading for user inputs
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
print("[Drawing... View the windows 'Cam Profile' and 'Follower Displacement graph']")
class Window(Tk):
    def __init__(self, title, geometry):
        super().__init__()
        self.running = True
        self.geometry(geometry)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.destroy_window)
        self.canvas = Canvas(self)
        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.turtle = RawTurtle(TurtleScreen(self.canvas))

    def update_window(self):
        if self.running:
            self.update()

    def destroy_window(self):
        self.running = False
        self.destroy()

# create windows
win1 = Window('Cam Profile', '640x480+0+0')
win1.geometry("1000x1000")
t1 = win1.turtle # assign turtles

# drawing
t1.speed("fastest")
t1.hideturtle()
x_t = 200 #translation in x direction
y_t = 200 #translation in y direction

try:
    s_f = floor(380 / ceil(h)) #finding scale factor
    R_o = R_b + R_f
except NameError as e:
    print(e)

turtle.delay(10)
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

#################################################################
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
print(bound)

b_pairs = [] #boundary pairs of angular range
for i in range(len(bound)-1):
    b_pairs.append([bound[i],bound[i+1]])
print(b_pairs)
def calc(R,R_p,x_gl): #calculating function that returns coordinates of P
    x_p = R_p * cos(x_gl) - sin(x_gl) * R
    y_p = R_p * sin(x_gl) + cos(x_gl) * R
    mag_N = sqrt((y_p) ** 2 + (x_p) ** 2)
    x_n = -(y_p) / mag_N
    y_n = (x_p) / mag_N
    x_P = R * cos(x_gl) + R_f * x_n
    y_P = R * sin(x_gl) + R_f * y_n
    return x_P, y_P


def cam_f(mo,x,x_gl,B): #function to draw cam profile
    if mo == 'shm rise':
        y = (h/2)*(1-cos(pi*x/B))
        R = R_o + y
        R_p = ((h * pi) / (2 * B)) * sin((pi * x) / B)
        x_P, y_P = calc(R,R_p,x_gl)
        t1.goto(20*x_P+x_t,20*y_P-y_t)
    elif mo == 'shm return':
        y = (h/2)*(1+cos(pi*x/B))
        R = R_o + y
        R_p = -((h * pi) / (2*B)) * sin(pi * x/B)
        x_P, y_P = calc(R, R_p,x_gl)
        t1.goto(20*x_P+x_t, 20*y_P-y_t)
    elif mo == "cycloidal rise":
        y = h*(x/B-(sin(2*pi*x/B)/(2*pi)))
        R = R_o + y
        R_p = (h/B) * (1 - cos(2*pi * x/B))
        x_P, y_P = calc(R, R_p,x_gl)
        t1.goto(20 * x_P+x_t, 20 * y_P-y_t)
    elif mo == "cycloidal return":
        y = h * (1 - x/B + sin(2 * pi * x/B) / (2 * pi))
        R = R_o + y
        R_p = (h / B) * (-1 + cos((2 * pi * x) / B))
        x_P, y_P = calc(R, R_p,x_gl)
        t1.goto(20 * x_P+x_t, 20 * y_P-y_t)
    elif mo == "constant acceleration rise":
        if x<=B/2:
            y = 2*h*(x/B)**2
            R = R_o + y
            R_p = 4*h*x/(B**2)
            x_P, y_P = calc(R, R_p,x_gl)
        elif x>B/2:
            y = h*(1-2*(1-x/B)**2)
            R = R_o + y
            R_p = 4 * h * (1-x/B)/B
            x_P, y_P = calc(R, R_p,x_gl)
        t1.goto(20 * x_P+x_t, 20 * y_P-y_t)
    elif mo == "constant acceleration return":
        if x<=B/2:
            y = h*(1-2*(x/B)**2)
            R = R_o + y
            R_p = -((h * pi) / (2 * B)) * sin(pi * x/B)
            x_P, y_P = calc(R, R_p,x_gl)
        elif x>B/2:
            y = 2*h*(1-x/B)**2
            R = R_o + y
            R_p = -4 * h * (1 - x/B) / B
            x_P, y_P = calc(R, R_p,x_gl)
        t1.goto(20 * x_P+x_t, 20 * y_P-y_t)
    elif mo == "up dwell":
        R = R_o + h
        R_p = 0
        x_P, y_P = calc(R, R_p,x_gl)
        t1.goto(20 * x_P+x_t, 20 * y_P-y_t)
    elif mo == "down dwell":
        R = R_o
        R_p = 0
        x_P, y_P = calc(R, R_p, x_gl)
        t1.goto(20 * x_P+x_t, 20 * y_P-y_t)
M = ['shm rise',"shm return","cycloidal rise","cycloidal return","constant acceleration rise","constant acceleration return","up dwell","down dwell"]
try:
    for i in range(0,361): #global angle
        for bp in b_pairs:
            if bp[0]<=i<=bp[1]: #check global angle
                if i == 0:
                    seg_no = b_pairs.index(bp)
                    if not mo_types[seg_no] in M:
                        print("Error: Type of motion not recognised.")
                        break
                    else:
                        t1.pu()
                        x_gl = radians(i)
                        x_lc = x_gl - radians(bp[0]) #finding angle x local to segment
                        cam_f(mo_types[seg_no], x_lc, x_gl, radians(ranges[seg_no]))
                        t1.pd()
                else:
                    x_gl = radians(i)
                    x_lc = x_gl - radians(bp[0]) #finding angle x local to segment
                    seg_no = b_pairs.index(bp)
                    cam_f(mo_types[seg_no],x_lc,x_gl,radians(ranges[seg_no]))
except IndexError as e:
    print(e)
t1.speed(6)
#drawing follower
t1.setheading(90)
try:
    t1.circle(-R_f*20)
except NameError as e:
    print(e)
#drawing follower
t1.pencolor("red")
try:
    t1.circle(R_b*20)
    t1.left(90)
    t1.pu()
    t1.fd(R_b*20)
    t1.pd()
    t1.dot()
    t1.pu()
    t1.bk((R_b+R_f)*20)
    t1.pencolor("black")
    t1.pd()
    t1.dot()
except NameError as e:
    print(e)

# update windows (the mainloop)
#############################################################################
screen = turtle.Screen()
screen.title("Follower Displacement graph")
p=turtle.Turtle()
p.hideturtle()
turtle.delay(0)
screen.setup(600,600,-1,0)
screen.setworldcoordinates(-100,-100,500,500)
p.hideturtle()
#drawing x-axis########
p.fd(380)
p.stamp()
p.up()
p.goto(0,0)
#drawing y-axis########
p.pd()
p.begin_fill()
p.setheading(90)
p.fd(390)
p.setheading(180)
p.fd(5)
for i in range(2):
    p.right(120)
    p.fd(10)
p.right(120)
p.fd(5)
p.end_fill()
p.goto(0,0)
p.setheading(0)
#drawing ticks on x-axis
for i in range(0,361):
    if i%30==0:
        p.setheading(-90)
        p.fd(5)
        p.bk(5)
        p.setheading(0)
        p.fd(1)
    else:
        p.fd(1)
p.goto(0,0)
#drawing ticks on x-axis
for i in range(0,361):
    if i%30==0:
        p.setheading(-90)
        p.fd(5)
        p.bk(5)
        p.setheading(0)
        p.fd(1)
    else:
        p.fd(1)
p.goto(0,0)
#drawing ticks on y-axis
p.setheading(90)
for i in range(0,390):
    if i%s_f==0:
        p.setheading(180)
        p.fd(5)
        p.bk(5)
        p.setheading(90)
        p.fd(1)
    else:
        p.fd(1)
p.goto(0,0)
#labelling the x-axis
p.setheading(0)
for i in range(0,361):
    p.pu()
    if i%30==0:
        p.setheading(-90)
        p.fd(20)
        p.write(str(i),font=("Times New Roman", 10), align="center")
        p.bk(20)
        p.setheading(0)
        p.fd(1)
    else:
        p.fd(1)
p.goto(0,0)
# labelling the y-axis
p.setheading(90)
p.pu()
p.bk(8)
for i in range(0,400):
    if i%s_f==0:
        p.setheading(180)
        p.fd(10)
        p.write(str(int(i//s_f)), font=("Times New Roman", 10), align="right")
        p.bk(10)
        p.setheading(90)
        p.fd(1)
    else:
        p.pu()
        p.fd(1)
p.goto(0,400)
p.write("Displacement/cm", font=("Times New Roman", 10), align="right")
p.pu()
p.goto(380,-20)
p.write("Angle/degrees",font=("Times New Roman", 10), align="left")
p.pu()
p.goto(0,0)

#drawing graph
p.pd()
turtle.delay(10)
p.hideturtle()
#################################################################
b_pairs = []
for i in range(len(bound)-1):
    b_pairs.append([bound[i],bound[i+1]])

def disp(mo,x,B): #function to draw displacement graph
    p.pencolor("blue")
    if mo == 'shm rise':
        y = (h/2)*(1-cos(pi*x/B))
        p.goto(i,s_f*y)
    elif mo == 'shm return':
        y = (h/2)*(1+cos(pi*x/B))
        p.goto(i, s_f * y)
    elif mo == "cycloidal rise":
        y = h*(x/B-(sin(2*pi*x/B)/(2*pi)))
        p.goto(i, s_f * y)
    elif mo == "cycloidal return":
        y = h * (1 - x/B + sin(2 * pi * x/B) / (2 * pi))
        p.goto(i, s_f * y)
    elif mo == "constant acceleration rise":
        if x<=B/2:
            y = 2*h*(x/B)**2
        elif x>B/2:
            y = h*(1-2*(1-x/B)**2)
        p.goto(i,s_f*y)
    elif mo == "constant acceleration return":
        if x<=B/2:
            y = h*(1-2*(x/B)**2)
        elif x>B/2:
            y = 2*h*(1-x/B)**2
        p.goto(i, s_f * y)
    elif mo == "up dwell":
        p.goto(i,s_f*h)
    elif mo == "down dwell":
        p.goto(i,0)
try:
    for i in range(0,361): #global angle
        for bp in b_pairs:
            if bp[0]<=i<=bp[1]: #check global angle
                x_gl = radians(i)
                x_lc = x_gl - radians(bp[0]) #angle local to segment
                seg_no = b_pairs.index(bp)
                disp(mo_types[seg_no],x_lc,radians(ranges[seg_no]))
    print("Completed! Check cam profile and displacement graph.")
except IndexError as e:
    print(e)
while win1.running:
    win1.update_window()