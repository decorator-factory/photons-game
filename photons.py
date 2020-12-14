#!/usr/bin/env python3
import random
import tkinter as tk
import tkinter.font as tkf
import math

dirDef = {'u':(0,-1), 'r': (1,0), 'd':(0,1), 'l':(-1,0)}

def colorIsNull(x):
    return (x == {'r':0, 'g':0, 'b':0})

def sign(x):
    if x==0:
        return 0
    elif x>0:
        return 1
    else:
        return -1

def listToTkColor(l):
    return '#{:02x}{:02x}{:02x}'.format(*l)

def listToDictColor(l):
    return {'r':l[0], 'g':l[1], 'b':l[2]}

def colorFromLetter(color):
    if color == "g":
        return '#00FF00'
    elif color == "r":
        return '#FF0000'
    else:
        return '#0000FF'

def emptyColor():
    return {'r':0,'g':0,'b':0}

def fixColor(c):
    return {'r':c['r']%16,'g':c['g']%16,'b':c['b']%16}

def rotateDir(direction, rotate):
    rotate %= 4
    if rotate == 0:
        return direction
    nextDir = {'u':'r', 'r':'d', 'd':'l', 'l':'u'}
    return rotateDir(nextDir[direction], rotate-1)
    
def unpackGrElement(element, canvas, scale, pos, rotate):
    t = element[0]
    m = eval("canvas.create_"+t)
    
    z = list(element[1])
    
    z = rotateGrElement(z, rotate)
    
    try:
        z = [x*scale+16 for x in z]
    except TypeError:
        raise ValueError(z)
    
    for n in range(len(z)):
        z[n] += pos[n%2]*scale
    
    
    if len(element)==3:
        return m(*z, **element[2])
    else:
        return m(*z)

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def rotatePoint(x,y, angle):
    return rotate((0.5,0.5), (x,y), math.radians(angle))

def rotateGrElement(pts, rotate):
    r = []
    for i in range(0, len(pts), 2):
        x = rotatePoint(pts[i],pts[i+1], rotate*90)
        r.append(x[0])
        r.append(x[1])
    return r


def _oc(d):
    o = {}
    for k in d:
        i = d[k]
        o[k] = i.copy() if type(i) in (dict, list) else i
    return o

def unpackElements(elList, canvas, scale, pos, rotate):
    return [unpackGrElement(x, canvas, scale, pos, rotate) for x in elList]
    

class Block:
    defaultState = {"active":True, "state":"main"}
    defaultOptions = {}
    blockName = "Block"
    
    def getGraphics(self, scale, offset=(0,0)):
        glm = self.__class__.getGraphicsList
        pz = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        return unpackElements(glm(self), self.cell.field.canvas, scale, pz, self.rotate)
    
    gGraphics = [
            ("line", (0,0,1,0)),
            ("line", (1,0,1,1)),
            ("line", (1,1,0,1)),
            ("line", (0,1,0,0))
            ]

    def clickMouse(self):
        pass
    
    def getGraphicsList(self):
        return Block.gGraphics
    
    def __str__(self):
        return "Block @"+str(self.cell.pos)
    
    def __init__(self, cell=None, neighbors=None, pos=(0,0), rotate = 0):
        # neighbors: u, r, d, l
        self.options = {}
        d = self.__class__.defaultOptions.copy()
        for k in d:
            i = d[k]
            self.options[k] = i.copy() if type(i) is dict else i
        self.randomId = random.randint(1, 100000)
        self.cell = cell
        if neighbors is None:   
            neighbors = cell.pullNeighbors(pos)
        self.neighbors = neighbors
        self.state = self.__class__.defaultState.copy()
        self.pos = pos
        self.rotate = rotate
        
    def tick(self):
        return None
    
    def getOption(self, option):
        return self.options[option]["value"]
    
    def setOption(self, option, v):
        self.options[option]["value"] = v
    
    def stack(self, z):
        return (None, None)
    
    def pretty(self):
        return ("╔═══╗","║:-)║","╚═══╝")
    
    def previewPretty(self):
        for i in self.pretty():
            print(i)
    
