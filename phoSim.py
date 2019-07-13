#!/usr/bin/env python3

import photons as photons
import tkinter as tk
import time
import pickle
import tkinter.filedialog as tkfd
import os


root = tk.Tk()

def fileOpen(arg=None):
    filename = tkfd.askopenfilename(initialdir = os.curdir,title = "Open",filetypes = (("Pickle","*.pickle"),("all files","*.*")))
    return filename

filename = fileOpen()#root.destroy()

with open(filename, 'rb') as file:
    y = pickle.load(file)

sz = y['size']
w = sz[0]
h = sz[1]
u = y['contents']

Z = photons.Field(size=sz, scale=32)

for i in range(w):
    for j in range(h):
        zx = u[i][j]
        if zx != []:
            bload = zx[0]
            A = Z.putBlock(block=bload['type'], pos=(i,j), rotate=bload['rotate'])
            A.state = bload['state']
            A.options = bload['options']

time.sleep(1)
stepN  = 0

speed = 1
fps = 60

def Step():
    global speed, fps
    t0 = time.time()
    if not Z.pause:
        for i in range(speed):
            Z.step()
    Z.draw(Z.scale)
    t1 = time.time()
    Z.tkRoot.after(ms=max(1, round(1000//fps-500*(t1-t0))), func=Step)
    #Z.tkRoot.after(ms=max(1, 1000//fps), func=Step)
    #Z.tkRoot.after(ms=1, func=Step)

Z.tkRoot.title("Photons | Simulator")

def setPause(a):
    global Z
    Z.pause = not Z.pause
    print(Z.pause)

def callbackLClick(arg):
    cx = (arg.x-16)//Z.scale
    cy = (arg.y-16)//Z.scale
    cx,cy = Z.adjpos((cx,cy))
    s = Z[cx,cy]
    if s.stack != []:
        if type(s.stack) is not photons.Beam:
            s.stack[0].clickMouse()

Z.tkRoot.bind("<Left>", lambda a: Z.shiftViewportRefresh((-1,0)))
Z.tkRoot.bind("<Right>", lambda a: Z.shiftViewportRefresh((1,0)))
Z.tkRoot.bind("<Up>", lambda a: Z.shiftViewportRefresh((0,-1)))
Z.tkRoot.bind("<Down>", lambda a: Z.shiftViewportRefresh((0,1)))

Z.canvas.bind("<Button-1>", callbackLClick)

Z.tkRoot.bind("p", setPause)
Z.tkRoot.after(ms=10, func=Step)
Z.tkMainLoop()
