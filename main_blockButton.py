import photons
rotd = photons.rotateDir
dirDef = photons.dirDef

class main(photons.Block):
    defaultOptions = {"color":{"name":"Color","type":"color","value":photons.emptyColor()}}
    """
    states:
        main
        on
        
    ╔═══╗
    ║ L═╢ 1
    ╚═══╝
      
    """
    blockName = "Button"
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
        clr = photons.listToTkColor(cl3)
        opt_oval = {'fill': clr}
        opt_line = {'fill': clr, 'width': 2}
        a += [
                ("oval", (0.2,0.2,0.8,0.8)),
                ("oval", (0,0.4,0.4,0.6), opt_oval),
                ("line", (0.1,0.5,1,0.5), opt_line)
                
            ]
        return a
    
    def clickMouse(self):
        self.state["state"] = "main" if self.state["state"] == "on" else "on"
    
    def stack(self, z):
        if self.state["state"] != "on":
            return ("remove",z)

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
                    color = photons.fixColor(self.getOption("color")),
                    pos = newPos,
                    active = 1
                  )
                ]
               ),

               (
                "remove",
                z
               )
                ]
                 
    pictures = {
            0: ("╔═══╗","║ L─╢","╚═══╝"),
            1: ("╔═══╗","║ L ║","╚═╧═╝"),
            2: ("╔═══╗","╟─L ║","╚═══╝"),
            3: ("╔═╤═╗","║ L ║","╚═══╝")
            }
    
    def pretty(self):
        return main.pictures[self.rotate]
