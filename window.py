
import pygame
import config as cfg
import sys
import time


class Window:
    activated = False
    paused = False
    title = ''
    update_every = 1
    delay = 10
    size = 50
    clock = pygame.time.Clock()
    
    def __init__(self):
        self.world = None
    
    
    def activate(self, size=size):
        self.size = size
        pygame.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 12)
        w = (cfg.cols+2) * size
        h = (cfg.rows+2) * size
        self.screen =  pygame.display.set_mode((w, h))
        self.activated = True
        self.default_color = pygame.Color(cfg.background_color)
        self.redraw()
    
    
    def redraw(self):
        self.screen.fill(self.default_color)
        for row in self.world.grid:
            for cell in row:
                if cell.wall:
                    c = pygame.Color(cfg.wall_color)
                
                if len(cell.agents) > 0:
                    c = self.getColour(cell.agents[0])
                else:
                    c = self.getColour(cell)
                
                if c != self.default_color:
                    try:
                        self.screen.fill(c, (cell.x*self.size, cell.y*self.size, self.size, self.size))
                    except:
                        print('ERROR: invalid color:', c)
                rect = pygame.Rect(cell.x*self.size, cell.y*self.size, self.size, self.size)
                pygame.draw.rect(self.screen, pygame.Color(cfg.wall_color), rect, 2)
    
    
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
        if self.world.age % self.update_every != 0 and not self.paused:
            return
        self.setTitle(self.title)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if self.delay > 0:
                    self.delay -= 1
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                self.delay += 1
                if self.delay > 20:
                    self.delay = 20             
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.pause()
        pygame.display.flip()
        if self.delay > 0:
            time.sleep(self.delay * 0.1)
        #self.clock.tick(60)
    
    
    def pause(self, event=None):
        self.paused = not self.paused
        while self.paused:
            self.update()
    
    
    def setTitle(self, title):
        if not self.activated:
            return
        self.title = title
        title += ' %s' % self.makeTitle(self.world)
        textsurface = self.myfont.render(title, False, self.defaultColour)
        self.screen.blit(textsurface,(0,0))
        #if pygame.display.get_caption()[0] != title:
        #    pygame.display.set_caption(title)
    
    
    def makeTitle(self, world):
        text = 'age: %d\n' % world.age
        extra = []
        if world.rabbit_energy:
            extra.append('energy=%d' % world.rabbit_energy)
        if world.rabbit_starved:
            extra.append('starved=%d' % world.rabbit_starved)
        if world.wolf_win:
            extra.append('wolf_win=%d' % world.wolf_win)      
        if self.paused:
            extra.append('paused')
        if self.update_every != 1:
            extra.append('skip=%d' % self.update_every)
        if self.delay > 0:
            extra.append('delay=%d' % self.delay)

        if len(extra) > 0:
            text += ' [%s]' % ', '.join(extra)
        return text
