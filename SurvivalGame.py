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
wolf_lookcells_UP = []
for i in range(-lookdist, lookdist+1):
    for j in range(0, lookdist+1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            wolf_lookcells_UP.append((i,j))
            
wolf_lookcells_DOWN = []
for i in range(-lookdist, lookdist +1):
    for j in range(-lookdist, 1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            wolf_lookcells_DOWN.append((i,j))
            
wolf_lookcells_RIGHT = []
for i in range(0, lookdist +1):
    for j in range(-lookdist, lookdist +1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            wolf_lookcells_RIGHT.append((i,j))

wolf_lookcells_LEFT = []
for i in range(-lookdist, 1):
    for j in range(-lookdist, lookdist + 1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            wolf_lookcells_LEFT.append((i,j))
                    



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
    
    def update(self):
        pass   

class Wolf(setup.Agent):
    def __init__(self):
        #wolf has 7 directions
        
        self.directions = 7
        self.cell = None #current wolf coordinate in world grid
        self.world = None #World will assign world
        self.score = 0 #times ate rabbit
        self.direction = 1 #UP, current direction wolf is looking. Random at the start?
        self.color = cfg.wolf_color
        self.lastAction = None
        self.lastState = None

    def update(self):
        state = self.calc_state()
        if self.cell == rabbit.cell:
            self.score +=1   
        next_states = self.get_next_states()    
        action = self.choose_action(state, next_states)
        new_cell = next_states[action]
        if new_cell.wall:
            #"reflect from the wall"
            #somehow change self.direction
            #ant transform new_cell according direction
            self.direction = random.randint(1, self.directions) #kaip direction nustatyti?
        self.lastState = self.cell
        self.cell = new_cell
        self.lastAction = action
        
            
        
        
    def choose_action(self, state, next_states):       
        #if rabbit is visible move towards rabbit
        if 3 in state:
            return self.best_action_towards_rabbit(next_states, rabbit.cell) 
        else:
            #rabit is not in sight. Just wander.
            return random.randint(1,2)   
    
    def get_next_states(self):      
        opts = [self.get_cell_for_action(action) for action in range(self.directions)]
        return tuple(self.world.grid[y][x] for x, y in opts)
        
    
    def get_cell_for_action(self, action):
        dx = 0
        dy = 0
        if self.directions == 7:
            #UP
            if self.direction == 1:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(-1, -1), (1, -1), (0, -2), (2, -2), (2, 0), (-2, 0), (-2, -2)][action]
            #RIGHT
            if self.direction == 2:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(1, -1), (1, 1), (2, 0), (2, 2), (0, 2), (0, -2), (2, -2)][action]
            #DOWN
            if self.direction == 3:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(1, 1), (-1, 1), (0, 2), (-2, 2), (-2, 0), (2, 0), (2, 2)][action]
            if self.direction == 4:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(-1, 1), (-1, -1), (-2, 0), (-2, -2), (0, -2), (0, 2), (-2, 2)][action]
            
        x2 = self.cell.x + dx
        y2 = self.cell.y + dy
        
        #Wolf walking by 2 distance might "jump" over wall
        #So if coordinate exceeds boundaries set them to boundaries.
        #check for grid violation. Gali but, kad neprireiks ju
        if x2 < 0:
            x2 = 0
        if y2 < 0:
            y2 = 0
        if x2 >= self.world.width:
            x2 = self.world.width
        if y2 >= self.world.height:
            y2 = self.world.height
            
        return x2, y2
        
            
    
    def calc_state(self):
        #3 - rabbit
        #2 - apple
        #1 - wall
        #0 - empty cell
        def cellValue(cell):
            if rabbit.cell is not None and (cell.x == rabbit.cell.x and
                                            cell.y == rabbit.cell.y):
                return 3         
            elif apple.cell is not None and (cell.x == apple.cell.x and
                                            cell.y == apple.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0
        
        if (self.direction == 1):    
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + j, self.cell.y + i)) for i,j in wolf_lookcells_UP])
        if (self.direction == 2):    
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + j, self.cell.y + i)) for i,j in wolf_lookcells_RIGHT])
        if (self.direction == 3):    
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + j, self.cell.y + i)) for i,j in wolf_lookcells_DOWN])
        if (self.direction == 4):    
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + j, self.cell.y + i)) for i,j in wolf_lookcells_LEFT])
        
        
    def best_action_towards_rabbit(self, next_states, target):
        if self.cell == target:
            return
        best = None
        i = 0
        for n in next_states:
            i += 1
            if n == target:
                best = i
                break
            dist = (n.x - target.x) ** 2 + (n.y - target.y) ** 2
            if best is None or bestDist > dist:
                best = i
                bestDist = dist
        
        return best 
        
        
        
        
        
        
        
              

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
        
    
    
    def update(self):
        #calculate the state of the surround cells (field of view)
        state = self.calc_state()
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
        state = self.calc_state()
        print(state)
        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action
        #here should work 'neighbors' property which updates cell coordinates in world
        self.go_direction(action)
                    
        
    def calc_state(self):
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
world.add_agent(wolf, direction= 3)
world.add_agent(rabbit)
world.update()   