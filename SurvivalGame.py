
import random
import qlearn
import setup
import config as cfg


# Rabbit state (field of view; 40 cells in coordinates relative to rabbits position)
# It will be updated according to rabbit's positions in the grid (for instance, field of view should be smaller when near the wall)
rabbit_lookdist = cfg.rabbit_lookdist
rabbit_lookcells = []
for i in range(-rabbit_lookdist, rabbit_lookdist + 1):
    for j in range(-rabbit_lookdist, rabbit_lookdist + 1):
        if (abs(i) + abs(j) <= rabbit_lookdist) and (i != 0 or j != 0):
            rabbit_lookcells.append((i,j))

# Wolf's field of view. Wolf can rotate to 4 directions: up, down, right, left. Each field of view has 20 cells
wolf_lookdist = cfg.wolf_lookdist
wolf_lookcells_UP = []
for i in range(-wolf_lookdist, wolf_lookdist + 1):
    for j in range(-wolf_lookdist, 1): # y asis i apacia, bent jau pagal get_cell_for_action
        if (abs(i) + abs(j) <= wolf_lookdist) and (i != 0 or j != 0):
            wolf_lookcells_UP.append((i,j))

wolf_lookcells_DOWN = []
for i in range(-wolf_lookdist, wolf_lookdist + 1):
    for j in range(0, wolf_lookdist + 1): # y asis i apacia, bent jau pagal get_cell_for_action
        if (abs(i) + abs(j) <= wolf_lookdist) and (i != 0 or j != 0):
            wolf_lookcells_DOWN.append((i,j))

wolf_lookcells_RIGHT = []
for i in range(0, wolf_lookdist + 1):
    for j in range(-wolf_lookdist, wolf_lookdist + 1):
        if (abs(i) + abs(j) <= wolf_lookdist) and (i != 0 or j != 0):
            wolf_lookcells_RIGHT.append((i,j))

wolf_lookcells_LEFT = []
for i in range(-wolf_lookdist, 1):
    for j in range(-wolf_lookdist, wolf_lookdist + 1):
        if (abs(i) + abs(j) <= wolf_lookdist) and (i != 0 or j != 0):
            wolf_lookcells_LEFT.append((i,j))


