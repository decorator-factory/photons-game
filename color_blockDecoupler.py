import photons
rotd = photons.rotateDir
dirDef = photons.dirDef
ltod = photons.listToDictColor


class main(photons.Block):
    defaultState = {"active":True, "state":"main", "colorCaptive":photons.emptyColor()}
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
            ("line", (0.5,0.5,  1,0.5), {'fill':'#00FF00', 'width':2}),
            ("line", (0.5,0.5,  0.5,1), {'fill':'#0000FF', 'width':2}),
            ("line", (0,0.5,  0.4,0.5)),
            ("line", (0.4,0.5,  0.2,0.3)),
            ("line", (0.4,0.5,  0.2,0.7))
                  ]

    blockName = "Decoupler"
    
    def getGraphicsList(self):
        return main.boxGraphics
    
    def stack(self, z): 
        dirIn = rotd('r', self.rotate)
        
        dirR = rotd('u', self.rotate)
        dirG = rotd('r', self.rotate)
        dirB = rotd('d', self.rotate)
        
        
        rt = ("remove", z)
        if self.state["state"] == "keep":
            self.state["state"] = "main"
            hr = dirDef[dirR]
            hg = dirDef[dirG]
            hb = dirDef[dirB]
            newPosR = (self.pos[0]+hr[0], self.pos[1]+hr[1])
            newPosG = (self.pos[0]+hg[0], self.pos[1]+hg[1])
            newPosB = (self.pos[0]+hb[0], self.pos[1]+hb[1])
            rt = [("add",[     
                    
                                    photons.Beam(   
                                        cell = self.cell.field[newPosR],
                                        field = self.cell.field,
                                        direction = dirR,
                                        color = ltod( [self.state["colorCaptive"]['r'], 0, 0 ] ),
                                        pos = newPosR,
                                        active = 2
                                    ),
                            
                                    photons.Beam(   
                                        cell = self.cell.field[newPosG],
                                        field = self.cell.field,
                                        direction = dirG,
                                        color = ltod( [ 0, self.state["colorCaptive"]['g'], 0 ] ),
                                        pos = newPosR,
                                        active = 2
                                    ),
                                            
                                    photons.Beam(   
                                        cell = self.cell.field[newPosB],
                                        field = self.cell.field,
                                        direction = dirB,
                                        color = ltod( [0, 0, self.state["colorCaptive"]['b']] ),
                                        pos = newPosB,
                                        active = 2
                                    ),
                                            
                        ]),
                                            
                                    
                ("remove",z)]
                
                
        if z != []: 
            beam = z[0]
            if beam.direction == dirIn:
                self.state["colorCaptive"] = beam.color
                self.state["state"] = "keep"
                    
        return rt