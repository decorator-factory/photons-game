import photons
rotd = photons.rotateDir
dirDef = photons.dirDef

class main(photons.Block):
    defaultState = {"active":True, "state":"main", "ticks":0}
    defaultOptions = {
            "color":{
                    "name":"Color",
                    "type":"color",
                    "value":photons.emptyColor()
                    },
            "lowtime":{
                    "name":"Low time",
                    "type":"integer",
                    "value": 7
                },
            "hightime":{
                    "name":"High time",
                    "type":"integer",
                    "value": 3
                }
            }
    """
    states:
        main
        on
        
    ╔═══╗
    ║ G═╢ 1
    ╚═══╝
      
    """
    
    blockName = "Generator"
    boxGraphics = [
        ("line", (0,0,1,0)),
        ("line", (1,0,1,1)),
        ("line", (1,1,0,1)),
        ("line", (0,1,0,0)),
        ]
    
    def getGraphicsList(self):
        a = main.boxGraphics.copy()
        z = self.getOption("color")
        cl3 = [(z['r']+1)*16-1,(z['g']+1)*16-1,(z['b']+1)*16-1]
        if self.state["state"] == "main":
            cl3 = [x//2 for x in cl3]
        clr = photons.listToTkColor(cl3)
        opt_line = {'fill': clr, 'width': 2}
        a += [
                ("line", (0,0.5,0.2,0.5), opt_line),
                ("line", (0.2,0.5,0.2,0.3), opt_line),
                ("line", (0.2,0.3,0.4,0.3), opt_line),
                ("line", (0.4,0.3,0.4,0.7), opt_line),
                ("line", (0.4,0.7,0.6,0.7), opt_line),
                ("line", (0.6,0.7,0.6,0.5), opt_line),
                ("line", (0.6,0.5,1,0.5), opt_line),
                
                ("line", (1,0.5,0.8,0.3), opt_line),
                ("line", (1,0.5,0.8,0.7), opt_line)
                
            ]
        return a
    
    def stack(self, z):
        self.state["ticks"] += 1
        if self.state["state"] == "on":
            if self.state["ticks"] >= self.getOption("hightime"):
                self.state["state"] = "main"
                self.state["ticks"] = 0
            dirOut = rotd('r', self.rotate)
            h = dirDef[dirOut]
            newPos = (self.pos[0]+h[0], self.pos[1]+h[1])
            #self.state["state"] = "main"
            return [
                    
                    (
                     "add",
                     [photons.Beam(   
                        cell = self.cell.field[newPos],
                        field = self.cell.field,
                        direction = dirOut,
                        color = photons.fixColor(self.options["color"]["value"]),
                        pos = newPos,
                        active = 2
                      )
                    ]
                   ),
                     
                   (
                    "remove",
                    z
                   )
                    ]
        else:
            if self.state["ticks"] >= self.getOption("lowtime"):
                self.state["state"] = "on"
                self.state["ticks"] = 0
            return [("remove", z)]
                 
    pictures = {
            0: ("╔═══╗","║ G─╢","╚═══╝"),
            1: ("╔═══╗","║ G ║","╚═╧═╝"),
            2: ("╔═══╗","╟─G ║","╚═══╝"),
            3: ("╔═╤═╗","║ G ║","╚═══╝")
            }
    
    def pretty(self):
        return main.pictures[self.rotate]