def moveTowardsCenter(agent, verbose=False):
    dist = cfg.move_towards_center # move towards center per 4 cells
    # locate center cell (chose one of the two for even dimensions)
    width = agent.world.width
    height = agent.world.height
    if (width % 2 == 0):
        center_x = width/2 - 1
    else:
        center_x = (width - 1)/2
    if (height % 2 == 0):
        center_y = height/2 - 1
    else:
        center_y = (height - 1)/2
    center_x = int(center_x)
    center_y = int(center_y)
    
    if verbose:
        print('World dimensions: {rows} rows by {cols} columns (without walls)'.format(rows=height-2, cols=width-2))
        print('Moving distance towards center cell after encounter with wolf: {0}'.format(dist))
        print('Center cell coords: ({x},{y})'.format(x=center_x, y=center_y))
        print('Agent\'s cell coords before moving: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
    
    # cells that can reach the center cell with dist=4 moves or less will always be moved to the center cell
    proximity_grid = [(i + center_x, j + center_y) for i in range(-dist, dist+1) for j in range(-dist, dist+1)]
    if (agent.cell.x, agent.cell.y) in proximity_grid:
        agent.cell = agent.world.grid[center_y][center_x] # ar cia irgi validus kreipimasis?
        if verbose:
            print('Agent is in the proximity of the center cell')
            print('Agent\'s cell coords after moving: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
        return
    # for cells not in proximity, search for the closest cell near the center cell (nepabaigta)
    else:
        if verbose:
            print('Agent is not in the proximity of the center cell. Calculating agent\'s new cell coords')
        dx = agent.cell.x - center_x
        dy = agent.cell.y - center_y
        if (dx!=0 and dy!=0): # general line. Cia butu galima funkcija parasyt, maziau eiluciu butu, bet kol kas palieku
            k = dy/dx
            a = k
            b = -1
            c = center_y - k*center_x
            norm = 1 / (a**2 + b**2)**0.5
            if dx>0 and dy>0:
                proximity_ring_quarter = [(i + agent.cell.x, -dist + agent.cell.y) for i in range(-(dist-1), 1)] + [(-dist + agent.cell.x, j + agent.cell.y) for j in range(-(dist-1), 1)] + [(-dist + agent.cell.x, -dist + agent.cell.y)]
                distances = [norm * abs(a*x + b*y + c) for (x,y) in proximity_ring_quarter]
                (x,y) = proximity_ring_quarter[min(range(len(distances)), key=distances.__getitem__)]
                agent.cell = agent.world.grid[y][x]
                if verbose:
                    print(proximity_ring_quarter)
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return
            elif dx<0 and dy>0:
                proximity_ring_quarter = [(i + agent.cell.x, -dist + agent.cell.y) for i in range(dist)] + [(dist + agent.cell.x, j + agent.cell.y) for j in range(-(dist-1), 1)] + [(dist + agent.cell.x, -dist + agent.cell.y)]
                distances = [norm * abs(a*x + b*y + c) for (x,y) in proximity_ring_quarter]
                (x,y) = proximity_ring_quarter[min(range(len(distances)), key=distances.__getitem__)]
                agent.cell = agent.world.grid[y][x]
                if verbose:
                    print(proximity_ring_quarter)
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return
            elif dx<0 and dy<0:
                proximity_ring_quarter = [(i + agent.cell.x, dist + agent.cell.y) for i in range(dist)] + [(dist + agent.cell.x, j + agent.cell.y) for j in range(dist)] + [(dist + agent.cell.x, dist + agent.cell.y)]
                distances = [norm * abs(a*x + b*y + c) for (x,y) in proximity_ring_quarter]
                (x,y) = proximity_ring_quarter[min(range(len(distances)), key=distances.__getitem__)]
                agent.cell = agent.world.grid[y][x]
                if verbose:
                    print(proximity_ring_quarter)
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return
            else: # dx>0 and dy<0
                proximity_ring_quarter = [(i + agent.cell.x, dist + agent.cell.y) for i in range(-(dist-1), 1)] + [(-dist + agent.cell.x, j + agent.cell.y) for j in range(dist)] + [(-dist + agent.cell.x, dist + agent.cell.y)]
                distances = [norm * abs(a*x + b*y + c) for (x,y) in proximity_ring_quarter]
                (x,y) = proximity_ring_quarter[min(range(len(distances)), key=distances.__getitem__)]
                agent.cell = agent.world.grid[y][x]
                if verbose:
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return
        
        elif (dx==0 and dy!=0): # vertical line
            if dy > 0:
                agent.cell = agent.world.grid[agent.cell.y - dist][center_x]
                if verbose:
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return
            else: # dy < 0
                agent.cell = agent.world.grid[agent.cell.y + dist][center_x]
                if verbose:
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return
        
        else: # horizontal line
            if dx > 0:
                agent.cell = agent.world.grid[center_y][agent.cell.x - dist]
                if verbose:
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return
            else: # dx < 0
                agent.cell = agent.world.grid[center_y][agent.cell.x + dist]
                if verbose:
                    print('Agent\'s new coords: ({x},{y})'.format(x=agent.cell.x, y=agent.cell.y))
                return


def pickRandomLocationWithAverage(cell):
    #not implemented
    #need to create new cell object and assign x y in world 
    return setup.Cell()



class Apple(setup.Agent):
    def __init__(self):
        self.cell = None
        self.color = cfg.carrot_color
    
    def update(self):
        pass



class Wolf(setup.Agent):
    def __init__(self):
        name = self.__class__.__name__ # uztenka ir tiesiog name='Wolf', but whatever
        self.directions = cfg.class_directions[name] # wolf has 4 directions: up, right, down, left
        self.actions = cfg.class_actions[name] # wolf has 7 actions in each direction
        self.cell = None # current wolf coordinate in the world grid, invoked by world.addAgent()
        self.direction = None # class World will assign direction when world.addAgent() is invoked
        self.world = None # class World will assign world when world.addAgent() is invoked
        self.score = 0 # number of times the rabbit was eaten
        self.color = cfg.wolf_color
        self.last_cell = None
        self.last_action = None
    
    
    def update(self):
        state = self.calcState()
        if self.cell == rabbit.cell: # cia gal reiketu lyginti ne pacius objektus, bet ju atributus x ir y? cia rabbit objektas, esantis main'e?
            self.score += 1 # jei triusis suvalgomas, game over ir reload world. Gal reiketu pabaigoje tikrinti
        next_states = self.getNextStates()
        action = self.chooseAction(state, next_states)
        new_cell = next_states[action]
        while new_cell.wall:         
            if action in (0, 5, 6):
                self.direction = (int) (self.direction - 1) % self.directions
            if action in (1, 3, 4):
                self.direction = (int) (self.direction + 1) % self.directions                
            if action == 2:
                self.direction = (int) (self.direction + self.directions/2) % self.directions
            next_states = self.getNextStates()
            #reflected_action = action.index((x,y))
            new_cell = next_states[action]
            #"reflect from the wall"
            #somehow change self.direction
            #and transform new_cell according to direction
            #self.direction = random.randrange(self.directions) #kaip direction nustatyti? kol kas random
        self.last_cell = self.cell
        self.cell = new_cell
        self.last_action = action
    
    
    def chooseAction(self, state, next_states):
        if 3 in state: # if rabbit is visible, move towards rabbit
            return self.bestActionTowardsRabbit(next_states, rabbit.cell) # rabbit objektas is main?
        else:
            if self.last_action != 0 or self.last_action != 1:
                return 1
            if self.last_action == 0 or self.last_action == 1:
                return self.last_action
            return random.randint(0,1) # rabit is not in sight, just wander
    
    
    def getNextStates(self):
        opts = [self.getCellForAction(action) for action in range(self.actions)]
        return tuple(self.world.grid[y][x] for (x,y) in opts)
    
    
    def getCellForAction(self, action):
        dx = 0
        dy = 0
        if self.actions == 7:
            #UP
            if self.direction == 0:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(-1, -1), (1, -1), (0, -2), (2, -2), (2, 0), (-2, 0), (-2, -2)][action]
            #RIGHT
            if self.direction == 1:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(1, -1), (1, 1), (2, 0), (2, 2), (0, 2), (0, -2), (2, -2)][action]
            #DOWN
            if self.direction == 2:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(1, 1), (-1, 1), (0, 2), (-2, 2), (-2, 0), (2, 0), (2, 2)][action]
            #LEFT
            if self.direction == 3:
                #Kaire istrizai, Desine istrizai, UP, UR, R, L, UL
                dx, dy = [(-1, 1), (-1, -1), (-2, 0), (-2, -2), (0, -2), (0, 2), (-2, 2)][action]
        
        x2 = self.cell.x + dx
        y2 = self.cell.y + dy
        
        # Wolf chasing rabbit by 2 distance might "jump" over wall
        # So if coordinate exceeds boundaries set them to boundaries
        # 0 yra wall index, self.world.width-1 irgi wall index, todel juos irgi reikia iskaityt
        # cia dar reikes sugrizti
        if x2 <= 0:
            x2 = 0
        if y2 <= 0:
            y2 = 0
        if x2 >= self.world.width - 1:
            x2 = self.world.width - 1
        if y2 >= self.world.height - 1:
            y2 = self.world.height - 1
        
        return (x2, y2)
    
    
    def calcState(self):
        #3 - rabbit
        #2 - apple
        #1 - wall
        #0 - empty cell
        
        def cellValue(cell):
            # cia konkreciam objektui rabbit, kuris sukurtas main'e?
            if rabbit.cell is not None and (cell.x == rabbit.cell.x and cell.y == rabbit.cell.y):
                return 3
            # cia lygina tik vienam objektui apple? reikia kazka daryti, kad lygintu visiems apple objektams
            elif apple.cell is not None and (cell.x == apple.cell.x and cell.y == apple.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0
        
        # cia man rodos blogai, nes kai vilkas yra prie sienos, tai uz sienos ribu esancios field of view cells persikelia
        # i grido apacia del getRelativeCell veikimo, o ju isvis neturetu buti -- field of view turetu sumazeti.
        # Bet jauciu darysim kitaip,
        # paliksim fiksuoto dydzio field of view, tik reikes toms cells, kurios yra uz grid ribu, uzdeti kazkoki skaliara, kuris
        # rodytu, kad ta cell yra uz ribu. Panasiai kaip su calc_state, kai skirtingoms cells pagal tai, kas joje stovi,
        # priskiriama kazkokia verte. Ir siaip pagalvojus, tai triusio field of view yra 40 elementu dydzio. field of view
        # skirtingu konfiguraciju yra belekiek daug, tai nemanau, kad Q-Learning kazka ismoks, nes algoritmas vos ne kiekviena
        # karta susidurs su nauja busena (state). busenu dydis turi buti pakankamai mazas, kad Q-Learning sudarytu Q-table,
        # kas ir yra triusio isgyvenimo strategija.
        if (self.direction == 0):
            return tuple(cellValue(self.world.getCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_UP)
        if (self.direction == 1):
            return tuple(cellValue(self.world.getCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_RIGHT)
        if (self.direction == 2):
            return tuple(cellValue(self.world.getCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_DOWN)
        if (self.direction == 3):
            return tuple(cellValue(self.world.getCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_LEFT)
        
        
    def bestActionTowardsRabbit(self, next_states, target):
        if self.cell == target: # ar cia butinas sitas tikrinimas? update pradzioje patikrinam, o iki chooseAction jokio action vilkas neatlieka
            return
        best = None
        i = 2
        bestDist = 1000
        #discard states when rabbit is not in sight
        for n in next_states[2:]:
            if n == target: # cia gal irgi tikrinti ne Cell tipo objektus tarpusavyje, bet ju atributus x ir y?
                best = i
                break
            dist = (n.x - target.x) ** 2 + (n.y - target.y) ** 2
            # del next_states strukturos, ne visai simetriskai vilkas sokines, galesim del sitos padiskutuot
            # cia reikes is esmes kazkokio random proceso kai kurioms field of view celems
            if best is None or dist < bestDist:
                best = i
                bestDist = dist
            i += 1
        
        return best



class Rabbit(setup.Agent):
    def __init__(self):
        name = self.__class__.__name__
        self.directions = cfg.class_directions[name] # rabbit has 1 directions (does not rotate)
        self.actions = cfg.class_actions[name] # rabbit has 8 actions in each direction
        self.ai = None
        self.ai = qlearn.QLearn(actions=range(self.actions))
        self.cell = None
        self.direction = None
        self.world = None
        self.last_state = None
        self.last_action = None
        self.color = cfg.rabbit_color
        self.energy = cfg.N
        self.M = cfg.eat_apple
        self.wolf_encounter = cfg.eaten_by_wolf
        self.eaten = 0
        self.starved = 0
        self.direction_vectors = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        print('rabbit initialized.')
    
    
    def update(self):
        #calculate the state of the surround cells (field of view)
        state = self.calcState()
        #because of movement reward -1 by default will follow
        reward = cfg.move
        
        #observe the reward and update the Q-value
        if self.cell == wolf.last_cell: # gal geriau lyginti x ir y?
            self.eaten += 1
            reward = self.wolf_encounter
            if self.last_state is not None:
                self.ai.learnQ(self.last_state, self.last_action, state, reward)
            
            self.energy -= self.wolf_encounter
            if self.energy <= 0:
                #reset last state or reset only when energy <0?
                self.last_state = None
                self.cell = self.world.pickRandomLocation()
                return
    
            #rabbit survived, enough energy left. Move rabbit towards center
            self.cell = self.world.pickRandomLocation()# moveTowardsCenter(self)
               
        elif self.cell == apple.cell: # gal geriau lyginti x ir y?
            self.energy += self.M
            reward = self.M
            if self.last_state is not None:
                self.ai.learnQ(self.last_state, self.last_action, state, reward)
            #apple.cell = self.world.pickRandomLocationWithAverage(apple.cell)
        
        else:
            self.energy += reward
            if self.last_state is not None:
                self.ai.learnQ(self.last_state, self.last_action, state, reward)
        
        
        if self.energy <= 0:
            self.starved += 1
            self.last_state = None
            self.cell = self.world.pickRandomLocation()
            self.energy = cfg.N
            return
        
        
        # Choose a new action and execute it
        # What state after reward observation?
        state = self.calcState()
        print(state)
        action = self.ai.chooseAction(state)
        self.last_state = state
        self.last_action = action
        #here should work 'neighbors' property which updates cell coordinates in world
        self.goDirection(action)
        
    # Rabbit judejimas
    # perkelti i Rabbit klase?
    def goDirection(self, target_direction):
        new_direction = target_direction
        target_cell = self.getNextStates()[new_direction]
        if getattr(target_cell, 'wall', False): # o negalima ___ if target_cell.wall == False: ? ar butu skirtumas?
            x = self.direction_vectors[target_direction][0]
            y = self.direction_vectors[target_direction][1]
            if target_cell.x == (0 or self.world.width-1):
               x = -x
            if target_cell.y == (0 or self.world.height-1):
               y = -y
            new_direction = self.direction_vectors.index((x,y))
            self.cell = self.getNextStates()[new_direction]
            print("Rabbit hit a wall.")
            return False
            
            #if wall returns only false, rabbit might "decide" to stay near the walls
            #In which way change direction?
            #do-while change direction while cell.wall == true?
            # klausimas, ar rabbit aplamai rinktusi krypti i siena? jei jau taip atsitiktu, cia padaryta paprasta inversija sienos atzvilgiu, veikia ir kampui. Cia uztenka vieno perskaiciavimo, t.y. naujai krypciai new_direction tikrinimo nereikia, nes jos kryptimi cell visada bus laisva
        self.cell = self.getNextStates()[new_direction]
        return True
    
    def getNextStates(self):
        opts = [self.getCellForAction(action) for action in range(self.actions)]
        return tuple(self.world.grid[y][x] for (x,y) in opts)
    
    def getCellForAction(self, action):
        dx = 0
        dy = 0
        
        if self.actions == 8:
            dx, dy = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)][action]
        
        x2 = self.cell.x + dx
        y2 = self.cell.y + dy
        
        # check for grid violation. Gali but, kad neprireiks ju
        if x2 < 0:
            x2 += self.world.width
        if y2 < 0:
            y2 += self.world.height
        if x2 >= self.world.width:
            x2 -= self.world.width
        if y2 >= self.world.height:
            y2 -= self.world.height
        
        return (x2, y2)
                    
        
    def calcState(self):
        #3 - wolf
        #2 - apple
        #1 - wall
        #0 - empty cell
        def cellValue(cell):
            # tokie pat klausimai, kaip ir vilko funkcijos atveju
            if wolf.cell is not None and (cell.x == wolf.last_cell.x and cell.y == wolf.last_cell.y):
                return 3 
            elif apple.cell is not None and (cell.x == apple.cell.x and cell.y == apple.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0
        
        return tuple(cellValue(self.world.getCell(self.cell.x + i, self.cell.y + j)) for (i,j) in rabbit_lookcells)



world = setup.World(cell=setup.Cell)

apple = Apple() # turi buti multiple Apple objektai
wolf = Wolf() # gali buti multiple Wolf objektai
rabbit = Rabbit()


# svarbi agentu pakrovimo tvarka, nes pagal ja paskui updatinasi agentu busenos
world.addAgent(apple, cell=world.pickRandomLocation())
world.addAgent(wolf, cell=world.pickRandomLocation())
world.addAgent(rabbit, cell=world.pickRandomLocation()) # tegul visi agentai pakraunami ant neuzimtu langeliu

#world.UIdraw = False
while 1:
    world.updateWorld(rabbit.energy, rabbit.eaten, rabbit.starved)
