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
    
    blockName = "Negator" 
    opts_polygon = {'width':2, 'outline':'black', 'fill':''}
    opts_line = {'width':2}
    
    boxGraphics = [   
            ("line", (0,0, 1,0)),
            ("line", (1,0, 1,1)),
            ("line", (1,1, 0,1)),
            ("line", (0,1, 0,0)),
            ("line", (0,0.5, 0.2,0.5), opts_line),
            ("polygon", (0.2,0.2, 0.2,0.8, 0.5,0.5), opts_polygon),
            ("oval",(0.5,0.35, 0.8,0.65)),
            ("line", (0.8,0.5, 1,0.5), opts_line)
                  ]

    def getGraphicsList(self):
        return main.boxGraphics
    
    def stack(self, z): 
        dirIn = rotd('r', self.rotate)
        
        
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
                                        color = ltod( [15-self.state["colorCaptive"]['r'], 15-self.state["colorCaptive"]['g'], 15-self.state["colorCaptive"]['b'] ] ),
                                        pos = newPos,
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