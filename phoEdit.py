#!/usr/bin/env python3

import photons as ph
import tkinter as tk
import tkinter.filedialog as tkfd
import libMain as main
import libColor as color
import copy
import pickle
import os

_oc = ph._oc

imp = []
for module in (main, color):
    imp += module.__include__

def writeWH():
    global fieldWidth, fieldHeight, fieldScale, rootOptions
    fieldWidth = int(entryW.get())
    fieldHeight = int(entryH.get())
    fieldScale = int(entryS.get())
    rootOptions.destroy()

rootOptions = tk.Tk()

label1 = tk.Label(rootOptions, width=10, text="width:")
label2 = tk.Label(rootOptions, width=10, text="height:")
label3 = tk.Label(rootOptions, width=10, text="scale:")
label4 = tk.Label(rootOptions, width=10)

entryW = tk.Entry( master=rootOptions, width=10)
entryH = tk.Entry( master=rootOptions, width=10)
entryS = tk.Entry( master=rootOptions, width=10)

label1.grid(column=0, row=0)
label2.grid(column=0, row=1)
label3.grid(column=0, row=2)
label4.grid(column=2, row=1)

entryW.grid(column=1,row=0)
entryH.grid(column=1,row=1)
entryS.grid(column=1,row=2)

entryW.insert(0, "12")
entryH.insert(0, "12")
entryS.insert(0, "32")

buttonOK = tk.Button(rootOptions, text="Create", command=writeWH)
buttonOK.grid(column=1,row=3)
rootOptions.mainloop()


Z = ph.Field(size=(fieldWidth, fieldHeight), scale=fieldScale)



def editorLoop():
    Z.draw(Z.scale)
    pass

Z.tkRoot.after(ms=15,func=editorLoop)

windowOpened = False

blockAddData = {'blockType':main.BlockSolid, 'rotate':0, 'options':{}}

actions = []

redo = []

def _lc(x):
    return {'x':x['x'], 'y':x['y']}

def blockFromData(x,y,data):
    global Z
    if data != {}:
        A = Z.putBlock(block=data['blockType'], pos=(x,y), rotate=data['rotate'])
        A.options = _oc(data['options'])
    else:
        A = Z.putBlock(block=None, pos=(x,y))
    
def dataFromBlock(x,y):
    C = Z[x,y]
    if C.stack == []:
        return {}
    else:
        B = C.stack[0]
        return {'blockType':B.__class__, 'rotate':B.rotate, 'options':copy.deepcopy(B.options)}

LogEnable = False

def logHistory():
    if LogEnable:
        print("a:",actions)
        print("r:",redo)

def callbackLClick(arg):
    global windowOpened,Z,actions,redo
    if windowOpened is False:
        cx = (arg.x-16)//Z.scale
        cy = (arg.y-16)//Z.scale
        cx, cy = Z.adjpos((cx,cy))
        
        if cx>=0 and cy>=0:
            
            B = dataFromBlock(cx,cy)
            blockFromData(cx,cy, blockAddData)            
            
            Z.draw(Z.scale)
            
            actions.append({'x':cx,'y':cy, 'data':B})
            redo = []
        logHistory()
        
def callbackRClick(arg):
    global windowOpened,Z,actions,redo
    if windowOpened is False:
        cx = (arg.x-16)//Z.scale
        cy = (arg.y-16)//Z.scale
        
        cx, cy = Z.adjpos((cx,cy))
        if cx>=0 and cy>=0:
            
            B = dataFromBlock(cx,cy)
            
            blockFromData(cx,cy,{})
            
            Z.draw(Z.scale)
            
            actions.append({'x':cx,'y':cy, 'data':B})
            redo = []
        logHistory()
        
def undoAction(arg=None):
    global redo, Z
    if actions != []:
        A = actions.pop()
        #A: x, y, data
        
        #B: data -> {blockType, rotate, options}
        bx = A['x']
        by = A['y']
        
        B = dataFromBlock(bx,by)
        blockFromData(**A)
        
        redo.append({'x':bx, 'y':by, 'data':B})
        
        Z.draw(Z.scale)
        logHistory()
        
        
