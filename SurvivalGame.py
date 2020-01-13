
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


def moveTowardsCenter(agent):
    dist = cfg.move_towards_center # move towards center per 4 cells
    # locate center cell (chose one of the two for even dimensions)
    width = agent.world.width # ar galima taip kreiptis? Agent tipo objektas agent turi property world, so..?
    # man klausimas kyla toks: jei as kazka padarau klases World objektui world tiesiogiai, tai ar uzsiupdatina tokiu objektu,
    # kaip pvz rabbit ar wolf, property world? nes jei tai yra tiesiog nuoroda i objekta world, tai kaip ir turetu uzsiupdatint.
    # P.S.: paskaiciau nete, tai ale validu, bet still palieku kaip klausima
    height = agent.world.height
    if (width % 2 == 0):
        center_x = width/2 - 1
    else:
        center_x = (width - 1)/2
    if (height % 2 == 0):
        center_y = height/2 - 1
    else:
        center_y = (height - 1)/2
    
    # cells that can reach the center cell with dist=4 moves or less will always be moved to the center cell
    proximity_grid = [(i + center_x, j + center_y) for i in range(-dist, dist+1) for j in range(-dist, dist+1)]
    if (agent.cell.x, agent.cell.y) in proximity_grid:
        agent.cell = agent.world.grid[center_y][center_x] # ar cia irgi validus kreipimasis?
        return
    # for cells not in proximity, search for the closest cell near the center cell (nepabaigta)
    else:
        dx = center_x - agent.cell.x
        dy = center_y - agent.cell.y
        k = dy/dx
        
        
        
        if (dx!=0 and dy!=0): # general line
            if dx>0 and dy>0:
                
            elif dx<0 and dy>0:
                
            elif dx<0 and dy<0:
                
            else: # dx>0 and dy<0
                
            proximity_ring = [(i + agent.cell.x, j + agent.cell.y) for i in range(-dist, dist+1) for j in range(-dist, dist+1)]
        elif (dx==0 and dy!=0): # vertical line
            if dy > 0:
                agent.cell = agent.world.grid[agent.cell.y + dist][center_x]
                return
            else: # dy < 0
                agent.cell = agent.world.grid[agent.cell.y - dist][center_x]
                return
        else: # horizontal line
            if dx > 0:
                agent.cell = agent.world.grid[center_y][agent.cell.x + dist]
                return
            else: # dx < 0
                agent.cell = agent.world.grid[center_y][agent.cell.x - dist]
                return
    #need to create new cell object and assign x y in world


def pickRandomLocationWithAverage(cell):
    #not implemented
    #need to create new cell object and assign x y in world 
    return setup.Cell()


def pickRandomLocation(world): # tikriausiai nereikia tikrinimo, ar siena, nes sienos indekso niekada negaus. Gal perkelti i World?
    while 1:
        x = random.randrange(1, world.width-1)
        y = random.randrange(1, world.height-1)
        cell = world.getCell(x, y)
        if not (cell.wall or len(cell.agents) > 0): # chosen cell has to be a non-wall and has to be empty (no agents)
            return cell



class Apple(setup.Agent):
    def __init__(self):
        self.cell = None
    
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
        self.last_state = None
        self.last_action = None
    
    
    def update(self):
        state = self.calcState()
        if self.cell == rabbit.cell: # cia gal reiketu lyginti ne pacius objektus, bet ju atributus x ir y? cia rabbit objektas, esantis main'e?
            self.score += 1 # jei triusis suvalgomas, game over ir reload world. Gal reiketu pabaigoje tikrinti
        next_states = self.getNextStates()
        action = self.chooseAction(state, next_states)
        new_cell = next_states[action]
        if new_cell.wall:
            #"reflect from the wall"
            #somehow change self.direction
            #and transform new_cell according to direction
            self.direction = random.randrange(self.directions) #kaip direction nustatyti? kol kas random
        self.last_state = self.cell
        self.cell = new_cell
        self.last_action = action
    
    
    def chooseAction(self, state, next_states):
        if 3 in state: # if rabbit is visible, move towards rabbit
            return self.bestActionTowardsRabbit(next_states, rabbit.cell) # rabbit objektas is main?
        else:
            return random.randint(1,2) # rabit is not in sight, just wander
    
    
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
            x2 = 1
        if y2 <= 0:
            y2 = 1
        if x2 >= self.world.width - 1:
            x2 = self.world.width - 2
        if y2 >= self.world.height - 1:
            y2 = self.world.height - 2
        
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
            return tuple(cellValue(self.world.getRelativeCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_UP)
        if (self.direction == 1):
            return tuple(cellValue(self.world.getRelativeCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_RIGHT)
        if (self.direction == 2):
            return tuple(cellValue(self.world.getRelativeCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_DOWN)
        if (self.direction == 3):
            return tuple(cellValue(self.world.getRelativeCell(self.cell.x + i, self.cell.y + j)) for (i,j) in wolf_lookcells_LEFT)
        
        
    def bestActionTowardsRabbit(self, next_states, target):
        if self.cell == target: # ar cia butinas sitas tikrinimas? update pradzioje patikrinam, o iki chooseAction jokio action vilkas neatlieka
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
        print('rabbit initialized.')
    
    
    def update(self):
        #calculate the state of the surround cells (field of view)
        state = self.calcState()
        #because of movement reward -1 by default will follow
        reward = cfg.move
        
        #observe the reward and update the Q-value
        if self.cell == wolf.cell: # gal geriau lyginti x ir y?
            self.eaten += 1
            reward = self.wolf_encounter
            if self.last_state is not None:
                self.ai.learnQ(self.last_state, self.last_action, state, reward)
            
            self.energy -= self.wolf_encounter
            if self.energy <= 0:
                #reset last state or reset only when energy <0?
                self.last_state = None
                self.cell = pickRandomLocation(agent.world)
                return
    
            #rabbit survived, enough energy left. Move rabbit towards center
            self.cell = moveTowardsCenter(self)
        
        
        if self.cell == apple.cell: # gal geriau lyginti x ir y?
            self.energy += self.M
            reward = self.M
            if self.last_state is not None:
                self.ai.learnQ(self.last_state, self.last_action, state, reward)
            apple.cell = pickRandomLocationWithAverage(apple.cell)
        
        
        if self.energy <= 0:
            self.starved += 1
            self.last_state = None
            self.cell = pickRandomLocation(agent.world)
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
                    
        
    def calcState(self):
        #3 - wolf
        #2 - apple
        #1 - wall
        #0 - empty cell
        def cellValue(cell):
            # tokie pat klausimai, kaip ir vilko funkcijos atveju
            if wolf.cell is not None and (cell.x == wolf.cell.x and cell.y == wolf.cell.y):
                return 3 
            elif apple.cell is not None and (cell.x == apple.cell.x and cell.y == apple.cell.y):
                return 2
            else:
                return 1 if cell.wall else 0
        
        return tuple(cellValue(self.world.getRelativeCell(self.cell.x + i, self.cell.y + j)) for (i,j) in rabbit_lookcells)



world = setup.World(cell=setup.Cell)

apple = Apple() # turi buti multiple Apple objektai
wolf = Wolf() # gali buti multiple Wolf objektai
rabbit = Rabbit()


# svarbi agentu pakrovimo tvarka, nes pagal ja paskui updatinasi agentu busenos
world.addAgent(apple, cell=pickRandomLocation(world))
world.addAgent(wolf, cell=pickRandomLocation(world))
world.addAgent(rabbit, cell=pickRandomLocation(world)) # tegul visi agentai pakraunami ant neuzimtu langeliu

world.updateWorld()
