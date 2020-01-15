#always survice:
#rows,cols = 7, M=5 apples_number = 25
#survive rows x cols age
#rows,cols = 13, M=8 apples_number = 25 

# ----- World Settings -----
rows = 7 # world rows #13
cols = 7 # world columns #13
cell_size = 70
N = rows * cols # number of world cells
M = 5 # energy from apple #8
apples_number = 7 #20
wolves_number = 1
directions = 8 # neigbouring cells
background_color = '#FFFFFF' # white
wall_color = '#000000' # black
rabbit_color = '#0000FF' # blue
wolf_color = '#FF0000' # red
carrot_color = '#00FF00' # green


# ----- Agent Settings -----
# none of these parameters can be less than 1
move_towards_center = 4

apple_directions = 1
apple_actions = 1
apple_lookdist = 1

rabbit_directions = 1
rabbit_actions = 8
rabbit_lookdist = 4


wolf_directions = 4
wolf_actions = 7
wolf_lookdist = 4

class_directions = {'Apple': apple_directions, 'Rabbit': rabbit_directions, 'Wolf': wolf_directions} # directions for each class
class_actions = {'Apple': apple_actions, 'Rabbit': rabbit_actions, 'Wolf': wolf_actions} # actions for each class
class_lookdist = {'Apple': apple_lookdist, 'Rabbit': rabbit_lookdist, 'Wolf': wolf_lookdist} # lookdist for each class


# ----- Learning Parameters -----
alpha = 0.8 # learning rate, 0 < alpha < 1
gamma = 0.7 # discount rate, 0 < gamma < 1
epsilon = 0.1# starting exploration rate
#====USED ONLY WHEN EXPLORING==================
min_epsilon = 0.8# min exploration rate
epsilon_decay = 0.0005 # exploration decay rate
#==============================================
num_episodes = 10000
max_steps_per_episode = 100


# ----- Reward/Punishement -----
eat_apple = M
eaten_by_wolf = -N//4
move = -1
