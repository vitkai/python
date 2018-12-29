"""
takes N party possible participants
1st invitee passes info to a random candidate but not to the host
all other invitees pass info to another one but the one he get info from or host
to find out if info reaches all of the possible guests
"""
import random
N = 10


def pass_goss(src):
    r = random.randint(2, N-1)
    print (r)
    if not guests[r]:
        dst = r
    else :
        dst = N
    
    print(dst)
    return dst
    

# init arr of N
guests = [0] * N
guests[0] = 1 # host and 1st invitee know

cnt = 0 # number of notified people
curr = 1 # current person
    
while cnt <= N:
    guests[curr] = 1 
    cnt += 1
    print(guests)
    new_curr = pass_goss(curr)
    if new_curr == N:
        break
    elif (new_curr != curr):
          curr = new_curr

print("Total notified guests: {0}".format(cnt))