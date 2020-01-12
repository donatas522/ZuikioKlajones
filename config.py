
num_episodes = 10000
max_steps_per_episode = 100


# ----- World Settings -----
rows = 10 # world rows
cols = 10 # world columns
N = rows * cols # number of world cells
M = 10 # number of apples
directions = 8 # neigbouring cells
background_color = '#FFFFFF' # white
wall_color = '#000000' # black
rabbit_color = '#0000FF' # blue
wolf_color = '#FF000' # red
carrot_color = '#00FF00' # green


# ----- Agent Settings -----
rabbit_directions = 8
rabbit_actions = 8
rabbit_lookdist = 4
wolf_directions = 4
wolf_actions = 7
wolf_lookdist = 4


# ----- Learning Parameters -----
alpha = 0.1 # learning rate, 0 < alpha < 1
gamma = 0.9 # discount rate, 0 < gamma < 1
epsilon = 1 # starting exploration rate
min_epsilon = 0.01 # min exploration rate
epsilon_decay = 0.001 # exploration decay rate


# ----- Reward/Punishement -----
eat_apple = M
eaten_by_wolf = N//4
move = -1
