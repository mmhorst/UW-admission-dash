import sys, glob
fs = sys.argv[1]
paths = glob.glob(fs+"*.pdf")
for p in paths:
	print(p.split("\\")[-1])