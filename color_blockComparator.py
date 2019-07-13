import photons
rotd = photons.rotateDir
dirDef = photons.dirDef
ltod = photons.listToDictColor


class main(photons.Block):
    defaultState = {"active":True, "state":"main", "colorA":photons.emptyColor(), "colorB":photons.emptyColor()}
    """
    states:
        main    -- empty cell, nothing inside
        keep   -- a beam had entered the cell

    """
    defaultOptions = {
            "absdif":{
                    "name":"Absolute difference",
                    "type":"bool",
                    "value": True
                }
            }
            
    blockName = "Comparator"
    opts_r = {'fill':'#FF0000', 'width':2}
    opts_b = {'fill':'#0000FF', 'width':2}
    
    boxGraphics = [   
            ("line", (0,0, 1,0)),
            ("line", (1,0, 1,1)),
            ("line", (1,1, 0,1)),
            ("line", (0,1, 0,0)),
            ("line", (0.5,0.5,  0.5,0), opts_r),
            ("line", (0.5,0.5,  0,0.5), opts_r),
            ("line", (0.5,0.5,  0.5,1), opts_b),
            ("line", (0.7,0.5,  0.9,0.5)),
            ("line", (0.9,0.5,  0.7,0.3)),
            ("line", (0.9,0.5,  0.7,0.7))
                ]
    
    def getGraphicsList(self):
        a = main.boxGraphics.copy()
        if self.getOption("absdif") in ("1", True, 1, "yes", "Ja-ja"):
            a.append( ("oval", (0.3,0.3,  0.7,0.7)) )
        else:
            a.append( ("rectangle", (0.3,0.3,  0.7,0.7)) )
        return a
    
    def stack(self, z): 
        dirIn = rotd('r', self.rotate)
        
        dirA = rotd('d', self.rotate)
        dirB = rotd('u', self.rotate)
        
        rt = [("remove", z)]
    
        if self.state["state"] == "keep":
            self.state["state"] = "main"
            h = dirDef[dirIn]
            newPos = (self.pos[0]+h[0], self.pos[1]+h[1])

            c1 = self.state["colorA"]
            c2 = self.state["colorB"]
            if self.getOption("absdif") in ("1", "true", "True", "aye"):
                d = [abs(c1[x] - c2[x]) for x in "rgb"]
            else:
                d = [max(0,c1[x] - c2[x]) for x in "rgb"]
            clr = ltod(d)
            
            rt.append( ("add",[     
                    
                                    photons.Beam(   
                                        cell = self.cell.field[newPos],
                                        field = self.cell.field,
                                        direction = dirIn,
                                        color = clr,
                                        pos = newPos,
                                        active = 2
                                    )
                                            
                        ]) )
            self.state["colorA"] = photons.emptyColor()
            self.state["colorB"] = photons.emptyColor()
                
                
        if z != []: 
            for beam in z:
                if beam.direction in (dirA, dirIn):
                    self.state["colorA"] = beam.color
                    self.state["state"] = "keep"
                elif beam.direction == dirB:
                    self.state["colorB"] = beam.color
                    self.state["state"] = "keep"
                    
        return rt
