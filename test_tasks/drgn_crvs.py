"""
2018-12-15
Dragon curves can be got by folding strip of paper n times
They can be described as set of moves F(orward) and L(eft)/R(ight) turns
Each n curve contains n-1 curve + L + reversed curve
Samples:
n=0 : F
n=1 : F L F
n=2 : FLF L FRF
n=3 : FLF L FRF L FLF R FRF
n=3 : L L R L L R R
	  FLF L FRF L FLF R FRF
n=4 : L L R L L R R L L L R R L R R
	  FLF L FRF L FLF R FRF L FLF L FRF R FLF R FRF
	  
"""

import sys

def calc_curve(num):
	if num == 0:
		result = "F"
		return result

	result = "FLF"
	
	i = 1
	while i < num: 
		i += 1
		result = result + ' L ' + result[::-1].replace('L', 't').replace('R', 'L').replace('t', 'R')
		print("i={0} : {1}".format(i, result))
	print('-'*15)
	
	return result
	
	
def main():
	msg = "Script requires integer number >= 0 for curves count"
	
	if len(sys.argv) < 2:
		print(msg)
		exit(1)
		
	try:
		N = int(sys.argv[1])
	except Exception as err:
		print("Error: {0}".format(err))
		print(msg)
		exit(1)

	if N < 0:
		print(msg)
		exit(1)
		
	print("Building dragon curve for N={0}".format(N))
	crv = calc_curve(N)
	print("Resulting curve: {0}".format(crv))

if __name__ == '__main__':
	main()