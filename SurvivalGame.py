import random
import qlearn
import setup
import config as cfg


#this is rabbit state or field of view it will be updated
#according rabbit positions in grid.
lookdist = cfg.lookdist
rabbit_lookcells = []
for i in range(-lookdist,lookdist+1):
    for j in range(-lookdist,lookdist+1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            rabbit_lookcells.append((i,j))

#Good field of view.
#But wolf ca rotate also! this is direction UP
wolf_lookcells = []
for i in range(-lookdist, lookdist+1):
    for j in range(0, lookdist+1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            wolf_lookcells.append((i,j))            



def moveFourCellsTowardsCenter(cell):
    #not implemented
    #need to create new cell object and assign x y in world
    return setup.Cell()

def pickRandomLocationWithAverage(cell):
    #not implemented
    #need to create new cell object and assign x y in world 
    return setup.Cell()

def pickRandomLocation():
    while 1:
        x = random.randrange(world.width)
        y = random.randrange(world.height)
        cell = world.get_cell(x, y)
        if not (cell.wall or len(cell.agents) > 0):
            return cell

class Apple(setup.Agent):
    def __init__(self):
        self.cell = None
    
    @property
    def cell(self):
        return self.cell
    

class Wolf(setup.Agent):
    def __init__(self):
        self.cell = None
        self.score = 0
    
    def update(self):
        pass
        
        
        
              

class Rabbit(setup.Agent):
    def __init__(self):
        self.ai = None
        self.ai = qlearn.QLearn(actions=range(cfg.directions))
        self.cell = None
        #rabbit does not rotate!!
        self.direction = None
        self.world = None
        self.lastState = None
        self.lastAction = None
        self.color = cfg.rabbit_color
        self.energy = cfg.M
        self.eaten = 0
        self.starved = 0
        print('rabbit initialized.')
        
    @property
    def cell(self):
        return self.cell
    
    def update(self):
        #calculate the state of the surround cells (field of view)
        state = self.calcState()
        #because of movement reward -1 by default will follow
        reward = cfg.move
        
        #observe the reward and update the Q-value
        if self.cell == wolf.cell:
            self.eaten += 1
            reward = cfg.eaten_by_wolf
            if self.lastState is not None:
                self.ai.learnQ(self.lastState, self.lastAction, state, reward)
            
            self.energy -= cfg.eaten_by_wolf
            if self.energy <= 0:
                #reset last state or reset only when energy <0?
                self.lastState = None
                self.cell = pickRandomLocation()
                return
    
            #rabbit survived enough energy left. Move rabbit towards center
            self.cell = moveFourCellsTowardsCenter(self.cell)
                 
            
        if self.cell == apple.cell:
            self.energy += cfg.eat_carrot
            reward = cfg.eat_carrot
            if self.lastState is not None:
                self.ai.learnQ(self.lastState, self.lastAction, state, reward)
            apple.cell = pickRandomLocationWithAverage(apple.cell)
            
        if self.energy < 0:
            self.starved += 1
            self.lastState = None
            pickRandomLocation()
            return
            
        # Choose a new action and execute it
        # What state after reward observation?
        state = self.calcState()
        print(state)
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action
        #here should work 'neighbors' property which updates cell coordinates in world
        self.go_direction(action)
                    
        
    
    def calcState(self):
        #3 - wolf
        #2 - apple
        #1 - wall
        #0 - empty cell
        def cellValue(cell):
            if wolf.cell is not None and (cell.x == wolf.cell.x and
                                          cell.y == wolf.cell.y):
                return 3         
            elif apple.cell is not None and (cell.x == apple.cell.x and
                                            cell.y == apple.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0
        
        return tuple([cellValue(self.world.get_relative_cell(self.cell.x + j, self.cell.y + i)) for i,j in rabbit_lookcells])
        
    
world = setup.World()    
wolf = Wolf()
rabbit = Rabbit()
apple = Apple()
world.add_agent(apple, cell=pickRandomLocation())
world.add_agent(wolf)
world.add_agent(rabbit)   