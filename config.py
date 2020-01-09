

# ----- World Settings -----
rows = 20 # world rows
cols = 20 # world columns
N = rows * cols # number of world cells
background_color = '#FFFFFF' # white
wall_color = '#000000' # black
rabbit_color = '#0000FF' # blue
wolf_color = '#FF000' # red
carrot_color = '#00FF00' # green


# ----- Learning Parameters -----
alpha = 0.1 # learning rate, 0 < alpha < 1
gamma = 0.9 # discount rate, 0 < gamma < 1
epsilon = 1 # starting exploration rate
min_epsilon = 0.01 # min exploration rate
epsilon_decay = 0.001 # exploration decay rate


# ----- Reward/Punishement -----
M = 10
eat_carrot = M
eaten_by_wolf = N//4
move = -1