def redoAction(arg=None):
    if redo != []:
        A = redo.pop()
        
        #bx = A['x']
        #by = A['y']
        
        #B = dataFromBlock(bx, by)
        blockFromData(**A)
        
        #actions.append({'x':bx, 'y':by, 'data':B})
        
        Z.draw(Z.scale)
        logHistory()


blockOptions = {}

bii = {x.blockName:x for x in imp}

def changeBlock(arg=None):
    global windowOpened, imp, blockAddData
    cbRoot = None
    
    def _fc():
        global windowOpened
        c = bii[blockName.get()]
        blockAddData['blockType'] = c
        blockAddData['options'] = c.defaultOptions
        windowOpened = False
        cbRoot.destroy()
        
    if not windowOpened:
        windowOpened = True
        cbRoot = tk.Tk()
        blockName = tk.StringVar(master=cbRoot)
        cbOM = tk.OptionMenu(cbRoot, blockName, *[x.blockName for x in imp])
        cbOM.config(width=15)
        cbOM.grid(column=1, row=0)
        
        blockName.set(blockAddData['blockType'].blockName)
        
        cbBut = tk.Button(cbRoot, text="OK", command=_fc)
        cbBut.grid(column=1, row=1)
        label1 = tk.Label(cbRoot, width=10, text="block:")
        label1.grid(column=0, row=0)
        cbRoot.protocol("WM_DELETE_WINDOW",  cbRoot.destroy)
        cbRoot.mainloop()
    Z.draw(Z.scale)
        
def rotateBlock(arg):
    global Z
    cx = (arg.x-16)//Z.scale
    cy = (arg.y-16)//Z.scale
    if cx>=0 and cy>=0:
        s = Z[Z.adjpos((cx,cy))].stack
        if s != []:
            b = s[0]
            b.rotate += 1
            b.rotate %= 4
            Z.draw(Z.scale)

class InvalidOptionValue(Exception):
    pass

def mmm(x):
    try:
        s = [int(i) for i in x.split(" ")]
        if len(s)!=3:
            raise InvalidOptionValue
        else:
            return ph.listToDictColor([i%16 for i in s])
    except ValueError:
        raise InvalidOptionValue

def fb(x):
    print(x)
    return x

def getOptionFromDict(option, root, nm):
    #option:
    #   value: str
    #   name: str
    #   type: str
    #   [options]: list
    
    #returnEntry:
    #   label: Label
    #   var: StringVar
    #   elementsToCreate: list
    #   func: function to pass StringVar thru
    
    if option["type"] == "integer":
        label = tk.Label(root, width=15, text=option['name'])
        var = tk.StringVar(master=root)
        elem = [tk.Entry(root, width=20, textvariable = var)]
        elem[0].insert( tk.END, str(option["value"]) )
        return {
                'name': nm,
                'label': label,
                'var': var,
                'elementsToCreate': elem,
                'func': int
               }
        
    if option["type"] == "bool":
        label = tk.Label(root, width=15, text=option['name'])
        var = tk.BooleanVar(master=root)
        elem = [tk.Checkbutton(root, variable=var, onvalue=True, offvalue=False)]
        if option["value"]:
            elem[0].select()
        var.set(option["value"])
        
        return {
                'name': nm,
                'label': label,
                'var': var,
                'elementsToCreate': elem,
                'func': fb
               }
        
    if option["type"] == "color":
        label = tk.Label(root, width=15, text=option['name'])
        var = tk.StringVar(master=root)
        elem = [tk.Entry(root, width=20, textvariable = var)]
        value = ' '.join([str(option["value"][k]) for k in "rgb"])
        elem[0].insert( tk.END, value )
                
        return {
                'name': nm,
                'label': label,
                'var': var,
                'elementsToCreate': elem,
                'func': mmm
               }
        
    if option["type"] == "colorLetter":
        label = tk.Label(root, width=15, text=option['name'])
        var = tk.StringVar(master=root)
        var.set(option["value"])
        elem = [tk.OptionMenu(root, var, *["r", "g", "b"])]
        
        return {
                'name': nm,
                'label': label,
                'var': var,
                'elementsToCreate': elem,
                'func': lambda x: x
               }

