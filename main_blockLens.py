import photons
rotd = photons.rotateDir
dirDef = photons.dirDef

class main(photons.Block):
    
    """
    states:
        off
        offKeep -- off, has a beam inside
        on
        onKeep  -- on,  has a beam inside
     
       B
     ╔═*═╗
   2 ║ ? → A
     ╚═══╝
       1
    """
    blockName = "Lens"
    defaultState = {"active":True, "state":"off", "ticks":1, "colorCaptive":photons.emptyColor()}
    
    defaultOptions = {
            "cap":{
                    "name":"Gate capacitance",
                    "type":"integer",
                    "value": 0
                },
            "invert":{
                    "name":"Invert",
                    "type":"bool",
                    "value": False
                }
            }

    boxGraphics = {
                ("off",False):
                    [
                        ("line", (0,0,1,0)),
                        ("line", (1,0,1,1)),
                        ("line", (1,1,0,1)),
                        ("line", (0,1,0,0)),
                        ("line", (0.5,0,0.5,0.5), {'arrow': 'last', 'width': 2}),
                        ("line", (0.5,0.5,1,0.5), {'width': 3}),
                        ("line", (0.5,0.5,0.5,1), {'width': 3})
                    ],
                ("on",False):
                    [
                        ("line", (0,0,1,0)),
                        ("line", (1,0,1,1)),
                        ("line", (1,1,0,1)),
                        ("line", (0,1,0,0)),
                        ("line", (0.5,0,0.5,0.5), {'arrow': 'last', 'width': 2}),
                        ("line", (0.5,0.5,0,0.5), {'width': 3}),
                        ("line", (0.5,0.5,0.5,1), {'width': 3})
                    ],
                ("on",True):
                    [
                        ("line", (0,0,1,0)),
                        ("line", (1,0,1,1)),
                        ("line", (1,1,0,1)),
                        ("line", (0,1,0,0)),
                        
                        ("oval", (0.4,0.25,0.6,0.5)),
                        
                        ("line", (0.5,0,0.5,0.25), {'width': 2}),
                        ("line", (0.5,0.5,1,0.5), {'width': 3}),
                        ("line", (0.5,0.5,0.5,1), {'width': 3})
                    ],
                ("off",True):
                    [
                        ("line", (0,0,1,0)),
                        ("line", (1,0,1,1)),
                        ("line", (1,1,0,1)),
                        ("line", (0,1,0,0)),
                        
                        ("oval", (0.4,0.25,0.6,0.5)),
                        
                        ("line", (0.5,0,0.5,0.25), {'width': 2}),
                        ("line", (0.5,0.5,0,0.5), {'width': 3}),
                        ("line", (0.5,0.5,0.5,1), {'width': 3})
                    ],
            }
    
    def getGraphicsList(self):
        return main.boxGraphics[(self.state["state"].replace("Keep",""), self.getOption("invert"))]

    def __repr__(self):
        if "off" in self.state["state"]:
            return "[  LS off]"
        else:
            return "[  LS on ]"
        
    pictures = {
                0: ("╔═*═╗","← ? →","╚═══╝"),
                1: ("╔═↑═╗","║ ? *","╚═↓═╝"),
                2: ("╔═══╗","← ? →","╚═*═╝"),
                3: ("╔═↑═╗","* ? ║","╚═↓═╝")
            }
    
    
    
    def stack(self,z):
        dirIn1 = rotd('u', self.rotate)
        if ("off" in self.state["state"]) != self.getOption("invert"):
            dirIn2 = rotd('r', self.rotate)
        else:
            dirIn2 = rotd('l', self.rotate)
        dirInB = rotd('d', self.rotate)
        
        on = False
        keep = None
        
        for i in z:
            if i.direction == dirInB:
                on = True
            if i.direction in (dirIn1, dirIn2):
                keep = i.color
                
            
        if not on:
            if ("on" in self.state["state"]):
                self.state["ticks"] -= 1
                if self.state["ticks"] <= 0:
                    self.state["state"] = self.state["state"].replace("on","off")
        else:
            self.state["ticks"] = self.getOption("cap")
            self.state["state"] = self.state["state"].replace("off","on")
            
                
        
        if "Keep" in self.state["state"]:
            self.state["state"] = self.state["state"].replace("Keep","")
            h = dirDef[dirIn2]
            newPos = (self.pos[0]+h[0], self.pos[1]+h[1])
            u =    [
                    ("add",[photons.Beam(   
                                                cell = self.cell.field[newPos],
                                                field = self.cell.field,
                                                direction = dirIn2,
                                                color = self.state["colorCaptive"],
                                                pos = newPos,
                                                active = 1
                                            )]
                     
                     )
                    ]
        else:
            u = []
        
        if not (keep is None):
            self.state["colorCaptive"] = keep
            self.state["state"] = self.state["state"] + "Keep"
            
        u.append(("remove",z))
            
        return u
    
    
    
    def pretty(self):
        r = list(main.pictures[self.rotate])
        right = (("on" in self.state["state"]) == self.getOption("invert"))
        left  = not right
        if (right and self.rotate==0) or (left and self.rotate==2):
            r[1] = r[1].replace("←","║")
        if (left and self.rotate==0) or (right and self.rotate==2):
            r[1] = r[1].replace("→","║")
        if (right and self.rotate==1) or (left and self.rotate==3):
            r[0] = r[0].replace("↑","═")
        if (left and self.rotate==1) or (right and self.rotate==3):
            r[2] = r[2].replace("↓","═")
            
        a = self.getOption("cap")
        if a>9:
            a = "C"
        else:
            a = str(a)
            
        if self.getOption("invert"):
            r = [i.replace("*","o") for i in r]
            
        r[1] = r[1].replace("?",a)
        return r
