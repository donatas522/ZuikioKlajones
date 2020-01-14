import pygame
import config as cfg
import sys

class Window:
    activated = False
    paused = False
    title = ''
    updateEvery = 2**13
    delay = 0
    clock = pygame.time.Clock()
    
    def __init__(self):
        self.world = None
        
    
    def activate(self, size=50):
        self.size = size
        pygame.init()
        w = (cfg.cols+2) * size
        h = (cfg.rows+2) * size
        self.screen =  pygame.display.set_mode((w, h))
        self.activated = True
        self.defaultColour = pygame.Color(cfg.background_color)
        self.redraw()
        
    def redraw(self):
        self.screen.fill(self.defaultColour)
        for row in self.world.grid:
            for cell in row:
                if len(cell.agents) > 0:
                    c = self.getColour(cell.agents[0])
                else:
                    c = self.getColour(cell)
                
                if cell.wall:
                    c = pygame.Color(cfg.wall_color)
                
                if c != self.defaultColour:
                    try:                      
                        self.screen.fill(c, (cell.x*self.size, cell.y*self.size, self.size, self.size))
                    except:
                        print('Error: invalid color:', c)
        
    def getColour(self, obj):
        c = getattr(obj, 'colour', None)
        if c is None:
            c = getattr(obj, 'color', 'white')
        if callable(c):
            c = c()
        if isinstance(c, type(())):
            if isinstance(c[0], type(0.0)):
                c = (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
            return c
        return pygame.Color(c)
    
    def update(self):
        if not self.activated:
            return
        if self.world.age % self.updateEvery != 0 and not self.paused:
            return
        #self.setTitle(self.title)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.QUIT:
                sys.exit()             
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.pause()
        pygame.display.flip()
        self.clock.tick(60)
            
    def pause(self, event=None):
        self.paused = not self.paused
        while self.paused:
            self.update()