def MessageBox(txt):
    rt = tk.Tk()
    label = tk.Label(master=rt, text=txt)
    button = tk.Button(rt, text="OK", command=rt.destroy)
    label.pack()
    button.pack()
    rt.protocol("WM_DELETE_WINDOW",  rt.destroy)
    rt.mainloop()
    
def manageOptions(arg):
    global Z, windowOpened

    oz = {}

    def _fc():
        global windowOpened
        for i in rtens:
            try:
                oz[i['name']]["value"] = i['func']( i['var'].get() )
            except InvalidOptionValue:
                MessageBox("Invalid value!")
        windowOpened = False
        Z.draw(Z.scale)
        cbRoot.destroy()
    
    if not windowOpened:
        cx = (arg.x-16)//Z.scale
        cy = (arg.y-16)//Z.scale
        cx,cy = Z.adjpos((cx,cy))
        if cx>=0 and cy>=0:
            s = Z[cx,cy].stack
            
            if s != []:
                windowOpened = True
                cbRoot = tk.Tk()
                rtens = []
                oz = s[0].options
                for k in oz:
                    i = oz[k]
                    ow = getOptionFromDict(i, cbRoot, nm=k)
                    rtens.append(ow)
                cbBtn = tk.Button(cbRoot, text="OK", command=_fc)
                cbRoot.protocol("WM_DELETE_WINDOW",  cbRoot.destroy)
                mainLabel = tk.Label(cbRoot, width=40, text="Options")
                mainLabel.grid(column=1, row=1)
                n = 3
                for i in rtens:
                    i['label'].grid(column=0, row=n)
                    for j in i['elementsToCreate']:
                            j.grid(column=1, row=n)            
                            n += 1
                            
                cbBtn.grid(column=1, row=n)
                cbRoot.mainloop()
                
            
            #cbRoot.protocol("WM_DELETE_WINDOW",  cbRoot.destroy)
            #cbRoot.mainloop()
    
    
        
def fileSave(arg=None):
    filename = tkfd.asksaveasfilename(initialdir = os.curdir,title = "Save",filetypes = (("Pickle","*.pickle"),("all files","*.*")))
    try:
        with open(filename, 'wb+') as file:
            pickle.dump(Z.getSerial(), file)
    except IOError:
        MessageBox("IOError!")
    Z.unmark()
    Z.unselect()
    
def fileOpen(arg=None):
    filename = tkfd.askopenfilename(initialdir = os.curdir,title = "Open",filetypes = (("Pickle","*.pickle"),("all files","*.*")))
    
    with open(filename, 'rb') as file:
        y = pickle.load(file)
        
    sz = y['size']
    w = sz[0]
    h = sz[1]
    u = y['contents']
    
    
    if w>Z.size[0]  or h>Z.size[1]:
        MessageBox("File size is "+str(sz)+" cells big.")
    else:
        for i in range(w):
            for j in range(h):
                zx = u[i][j]
                if zx != []:
                    bload = zx[0]
                    A = Z.putBlock(block=bload['type'], pos=(i,j), rotate=bload['rotate'])
                    A.state = bload['state']
                    A.options = bload['options']
        Z.draw(Z.scale)

def makeSelection(arg):
    print("make sel")
    cx = (arg.x-16)//Z.scale
    cy = (arg.y-16)//Z.scale
    if not Z.isMarked() and not Z.isSelected():
        Z.makeMark((cx,cy))
        print(Z.mark)
    elif not Z.isSelected():
        Z.finishSelection((cx,cy))
        print(Z.selection)
    else:
        removeSelection(None)
        
    Z.draw(Z.scale)
        
