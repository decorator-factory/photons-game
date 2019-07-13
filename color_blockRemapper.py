import photons
rotd = photons.rotateDir
dirDef = photons.dirDef
ltod = photons.listToDictColor
cofl = photons.colorFromLetter


class main(photons.Block):
    defaultState = {"active":True, "state":"main", "colorCaptive":photons.emptyColor()}
    """
    states:
        main    -- empty cell, nothing inside
        keep   -- a beam had entered the cell

    """
    blockName = "Remapper"
    defaultOptions = {
            "from":{
                    "name":"Map from",
                    "type":"colorLetter",
                    "value": "r"
                },
            "to":{
                    "name":"Map onto",
                    "type":"colorLetter",
                    "value": "g"
                }
            }
    
    
    boxGraphics = [   
            ("line", (0,0, 1,0)),
            ("line", (1,0, 1,1)),
            ("line", (1,1, 0,1)),
            ("line", (0,1, 0,0)),
            ("line", (0,0.5, 0.2,0.5)),
            ("line", (0.5,0.3, 0.5,0.7)),
            ("line", (0.4,0.5, 0.5,0.5)),
            ("line", (0.8,0.5, 1,0.5))
                  ]

    def getGraphicsList(self):
        a = main.boxGraphics.copy()
        
        opts_polygon1 = {'fill':cofl(self.getOption("from")), 'outline':'black'}
        opts_polygon2 = {'fill':cofl(self.getOption("to")), 'outline':'black'}
        
        a.append(  ("polygon", (0.2,0.3, 0.2,0.7, 0.4,0.5), opts_polygon1)  )
        a.append(  ("polygon", (0.6,0.3, 0.6,0.7, 0.8,0.5), opts_polygon2)  )
        
        return a
    
    def stack(self, z): 
        dirIn = rotd('r', self.rotate)
        
        
        rt = ("remove", z)
        if self.state["state"] == "keep":
            self.state["state"] = "main"
            cfrom = self.getOption("from")
            cto = self.getOption("to")
            h = dirDef[dirIn]
            cval = self.state["colorCaptive"][cfrom]
            newcol = photons.emptyColor()
            newcol[cto] = cval
            
            newPos = (self.pos[0]+h[0], self.pos[1]+h[1])
            rt = [("add",[     
                    
                                    photons.Beam(   
                                        cell = self.cell.field[newPos],
                                        field = self.cell.field,
                                        direction = dirIn,
                                        color = newcol,
                                        pos = newPos,
                                        active = 1
                                    ),
                                            
                        ]),
                                            
                                    
                ("remove",z)]
                
                
        if z != []: 
            beam = z[0]
            if beam.direction == dirIn:
                self.state["colorCaptive"] = beam.color
                self.state["state"] = "keep"
                    
        return rt