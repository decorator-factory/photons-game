import photons
rotd = photons.rotateDir
dirDef = photons.dirDef



class main(photons.Block):
    defaultState = {"active":True, "state":"main", "colorCaptive":photons.emptyColor()}
    """
    states:
        main    -- empty cell, nothing inside
        from1   -- a beam had entered the cell in port 1 or 3
        from2   -- a beam had entered the cell in port 1
        
    ╔═══╗
  3 ╟─┬─╢ 1
    ╚═╧═╝
      2
    """
    blockName = "Scatterer"
    boxGraphics = [
            ("line", (0,0,1,0)),
            ("line", (1,0,0.5,1)),
            ("line", (0.5,1,0,0))
            ]
    
    def getGraphicsList(self):
        a = main.boxGraphics.copy()
        z = self.state["colorCaptive"]
        cl3 = [(z['r']+1)*16-1,(z['g']+1)*16-1,(z['b']+1)*16-1]
        clr = photons.listToTkColor(cl3)
        opt_oval = {'fill': clr, 'outline': clr}
        opt_line = {'fill': clr, 'width': 4}
        if photons.colorIsNull(self.state["colorCaptive"]) is False:
            if self.state["state"] == "from1":
                a += [
                        ("line", (0.5,0.5,0.5,1), opt_line),
                        ("oval", (0.35,0.35,0.65,0.65), opt_oval),
                ]
            elif self.state["state"] == "from2":
                a += [
                        ("line", (0,0.5,0.25,0.5), opt_line),
                        ("line", (1,0.5,0.75,0.5), opt_line),
                ]
            
        return a
    
    def stack(self, z): 
        dirIn1 = rotd('l', self.rotate)
        dirIn2 = rotd('u', self.rotate)
        dirIn3 = rotd('r', self.rotate)
        
        dirOut1 = rotd('r', self.rotate)
        dirOut2 = rotd('d', self.rotate)
        dirOut3 = rotd('l', self.rotate)
        
        rt = ("remove", z)
        if self.state["state"] == "from2":
            self.state["state"] = "main"
            h1 = dirDef[dirOut1]
            h2 = dirDef[dirOut3]
            newPos1 = (self.pos[0]+h1[0], self.pos[1]+h1[1])
            newPos2 = (self.pos[0]+h2[0], self.pos[1]+h2[1])
            rt = [("add",[     
                    
                                    photons.Beam(   
                                        cell = self.cell.field[newPos2],
                                        field = self.cell.field,
                                        direction = dirOut3,
                                        color = self.state["colorCaptive"],
                                        pos = newPos2,
                                        active = 2
                                    ),
                            
                                    photons.Beam(   
                                        cell = self.cell.field[newPos1],
                                        field = self.cell.field,
                                        direction = dirOut1,
                                        color = self.state["colorCaptive"],
                                        pos = newPos1,
                                        active = 2
                                    )])
                ,("remove",z)]
        elif self.state["state"] == "from1":
                    self.state["state"] = "main"
                    h = dirDef[dirOut2]
                    newPos = (self.pos[0]+h[0], self.pos[1]+h[1])
                    rt = [("add",[     photons.Beam(   
                                                cell = self.cell.field[newPos],
                                                field = self.cell.field,
                                                direction = dirOut2,
                                                color = self.state["colorCaptive"],
                                                pos = newPos,
                                                active = 2
                                            )]),
                            ("remove", z)
                            
                            ]
                
                
        if z != []: 
            for beam in z:
                if beam.direction in (dirIn1, dirIn3):
                    self.state["colorCaptive"] = beam.color
                    self.state["state"] = "from1"
                elif beam.direction == dirIn2:
                    self.state["colorCaptive"] = beam.color
                    self.state["state"] = "from2"
                    
        return rt
    def __repr__(self):
        return "[  SD  ]"
    
    pictures = {
            0: ("╔═══╗","╟─┬─╢","╚═╧═╝"),
            1: ("╔═╤═╗","╟─┤ ║","╚═╧═╝"),
            2: ("╔═╤═╗","╟─┴─╢","╚═══╝"),
            3: ("╔═╤═╗","║ ├─╢","╚═╧═╝")
            }
    
    def pretty(self):
        x = main.pictures[self.rotate]
        if self.state["state"] != "main":
            x = [i.replace(" ","X") for i in x]
        #x = [i.replace(" ",str(len(self.cell.stack))) for i in x]
        return x