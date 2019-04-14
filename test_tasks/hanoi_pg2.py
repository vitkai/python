'''     Animated Tower of Hanoi
        Graphical display of the moves to solve Tower of Hanoi.
        Initial Authour: Alan Richmond, Python3.Codes
'''
import pygame, random, time
 
#cols = ['#ff0000','#ff8000','#ffff00','#008000','#0000ff','#a000c0']
 
ndisks = 5                          # Number of disks
w, h = 1024, 512                    # Size of display window
st = 0.005                          # Animation speen - smaller is faster
 
wx = int(w/6)
dh = int(h/ndisks)
#radius = 60
radius = w//(3*ndisks)
rect=[0 for i in range(ndisks)]

cols = [0 for i in range(ndisks)]
 
d = pygame.display.set_mode((w,h))
pygame.display.set_caption("Towers of Hanoi")

def rand_color():
	return [random.randrange(0,255) for i in range(0,3)]

 
def moveDisk(disk, to):
    print("Move disk %d to peg %d" % (disk, to))
    r = radius*(disk+1)
    #c = pygame.Color(cols[disk])
    c = cols[disk]
    (x1,_,_,_)=rect[disk]               # current position
    x2=wx+to*2*wx-r/2                   # desired position
    dx = (x2-x1)/50                     # step size
    for i in range(50):                 # Animation loop:
                                            # erase disk from current position
        pygame.draw.rect(d, pygame.Color('#000000'), rect[disk])
        rect[disk]=pygame.Rect(x1+dx*(i+1),dh*disk,r,dh)
        pygame.draw.rect(d, c, rect[disk])  # draw disk in new position
        pygame.display.flip()               # update display
        time.sleep(st)                      # slow it down or it's too fast
    time.sleep(1)                       # allow a little time to admire it..
 
#   This is the magic bit:
def hanoi(ndisks, startPeg=0, endPeg=2):
    if ndisks:
                                        # move all but 1 disc from 1 peg to other
        hanoi(ndisks-1, startPeg, 3-startPeg-endPeg)
        moveDisk(ndisks-1, endPeg)      # move 1 disk to vacant peg
                                        # now move rest on to it...
        hanoi(ndisks-1, 3-startPeg-endPeg, endPeg)
 
#   Set up initial tower of disks
for disk in range(ndisks):
    r = radius*(disk+1)
    rect[disk]=pygame.Rect(wx-r/2,dh*disk,r,dh) # save disk coords, size
    cols[disk] = rand_color()
    pygame.draw.rect(d, cols[disk], rect[disk])
 
pygame.display.flip()
time.sleep(2)
hanoi(ndisks)