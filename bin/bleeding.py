#!/usr/bin/python

from skimage import io
from os.path import join
import re
from os import listdir
from itertools import combinations
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

#path = join(
#		"pucks",
#		"Run210603_Puck01_01",
#		"Run210603_Puck01_01_tif",
#		"Run210603_Puck01_01",
#		"Run210603_Puck01_01_Ligation_01_Stitched.tif"
#		)
#
#X = io.imread(path)
#
#for i, j in combinations( range(0, 4) , 2 ):
#	print(i, j)
#	I = X[:,:,i].reshape(1, X.shape[0]*X.shape[1])[:,4300000:4310000]
#	J = X[:,:,j].reshape(1, X.shape[0]*X.shape[1])[:,4300000:4310000]
#	print(I)
#	print(J)
#	plt.close()
#	plt.plot(I, J, marker="o", markersize=1, color="blue")
#	plt.title("{0} VS {1}".format(i, j))
#	plt.savefig( join("tmp", "channel{0}_vs_channel{1}.pdf".format(i, j)) )
#	plt.savefig( join("tmp", "channel{0}_vs_channel{1}.png".format(i, j)) )

dirpath = join(
		"pucks",
		"Run211004_Puck01_01",
		"Run211004_Puck01_01_tif",
		"Run211004_Puck01_01"
		)

tifs = []
for f in listdir(dirpath):
	if f.endswith("_Stitched.tif"):
		ligation = re.sub(".*_Ligation_(\d+)_.*", "\\1", f)
		tifs.append( ( ligation , join(dirpath, f) ) )
tifs = sorted(tifs, key=lambda x: x[0])
tifs = tifs[:1]

for l, (ligation, path) in enumerate(tifs):

	X = io.imread(path)

	for i, j in combinations( range(0, 4) , 2 ):
		print(i, j)
		I = X[:,:,i].reshape(1, X.shape[0]*X.shape[1])[:,4300000:4320000]
		J = X[:,:,j].reshape(1, X.shape[0]*X.shape[1])[:,4300000:4320000]
		print(I)
		print(J)
		plt.close()
		plt.plot(I, J, marker="o", markersize=1, color="blue")
		plt.title("ligation {0}, channel {1} VS {2}".format(int(ligation), i+1, j+1))
		#plt.savefig( join("tmp", "ligation{0}_channel{1}_vs_channel{2}.pdf".format(ligation, i+1, j+1)) )
		plt.savefig( join("tmp", "ligation{0}_channel{1}_vs_channel{2}.png".format(ligation, i+1, j+1)) )