class Cell:
    def __init__(self, field, pos):
        self.stack = []
        self.field = field
        self.pos = pos
        
    def pullNeighbors(self, pos):
        return self.field.pullNeighbors(pos)
        
    def tick(self, beam, sall):
        rmv = []
        add = []
        n = 0
        if self.stack != []:
            #print("ticking "+self.__repr__())
            pass

        for i in self.stack:
            if ((type(i) is Beam) == beam) or sall:
                #print("unpacking stack element",i)
                i.tick()
                q = i.stack(self.stack[n+1:])
                if q == (None, None) or q==None:
                    continue
                elif type(q[0]) is str:
                    q = [q]
                #print("i.stack method returned:",q)
                for s in q:
                    if s[0] == "remove":
                        rmv += s[1]
                        for x in s[1]:
                            x.cell = None
                    elif s[0] == "replace":
                        rmv += [i]
                        i.cell = None
                    if s[0] == "add" or s[0] == "replace":
                        for j in s[1]:
                            j.cell = self
                            add += [j]
            n += 1
        
        [self.stack.remove(x) for x in rmv if x in self.stack]
        self.stack += add
        
        for i in self.stack:
            if i.pos != self.pos:
                self.field[i.pos].stack.append(i)
                self.stack.remove(i)
                
        
                    
    
    def getStackLen(self):
        return ("┌   ┐"," {: 3} ".format(len(self.stack)),"└   ┘")
    
    def __repr__(self):
        return "Cell @"+str(self.pos)
        
        
class Beam:
    """
    Cell cell = the cell the beam belongs to
    dict/NoneType neighbors = the dict of adjacent Cell cells
    dict color = r,g,b components of the color
    tuple pos = x,y of the beam on the field
    """
    #
    def __init__(self, field, cell, neighbors=None, direction='r', color = {'r':0, 'g':0, 'b':0}, pos=("deprecated","deprecated"), active=0):
        # neighbors:    u, r, d, l
        # directions:   u, r, d, l
        # colors:       r, g, b
        if neighbors is None:
            self.neighbors = cell.pullNeighbors(pos)
        self.field = field
        self.neighbors = neighbors
        self.direction = direction
        self.color = color
        self.cell = cell
        self.pos = self.cell.pos
        self.active = active
    
    
    def getGraphicsList(self):
        z = self.color
        cl3 = [(z['r']+1)*16-1,(z['g']+1)*16-1,(z['b']+1)*16-1]
        clr = listToTkColor(cl3)
        opt = {'fill': clr, 'width':4}
        return [
                ("line",(0,0.5,1,0.5), opt),
            ]
    
    def getGraphics(self, scale, pos):
        glm = self.__class__.getGraphicsList
        rt = 1 if self.direction in "ud" else 0
        return unpackElements(glm(self), self.cell.field.canvas, scale, (self.pos[0]-pos[0],self.pos[1]-pos[1]), rt)
    
    def tick(z):
        return None
    
    def stack(self, z):
        if self.active==0:
            ggg = dirDef[self.direction]
            newPos = (self.pos[0] + ggg[0], self.pos[1] + ggg[1])
            if newPos[0]<0 or newPos[1]<0 or newPos[0]>=self.field.size[0] or newPos[1]>=self.field.size[1] : 
                return ("remove", [self])
            else:
                return ("replace", [Beam(   
                                            cell = self.field[newPos],
                                            field = self.field,
                                            direction = self.direction,
                                            color = self.color,
                                            pos = newPos,
                                            active = 2
                                        )]
                       )
        else:
            self.active -= 1
            return (None, None)
    
    def __repr__(self):
        return "Beam @"+str(self.pos)
    
    
