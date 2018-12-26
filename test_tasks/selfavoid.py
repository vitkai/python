"""
Refugee tries to escape NxN town starting form the middle
it cannot cross its own trail
script takes N dimension as an argument
"""
import random
#import sys
import turtle

#n = int(sys.argv[1])
n = 25

def prnt_arr(ar):
    for i in range(len(ar)):
        for j in range(len(ar[i])):
            if ar[i][j]: print(1, end='')
            else: print(0, end='')
        print('')


def draw_path(path):
    step = 800 // (n-1)
    angles = {'U':90, 'D':270, 'L':180, 'R':0}

    silly = turtle.Turtle()
    turn_angl = 0
    cur_angl = 0
    for cmd in path:
        # getting new turn angle
        turn_angl = (angles[cmd] - cur_angl)
        cur_angl += turn_angl

        silly.left(turn_angl)
        silly.forward(step)

        #print(cur_angl)

    turtle.done()


array = []
for i in range(n):
    row = [False] * n
    array += [row]

#prnt_arr(array)

# coordinates
x = n // 2
y = n // 2

trail = ''

"""print('({0}, {1})'.format(x, y))
array[x][y] = True
prnt_arr(array)"""

step = 0
# while we are inside the town
while (x > 0) and (x < n-1) and (y > 0) and (y < n-1):
    array[x][y] = True
    step += 1

    # to check if we're in the dead end
    if array[x-1][y] and array[x+1][y] and array[x][y-1] and array[x][y+1]:
        print('Dead end on step {0}'.format(step))
        break

    r = random.randrange(1, 5)

    # print('{0} => ({1}, {2})'.format(r, x, y))

    if (r == 1) and (not array[x+1][y]):
        x += 1
        trail += 'D'
    elif (r == 2) and (not array[x-1][y]):
        x -= 1
        trail += 'U'
    elif (r == 3) and (not array[x][y+1]):
        y += 1
        trail += 'R'
    elif (r == 4) and (not array[x][y-1]):
        y -= 1
        trail += 'L'

    #prnt_arr(array)

print(trail)
draw_path(trail)
# print(array)
