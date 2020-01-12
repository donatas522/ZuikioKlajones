import random
import qlearn
import setup
import config as cfg


# Rabbit state (field of view; 40 cells in general, but can be smaller)
# It will be updated according to rabbit's positions in the grid (for instance, field of view is smaller when near the wall)
lookdist = cfg.lookdist
rabbit_lookcells = []
for i in range(-lookdist, lookdist + 1):
    for j in range(-lookdist, lookdist + 1):
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            rabbit_lookcells.append((i,j))

# Wolf's field of view. Wolf can rotate to 4 directions: up, down, right, left. Each field of view has a maximum of 20 cells
wolf_lookcells_UP = []
for i in range(-lookdist, lookdist + 1):
    for j in range(-lookdist, 1): # y asis i apacia, bent jau pagal get_cell_for_action
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            wolf_lookcells_UP.append((i,j))

wolf_lookcells_DOWN = []
for i in range(-lookdist, lookdist + 1):
    for j in range(0, lookdist + 1): # y asis i apacia, bent jau pagal get_cell_for_action
        if (abs(i) + abs(j) <= lookdist) and (i != 0 or j != 0):
            wolf_lookcells_DOWN.append((i,j))

wolf_lookcells_RIGHT = []
for i in range(0, lookdist + 1):
    for j in range(-lookdist, lookdist + 1):
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
        x = random.randrange(1, world.width - 1)
        y = random.randrange(1, world.height - 1)
        cell = world.get_cell(x, y)
        if not (cell.wall or len(cell.agents) > 0): # chosen cell has to be a non-wall and has to be empty (no agents)
            return cell


class Apple(setup.Agent):
    def __init__(self):
        self.cell = None
    
    def update(self):
        pass

class Wolf(setup.Agent):
    def __init__(self):
        self.directions = 4 # wolf has 4 directions: up, right, down, left
        self.direction = 1 # UP, current direction wolf is looking. Random at the start? Yep, random
        self.actions = 7 # wolf has 7 actions in each direction
        self.cell = None # current wolf coordinate in the world grid
        self.world = None # class World will assign world
        self.score = 0 # times ate rabbit
        self.color = cfg.wolf_color
        self.lastAction = None
        self.lastState = None
    
    def update(self):
        state = self.calc_state()
        if self.cell == rabbit.cell: # cia gal reiketu lyginti ne pacius objektus, bet ju atributus x ir y? cia rabbit objektas, esantis main'e?
            self.score += 1 # jei triusis suvalgomas, game over ir reload world
        next_states = self.get_next_states()
        action = self.choose_action(state, next_states)
        new_cell = next_states[action]
        if new_cell.wall:
            #"reflect from the wall"
            #somehow change self.direction
            #and transform new_cell according to direction
            self.direction = random.randint(1, self.directions) #kaip direction nustatyti?
        self.lastState = self.cell
        self.cell = new_cell
        self.lastAction = action
        
    
    
    
    def choose_action(self, state, next_states):
        # if rabbit is visible, move towards rabbit
        if 3 in state:
            return self.best_action_towards_rabbit(next_states, rabbit.cell) # rabbit objektas is main?
        else:
            # rabit is not in sight, just wander
            return random.randint(1,2)
    
    def get_next_states(self):
        opts = [self.get_cell_for_action(action) for action in range(self.actions)]
        return tuple(self.world.grid[y][x] for (x, y) in opts)
    
    
    def get_cell_for_action(self, action):
        dx = 0
        dy = 0
        if self.actions == 7:
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
            #LEFT
            if self.direction == 4:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(-1, 1), (-1, -1), (-2, 0), (-2, -2), (0, -2), (0, 2), (-2, 2)][action]
        
        x2 = self.cell.x + dx
        y2 = self.cell.y + dy
        
        # Wolf chasing rabbit by 2 distance might "jump" over wall
        # So if coordinate exceeds boundaries set them to boundaries
        # 0 yra wall index, self.world.width-1 irgi wall index, todel juos irgi reikia iskaityt
        if x2 <= 0:
            x2 = 1
        if y2 <= 0:
            y2 = 1
        if x2 >= self.world.width - 1:
            x2 = self.world.width - 2
        if y2 >= self.world.height - 1:
            y2 = self.world.height - 2
        
        return x2, y2
    
    
    
    def calc_state(self):
        #3 - rabbit
        #2 - apple
        #1 - wall
        #0 - empty cell
        
        def cellValue(cell):
            # cia konkreciam objektui rabbit, kuris sukurtas main'e?
            if rabbit.cell is not None and (cell.x == rabbit.cell.x and
                                            cell.y == rabbit.cell.y):
                return 3
            # cia lygina tik vienam objektui apple? reikia kazka daryti, kad lygintu visiems apple objektams
            elif apple.cell is not None and (cell.x == apple.cell.x and
                                            cell.y == apple.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0
        
        # cia man rodos blogai, nes kai vilkas yra prie sienos, tai uz sienos ribu esancios field of view cells persikelia i grido apacia
        # del get_relative_cell veikimo, o ju isvis neturetu buti -- field of view turetu sumazeti
        if (self.direction == 1):
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_UP])
        if (self.direction == 2):
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_RIGHT])
        if (self.direction == 3):
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_DOWN])
        if (self.direction == 4):
            return tuple([cellValue(self.world.get_relative_cell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_LEFT])
        
        
    def best_action_towards_rabbit(self, next_states, target):
        if self.cell == target: # ar cia butinas sitas tikrinimas? update pradzioje patikrinam, o iki choose_action jokio action vilkas neatlieka
            return
        best = None
        i = 0
        bestDist = 1000
        for n in next_states:
            i += 1
            if n == target: # cia gal irgi tikrinti ne Cell tipo objektus tarpusavyje, bet ju atributus x ir y?
                best = i
                break
            dist = (n.x - target.x) ** 2 + (n.y - target.y) ** 2
            # del next_states strukturos, ne visai simetriskai vilkas sokines, galesim del sitos padiskutuot
            # cia reikes is esmes kazkokio random proceso kai kurioms field of view celems
            if best is None or dist < bestDist:
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
            if wolf.cell is not None and (cell.x == wolf.cell.x and # tokie pat klausimai, kaip ir vilko funkcijos atveju
                                          cell.y == wolf.cell.y):
                return 3 
            elif apple.cell is not None and (cell.x == apple.cell.x and
                                            cell.y == apple.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0
        
        return tuple([cellValue(self.world.get_relative_cell(self.cell.x + i, self.cell.y + j)) for (i,j) in rabbit_lookcells])
        
    
world = setup.World()    
wolf = Wolf()
rabbit = Rabbit()
apple = Apple()
world.add_agent(apple, cell=pickRandomLocation())
world.add_agent(wolf, direction= 3)
world.add_agent(rabbit)
world.update()   
