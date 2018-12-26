"""
Refugee tries to escape NxN town starting form the middle
it cannot cross its own trail
script takes N dimension as an argument
"""
import random
#import sys

#n = int(sys.argv[1])
n = 7

rows = [False] * n
array = [rows] * n

# coordinates
x = n // 2
y = n // 2

trail = ''

# while we are not in dead end
while (x > 0) and (x < n-1) and (y > 0) and (y < n-1):
    array[x][y] = True
    r = random.randrange(1, 5)
    print(r)
    if (r == 1) and (not array[x+1][y]):
        x += 1
        trail += 'R'
    elif (r == 2) and (not array[x-1][y]):
        x -= 1
        trail += 'L'
    elif (r == 3) and (not array[x][y+1]):
        y += 1
        trail += 'U'
    elif (r == 4) and (not array[x][y-1]):
        y -= 1
        trail += 'D'

print(trail)
print(array)
