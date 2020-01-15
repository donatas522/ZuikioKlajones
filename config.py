
# ----- World Settings -----
rows = 10 # world rows
cols = 10 # world columns
cell_size = 50
N = rows * cols # number of world cells
M = 10 # energy from apple
apples_number = 4
average_distance = 0.8 * M
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
alpha = 0.1 # learning rate, 0 < alpha < 1
gamma = 0.9 # discount rate, 0 < gamma < 1
epsilon = 1 # starting exploration rate
min_epsilon = 0.01 # min exploration rate
epsilon_decay = 0.001 # exploration decay rate
num_episodes = 10000
max_steps_per_episode = 100


# ----- Reward/Punishement -----
eat_apple = M
eaten_by_wolf = N//4
move = -1
