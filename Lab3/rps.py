import numpy as np

def user_move():
    move = input('Rock (R), Paper (P), or Scissors (S)?')
    if (move == 'R'):
        return 1
    elif (move == 'P'):
        return 2
    elif (move == 'S'):
        return 3

while(True):
    move = user_move()
    cpu_move = np.random.randint(1, 4)
    if (cpu_move == 1):
        print('CPU played Rock')
    elif (cpu_move == 2):
        print('CPU played Paper')
    elif (cpu_move == 3):
        print('CPU played Scissors')
    if ((move==cpu_move+1)or(cpu_move==3 and move==1)):
        print('You win!')
    elif (move==cpu_move):
        print('Tie')
    else:
        print('You Lose')
