import photons

class main(photons.Block):
    def stack(self, z): # Remove everything in the stack above
        return ("remove", z)
    def __repr__(self):
        return "[  SD  ]"
    def pretty(self):
        return ("╔═══╗","║   ║","╚═══╝")
    
    blockName = "Solid"
    
    boxGraphics = [
            ("line", (0,0,1,0)),
            ("line", (1,0,1,1)),
            ("line", (1,1,0,1)),
            ("line", (0,1,0,0)),
            ("line", (0,0,1,1)),
            ("line", (0,1,1,0))
            ]
    
    def getGraphicsList(self):
        return main.boxGraphics