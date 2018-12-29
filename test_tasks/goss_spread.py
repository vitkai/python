"""
takes N party possible participants
1st invitee passes info to a random candidate but not to the host
all other invitees pass info to another one but the one he get info from or host
to find out if info reaches all of the possible guests
"""
import random
N = 10

def pass_goss(src):
    r = random.random(1, N)
    print (r)
    return dst
    

# init arr of N
guests = [0] * N
guests[0:1] = [1, 1] # host and 1st invitee know
    
print(guests)