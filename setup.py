
from abc import ABCMeta, abstractproperty
import time
import random
import window
import config as cfg



def makeDisplay(world):
    d = window.Window()
    d.world = world
    return d


class Cell:
    def __init__(self):
        self.wall = False

    
    def color(self):
        if self.wall:
            return cfg.wall_color
        else:
            return cfg.background_color
    
    def makeWall(self):
        self.wall = True
    


class Agent:
    # this allows to follow the occupation of each cell with all agents
    def __setattr__(self, key, value):
        if key == 'cell':
            old = self.__dict__.get(key, None)
            if old is not None:
                old.agents.remove(self)
            if value is not None:
                value.agents.append(self)
        self.__dict__[key] = value



class World:
    def __init__(self, cell=None):
        if cell is None:
            cell = Cell
        self.Cell = cell      
        # pygame
        self.display = makeDisplay(self)
        self.UIdraw = True    
        self.grid = None
        self.agents = []
        self.age = 0
        self.directions = cfg.directions # neigbouring cells
        self.class_directions = cfg.class_directions # directions for each class
        self.class_actions = cfg.class_actions # actions for each class
        self.class_lookdist = cfg.class_lookdist # lookdist for each class
        
        self.height = cfg.rows + 2 # + 2 because of walls from both sides
        self.width = cfg.cols + 2 
        
        self.rabbit_win = None
        self.wolf_win = None
        self.rabbit_energy = None
        self.rabbit_starved = None
        self.rabbit_age = 0
        
        self.resetWorld()
        self.loadWorld()
        self.display.activate(size=cfg.cell_size)
    
    
    def resetWorld(self):
        self.grid = [[self.makeCell(i, j) for i in range(self.width)] for j in range(self.height)]
        self.agents = []
        self.age = 0
    
    
    def makeCell(self, x, y):
        cell = self.Cell()
        cell.x = x
        cell.y = y
        cell.world = self # each cell has a reference to the same World instance
        cell.agents = [] # each cell has a list of references to different Agent instances, which are on the cell
        return cell
    
    
    def loadWorld(self):
        # make borders
        for j in range(self.height):
            self.grid[j][0].makeWall()
            self.grid[j][self.width - 1].makeWall()
        
        for i in range(self.width):
            self.grid[0][i].makeWall()
            self.grid[self.height-1][i].makeWall()
    
    def getCell(self, x, y):
        w = self.width
        h = self.height
      
        if x < 0: x = 0
        elif x > w-1: x = w-1
        else: pass # 0 <= x <= w-1
        
        if y < 0: y = 0
        elif y > h-1: y = h-1
        else: pass # 0 <= y <= h-1
        
        return self.grid[y][x]
    
    
    def updateWorld(self, rabbit_energy=None, wolf_win=None, rabbit_starved=None, rabbit_age=None):
        #update each agent in world
        for a in self.agents:
            a.update()
        if self.UIdraw:
            self.display.redraw()
    
        if rabbit_energy:
            self.rabbit_energy = rabbit_energy
        if wolf_win:
            self.wolf_win = wolf_win
        if rabbit_starved:
            self.rabbit_starved = rabbit_starved
        if rabbit_age:
            self.rabbit_age = rabbit_age   
        if self.UIdraw:
            self.display.update()
        self.age += 1
    
    
    def addAgent(self, agent, x=None, y=None, cell=None, direction=None):
        self.agents.append(agent) # list of agents in the world
        if cell is not None:
            x = cell.x
            y = cell.y
        if x is None:
            x = random.randrange(1, self.width-1)
        if y is None:
            y = random.randrange(1, self.width-1)
        if direction is None:
            direction = self.pickRandomDirection(agent)
        
        agent.cell = self.grid[y][x] # cell object of the agent
        agent.direction = direction
        agent.world = self # each agent has a reference to the same World instance
    
    
    # direction choice depends on the class of the agent
    def pickRandomDirection(self, agent):
        class_name = agent.__class__.__name__
        directions = self.class_directions[class_name]
        direction = random.randrange(directions)
        return direction
    
    
    def pickRandomLocation(self):
        while True:
            x = random.randrange(1, self.width-1)
            y = random.randrange(1, self.height-1)
            cell = self.getCell(x, y)
            if not (cell.wall or len(cell.agents) > 0): # chosen cell has to be a non-wall and has to be empty (no agents)
                return cell
