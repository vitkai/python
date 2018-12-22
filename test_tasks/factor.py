"""
Finds multipliers of integer numbers
Expects number as input
"""
import sys

n = int(sys.argv[1])

N = n
flag = 0
factor = 2
outp = ''
while factor*factor <= n:
    while (n % factor) == 0:
        n //= factor
        outp += '{0} * '.format(factor)
        flag += 1
    factor += 1

if n > 1:
    outp += str(n)
    flag += 1
elif flag > 0: outp = outp[:-2]

if flag > 0:
    outp += ' = {0}'.format(N)

print(outp)