def removeSelection(arg=None):
    global Z
    Z.unmark()
    Z.unselect()
    Z.draw(Z.scale)

clipboard = None

def copySelection(arg=None):
    global Z, clipboard
    if Z.isSelected():
        clipboard = Z.copySelection()
        
def pasteSelection(arg=None):
    global Z, clipboard
    if clipboard is not None:
        if Z.isMarked():
            print("success")
            Z.pasteSelection(selection=clipboard, pos=Z.mark)
    Z.draw(Z.scale)
    
def pasteSelectionHard(arg=None):
    global Z, clipboard
    if clipboard is not None:
        if Z.isMarked():
            Z.pasteSelection(selection=clipboard, pos=Z.mark, hard=True)
    Z.draw(Z.scale)
    
def clearSelection(arg=None):
    global Z, clipboard
    Z.clearSelection()
    Z.draw(Z.scale)
        
        


Z.canvas.bind("<Button-1>", callbackLClick)
Z.canvas.bind("<Button-2>", makeSelection)
Z.canvas.bind("<Button-3>", callbackRClick)
#Z.tkRoot.bind("<Alt-z>", undoAlt)
Z.tkRoot.bind("<Control-z>", undoAction)
Z.tkRoot.bind("<Alt-z>", redoAction)
Z.tkRoot.bind("b", changeBlock)
Z.tkRoot.bind("<Control-s>", fileSave)
Z.tkRoot.bind("<Control-o>", fileOpen)
Z.tkRoot.bind("r", rotateBlock)
Z.tkRoot.bind("m", manageOptions)

Z.tkRoot.bind("q", removeSelection)
Z.tkRoot.bind("<Control-c>", copySelection)
Z.tkRoot.bind("<Control-v>", pasteSelection)
Z.tkRoot.bind("<Control-d>", clearSelection)
Z.tkRoot.bind("<Alt-v>", pasteSelectionHard)

Z.tkRoot.bind("<Left>", lambda a: Z.shiftViewportRefresh((-1,0)))
Z.tkRoot.bind("<Right>", lambda a: Z.shiftViewportRefresh((1,0)))
Z.tkRoot.bind("<Up>", lambda a: Z.shiftViewportRefresh((0,-1)))
Z.tkRoot.bind("<Down>", lambda a: Z.shiftViewportRefresh((0,1)))


Z.tkRoot.protocol("WM_DELETE_WINDOW",  Z.tkRoot.destroy)

menu = tk.Menu(Z.tkRoot)

filemenu = tk.Menu(menu, tearoff=0)
filemenu.add_command(label="Open (Ctrl+O)", command=fileOpen)
filemenu.add_command(label="Save (Ctrl+S)", command=fileSave)
menu.add_cascade(label="File", menu=filemenu)

editmenu = tk.Menu(menu, tearoff=0)
editmenu.add_command(label="Undo (Ctrl+Z)", command=undoAction)
editmenu.add_command(label="Redo (Ctrl+Y)", command=redoAction)
editmenu.add_command(label="Copy (Ctrl+C)", command=copySelection)
editmenu.add_command(label="Paste (Ctrl+V)", command=pasteSelection)
editmenu.add_command(label="Erase (Ctrl+D)", command=pasteSelection)
menu.add_cascade(label="Edit", menu=editmenu)

libmenu = tk.Menu(menu, tearoff=0)
libmenu.add_command(label="Change block type (B)", command=changeBlock)
libmenu.add_command(label="Manage libraries", command=None)
menu.add_cascade(label="Libraries", menu=libmenu)

"""
btnCopy = tk.Button(master=frame, label="Copy", command=copySelection)
btnPaste = tk.Button(master=frame, label="Paste", command=pasteSelection)
btnErase = tk.Button(master=frame, label="Erase", command=clearSelection)
btnSel = tk.Button(master=frame, label="Change block type", command=changeBlock)
"""

Z.tkRoot.config(menu=menu)

Z.tkRoot.title("Photons | Editor")

Z.tkMainLoop()
