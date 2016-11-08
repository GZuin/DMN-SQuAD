import sys
import os

#Include uppercase words in the stopword list
def expand(ifile):
	vet = []
	inp = open(ifile,'r')
	original = inp.readlines()
	for line in original:
		vet.append(line)
		vet.append(line.capitalize())
	inp.close()
	out = open(ifile,'w')
	for word in vet:
		out.write(word)
	out.close()

if __name__ == '__main__':
	expand(sys.argv[1])
