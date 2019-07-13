import photons
rotd = photons.rotateDir
dirDef = photons.dirDef
ltod = photons.listToDictColor


class main(photons.Block):
    defaultState = {"active":True, "state":"main", "colorR":0, "colorG":0, "colorB":0}
    """
    states:
        main    -- empty cell, nothing inside
        keep   -- a beam had entered the cell

    """
    
    boxGraphics = [   
            ("line", (0,0, 1,0)),
            ("line", (1,0, 1,1)),
            ("line", (1,1, 0,1)),
            ("line", (0,1, 0,0)),
            ("line", (0.5,0.5,  0.5,0), {'fill':'#FF0000', 'width':2}),
            ("line", (0.5,0.5,  0,0.5), {'fill':'#00FF00', 'width':2}),
            ("line", (0.5,0.5,  0.5,1), {'fill':'#0000FF', 'width':2}),
            ("line", (0.5,0.5,  0.9,0.5)),
            ("line", (0.9,0.5,  0.7,0.3)),
            ("line", (0.9,0.5,  0.7,0.7))
                ]

    blockName = "Coupler"
    
    def getGraphicsList(self):
        return main.boxGraphics
    
    def stack(self, z): 
        dirIn = rotd('r', self.rotate)
        
        dirR = rotd('d', self.rotate)
        dirG = rotd('r', self.rotate)
        dirB = rotd('u', self.rotate)
        
        rt = ("remove", z)
    
        if self.state["state"] == "keep":
            self.state["state"] = "main"
            
            h = dirDef[dirIn]
            newPos = (self.pos[0]+h[0], self.pos[1]+h[1])
            rt = [("add",[     
                    
                                    photons.Beam(   
                                        cell = self.cell.field[newPos],
                                        field = self.cell.field,
                                        direction = dirIn,
                                        color = ltod( [self.state['colorR'], self.state['colorG'], self.state['colorB'] ] ),
                                        pos = newPos,
                                        active = 1
                                    )
                                            
                        ]),
                                            
                                    
                ("remove",z)]
                
                
        if z != []: 
            for beam in z:
                if beam.direction == dirR:
                    self.state["colorR"] = beam.color['r']
                    self.state["state"] = "keep"
                elif beam.direction == dirG:
                    self.state["colorG"] = beam.color['g']
                    self.state["state"] = "keep"
                elif beam.direction == dirB:
                    self.state["colorB"] = beam.color['b']
                    self.state["state"] = "keep"
                    
        return rt