class Field:
    def __init__(self, size=(16,16), scale = 16):
        self.size = size
        self.field = []
        for i in range(size[0]):
            q = [Cell(field=self, pos = (i,j)) for j in range(size[1])]
            self.field.append(q)
        self.tkRoot = tk.Tk()
        self.scale = scale
        self.mark = (-1,-1)
        self.selection = ((-1,-1), (-1,-1))

        print("Field object initialized without errors (surprisingly)")
        self.viewport = size
        self.viewpos = (0,0)
        if max(size[0], size[1])>20:
            self.viewport = (min(size[0],32),min(size[1],24))

        self.canvas = tk.Canvas(self.tkRoot, width=self.viewport[0]*scale+64, height=self.viewport[1]*scale+64)
        self.canvas.grid(row=1, column=0)
        self.font = tkf.Font(family="Times New Roman", size=self.scale // 2  )

        self.pause = False

    ###
    
    def adjpos(self, pos):
        return (pos[0]+self.viewpos[0], pos[1]+self.viewpos[1])
    
    def inView(self, pos):
        assert type(pos) is tuple
        w = self.viewport[0]
        h = self.viewport[1]
        x = pos[0] - self.viewpos[0]
        y = pos[1] - self.viewpos[1]
        return (x>=0 and x<w) and (y>=0 and y<h)
    
    def inBoundary(self, pos):
        assert type(pos) is tuple
        w = self.size[0]
        h = self.size[0]
        x = pos[0]
        y = pos[1]
        return (x>=0 and x<w) and (y>=0 and y<h)
    
    def makeMark(self, pos):
        assert type(pos) is tuple
        pos = self.adjpos(pos)
        if self.inBoundary(pos):
            self.mark = pos
            
    def finishSelection(self, pos):
        assert type(pos) is tuple
        pos = self.adjpos(pos)
        if self.inBoundary(pos) and self.isMarked():
            pm = self.mark
            self.mark = (-1,-1)
            p1 = ( min(pm[0], pos[0]), min(pm[1], pos[1]) )
            p2 = ( max(pm[0], pos[0]), max(pm[1], pos[1]) )
            self.selection = (p1,p2)
            
            
    def unselect(self):
        self.selection = ((-1,-1),(-1,-1))
        
    def isSelected(self):
        return (self.selection != ((-1,-1),(-1,-1)))
            
    def unmark(self):
        self.mark = (-1,-1)
    
    def isMarked(self):
        return (self.mark != (-1,-1))
    
    def copySelection(self):
        z = self.selection
        if self.isSelected():
            s = []
            x = 0
            y = 1
            for i in range(z[0][x], z[1][x]+1):
                q = []
                for j in range(z[0][y], z[1][y]+1):
                    u = self[i,j].stack
                    if u == []:
                        q.append(None)
                    else:
                        q.append(u[0])
                s.append(q)
            return s
        return []
    
    def clearSelection(self):
        z = self.selection
        if self.isSelected():
            x = 0
            y = 1
            for i in range(z[0][x], z[1][x]+1):
                for j in range(z[0][y], z[1][y]+1):
                    self[i,j].stack = []
    
    def putBlock(self, block=Block, pos=(0,0), rotate=0):
        cell = self[pos]
        if block is not None:
            cell.stack = [ block(cell=cell, pos=pos, rotate=rotate) ]
            return cell.stack[0]
        else:
            cell.stack = []
            return None
    
    def pasteSelection(self, selection, pos, hard=False):
        w = len(selection)
        h = len(selection[0])
        print(pos)
        px = pos[0]
        py = pos[1]
        
        for i in range(w):
            py = pos[1]
            for j in range(h):
                if self.inBoundary((px,py)):
                    b = selection[i][j]
                    if b is not None:
                        self.field[px][py].stack = [self.putBlock(block=b.__class__, pos=(px,py), rotate=b.rotate)]
                        self.field[px][py].stack[0].options = _oc(b.options)
                        self.field[px][py].stack[0].state = _oc(b.state)
                    elif hard is True:
                        self.field[px][py].stack = []
                py += 1
            px += 1
            
                
        
    
    ###


    def shiftViewport(self,amount):
        assert type(amount) in (tuple, list)
        x = max(min(self.viewpos[0] + amount[0], self.size[0]-self.viewport[0]), 0)
        y = max(min(self.viewpos[1] + amount[1], self.size[1]-self.viewport[1]), 0)
        self.viewpos = (x,y)
        
    def shiftViewportRefresh(self,amount):
        self.shiftViewport(amount)
        self.draw(self.scale)
        
    
    
    ###
    
    def pullNeighbors(self, pos):
        x = pos[0]
        y = pos[1]
        r = ((1,0), (0,1), (-1,0), (0,-1))
        z = []
        for i in r:
            mx = x + i[0]
            my = y + i[1]
            if mx>=0 and my>=0 and mx<self.size[0] and my<self.size[1]:
                z.append(self.field[mx][my])
        return z
    
    def getSerial(self):
        r = []
        for i in self.field:
            q = []
            for cell in i:
                z = []
                for s in cell.stack:
                    if type(s) is Beam:
                        z.append({"type":Beam, "color":s.color, "active":s.active})
                    else:
                        z.append({"type":type(s), "state":s.state, "options":s.options, "rotate":s.rotate})
                q.append(z)
            r.append(q)
        return {'size':self.size, 'contents':r}
    
    def tkMainLoop(self):
        self.tkRoot.mainloop()
    
    def tkClear(self):
        self.canvas.delete("all")
        
        
    def fillWithBlock(self, block=Block, posUL=(0,0), posDR=(0,0), rotate=0):
        for i in range(posUL[0],posDR[0]+1):
            for j in range(posUL[1],posDR[1]+1):
                cell = self[i,j]
                cell.stack = [ block(cell=cell, pos=(i,j), rotate=rotate) ]
        
    def removeBlock(self, pos):
        cell = self.field[pos[0]][pos[1]]
        cell.stack = []
        
    def __getitem__(self, x):
        if type(x) is int:
            return self.field[x]
        elif type(x) in (tuple, list):
            return self.field[x[0]][x[1]]
        elif type(x) is dict:
            return self.field[x['x']][x['y']]
        else:
            raise TypeError("Field indices must be int, tuple, list or dict, not "+str(type(x)))
            
    def step(self):
        size = self.size

        for i in range(size[0]):
            for j in range(size[1]):
                cell = self[i,j]
                cell.tick(beam=True, sall=False)

        for i in range(size[0]):
            for j in range(size[1]):
                cell = self[i,j]
                for s in cell.stack:
                    if type(s) is Beam and s.active > 0:
                        s.active -= 1

        for i in range(size[0]):
            for j in range(size[1]):
                cell = self[i,j]
                cell.tick(beam=False, sall=False)

        for i in range(size[0]):
            for j in range(size[1]):
                cell = self[i,j]
                ds = []
                for s in cell.stack:
                    if type(s) is Beam:
                            if ([s.color['r'], s.color['g'], s.color['b']]==[0,0,0]):
                                cell.stack.remove(s)
                            elif s.active == 0:
                                ds.append(s.direction)

                ud = 0
                rl = 0
                if (ds.count("u") + ds.count("d"))>1:
                    ud = ds.count("u") + ds.count("d")
                if (ds.count("r") + ds.count("l"))>1:
                    rl = ds.count("r") + ds.count("l")
                if (ud or rl):
                    for g in cell.stack:
                        if type(g) is Beam and (
                            (ud and (g.direction in ("u", "d")))
                            or (rl and (g.direction in ("r", "l")))
                        ):
                            if g.direction in ("u","d"):
                                ud -= 1
                            else:
                                rl -= 1
                            cell.stack.remove(g)
                
                    
        
                
    def draw(self,scale):
        self.tkClear()
        for j in range(self.viewport[1]+1):
            self.canvas.create_line(16,16+j*scale,16+self.size[0]*scale,16+j*scale, fill="#b3b3b3")
            if j%4 == 0:
                self.canvas.create_text(12,32+j*scale,text=str(j+self.viewpos[1]), font=self.font)
        for i in range(self.viewport[0]+1):
            self.canvas.create_line(16+i*scale,16,16+i*scale,16+self.size[1]*scale, fill="#b3b3b3")
            if i%4 == 0:
                self.canvas.create_text(32+i*scale,12,text=str(i+self.viewpos[0]), font=self.font)
        if self.isMarked():
            mx = self.mark[0] - self.viewpos[0]
            my = self.mark[1] - self.viewpos[1]
            self.canvas.create_rectangle(16+mx*scale, 16+my*scale, 16+(mx+1)*scale, 16+(my+1)*scale, fill="#9198e2", stipple='gray25')
        elif self.isSelected():
            mx = self.selection[0][0] - self.viewpos[0]
            my = self.selection[0][1] - self.viewpos[1]
            px = self.selection[1][0] - self.viewpos[0]
            py = self.selection[1][1] - self.viewpos[1]
            self.canvas.create_rectangle(16+mx*scale, 16+my*scale, 16+(px+1)*scale, 16+(py+1)*scale, fill="#85a7c1", stipple='gray25')

        for j in range(self.viewport[1]):
            for i in range(self.viewport[0]):
                cell = self[i+self.viewpos[0],j+self.viewpos[1]]
                for i in cell.stack:
                    if type(i)!=Beam or i.active==0:
                        i.getGraphics(scale, self.viewpos)
                    
                
    def getText(self, stacklen=False):
        row = [""]*self.size[1]*3
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                cell = self[i,j]
                if stacklen:
                    r = cell.getStackLen()
                else:
                    if cell.stack == []:
                        #r = ("┌   ┐","     ","└   ┘")
                        r = ("     ","  .  ","     ")
                    else:
                        if type(cell.stack[0]) is Beam:
                            beam = cell.stack[0]

                            if beam.direction == 'd':
                                r = ["┏   ┓","     ","┗ ↓ ┛"]
                            elif beam.direction == 'l':
                                r = ["┏   ┓","←    ","┗   ┛"]
                            elif beam.direction == 'r':
                                r = ["┏   ┓","    →","┗   ┛"]
                            elif beam.direction == 'u':
                                r = ["┏ ↑ ┓","     ","┗   ┛"]
                            if len(cell.stack) > 1 and type(cell.stack[1]) is Beam:
                                beam = cell.stack[1]

                                if beam.direction == 'd':
                                    r[2] = "┗ ↓ ┛"
                                elif beam.direction == 'l':
                                    r[1] = "←    "
                                elif beam.direction == 'r':
                                    r[1] = "    →"
                                elif beam.direction == 'u':
                                    r[0] = "┏ ↑ ┓"
                        else:
                            r = cell.stack[0].pretty()

                if i==0:
                    row[j*3] += "  "+r[0]
                    row[j*3+1] += "{:02}".format(j)+r[1]
                    row[j*3+2] += "  "+r[2]
                else:
                    row[j*3] += r[0]
                    row[j*3+1] += r[1]
                    row[j*3+2] += r[2]
        return ["   "+"   ".join(["{:02}".format(p) for p in range(self.size[0])])]+row
    
    def printPretty(self):
        [print(r) for r in self.getText()]
        
    def printStacklen(self):
        [print(r) for r in self.getText(stacklen=True)]
                
                
    
if __name__ == "__main__":
    Z = Field(size = (8,8))
    Z.putBlock(pos=(3,3))
    Z[3,3].stack[0].previewPretty()
    print()
    Z.printPretty()
