import multiprocessing as mp
import math
import os

#----------------------------------------------------------------------------------------------------------------------
#This is a VERY SIMPLE example of parallel processing in Python using the multiprocessing library using the Pools object.
#----------------------------------------------------------------------------------------------------------------------


def process_info():
    print('Module:' + str(__name__) + '\n')
    print('Parent Process id:' + str(os.getppid())+ '\n' )
    print('Process id:' + str(os.getpid())+ '\n\n' )

def cubes_and_sqare_root(a):
	process_info()
	return (int(a), math.sqrt(a**3))

def main():
	pool = mp.Pool(processes= mp.cpu_count())
	results = [ pool.map(cubes_and_sqare_root, (x for x in range(1,8))) ]
	print(results)

if __name__ == '__main__':
	main()