import random

f = open("inputlinear.txt", "w");
f.write("10000000\n")

for i in range(10000000):
	f.write(str( int(random.random()*10000000)))
	f.write("\n")
f.close()
