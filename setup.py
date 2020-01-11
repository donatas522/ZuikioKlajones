from abc import ABCMeta, abstractproperty
import time
import random
import config as cfg

class Cell:
    def __init__(self):
        self.wall = False
    
    
    def color(self):
        if self.wall:
            return cfg.wall_color
        else:
            return cfg.background_color
    
    
    def load(self, data):
        if data == 'X':
            self.wall = True
        else:
            self.wall = False
    
    
    def __getattr__(self, key):
        if key == 'neighbors':
            opts = [[self.world.get_next_grid(self.x, self.y, direction)] for direction in range(self.world.directions)]
            next_states = tuple(self.world.grid[y][x] for (x, y) in opts)
            return next_states
        raise AttributeError(key)


class Agent:
    def __setattr__(self, key, value):
        if key == 'cell':
            old = self.__dict__.get(key, None)
            if old is not None:
                old.agents.remove(self)
            if value is not None:
                value.agents.append(self)
        self.__dict__[key] = value
    
    
    @abstractproperty # cia reikes grizti
    def cell(self):
        pass #return Cell
    
    
    def go_direction(self, direction):
        target = self.cell.neighbors[direction]
        if getattr(target, 'wall', False):
            #if wall returns only false, rabbit might "decide" to stay near the walls
            #In which way change direction?
            #do-while change direction while cell.wall == true?
            print("hit a wall")
            return False
        self.cell = target
        return True


class World:
    def __init__(self, cell=None, directions=cfg.directions):
        if cell is None:
            cell = Cell
        self.Cell = cell
        #Tkinter implementation
        #self.display = make_display(self)
        self.directions = directions
        #No file name. use from config grid size 
        #self.filename = filename
        
        self.grid = None
        self.dictBackup = None # galimai neprireiks
        self.agents = []
        self.age = 0
        
        self.height = cfg.rows + 2 # + 2 because of walls from both sides
        self.width = cfg.cols + 2 
        #self.get_file_size(filename)
        
        self.image = None
        self.rabbitWin = None
        self.wolfWin = None
        self.resetWorld()
        self.loadWorld()
    
    
    def resetWorld(self):
        self.grid = [[self.make_cell(i, j) for i in range(self.width)] for j in range(self.height)]
        self.dictBackup = [[{} for i2 in range(self.width)] for j2 in range(self.height)] # gali but, kad neprieiks
        self.agents = []
        self.age = 0
    
    
    def make_cell(self, x, y):
        c = self.Cell()
        c.x = x
        c.y = y
        c.world = self
        c.agents = []
        return c
    
    
    def loadWorld(self):
        # Make borders
        for i in range(self.height):
            self.grid[i][0].load('X')
            self.grid[i][self.width - 1].load('X')
        
        for j in range(self.width):
            self.grid[0][j].load('X')
            self.grid[self.height - 1][j].load('X')
    
    
    def get_relative_cell(self, x, y):
        return self.grid[y % self.height][x % self.width]
    
    
    def get_cell(self, x, y):
        return self.grid[y][x]
    
    
    def get_next_grid(self, x, y, dir):
        dx = 0
        dy = 0
        
        if self.directions == 8:
            dx, dy = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)][dir]
        
        x2 = x + dx
        y2 = y + dy
        
        #check for grid violation. Gali but, kad neprireiks ju
        if x2 < 0:
            x2 += self.width
        if y2 < 0:
            y2 += self.height
        if x2 >= self.width:
            x2 -= self.width
        if y2 >= self.height:
            y2 -= self.height
            
        return x2, y2
    
    
    def update(self, rabbit_win=None, wolf_win=None):
        if hasattr(self.Cell, 'update'):
            for a in self.agents: # cia galimai niekada neieina algortimas
                a.update()
            #tkinter update visual
            #self.display.redraw()
        else:
            for a in self.agents:
                old_cell = a.cell
                a.update()             
                #update Tkinter visual
                #if old_cell != a.cell:
                #    self.display.redraw_cell(old_cell.x, old_cell.y)
                #    
                #self.display.redraw_cell(a.cell.x, a.cell.y)
        
        if rabbit_win:
            self.rabbitWin = rabbit_win
        if wolf_win:
            self.wolfWin = wolf_win
        #Tkinter visual    
        #self.display.update()
        self.age += 1
    
    
    def add_agent(self, agent, x=None, y=None, cell=None, direction=None):
        self.agents.append(agent)
        if cell is not None:
            x = cell.x
            y = cell.y
        if x is None:
            x = random.randrange(1, self.width-1)
        if y is None:
            y = random.randrange(1, self.width-1)
        if direction is None:
            direction = random.randrange(self.directions)
        
        agent.cell = self.grid[y][x]
        agent.direction = direction
        agent.world = self
