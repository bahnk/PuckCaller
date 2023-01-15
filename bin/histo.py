#!/usr/bin/python

import re
from skimage import io
from os.path import join
from os import listdir
from itertools import combinations
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

mpl.rcParams.update({'font.size': 4})

dirpath = join(
		"pucks",
		"Run210603_Puck01_01",
		"Run210603_Puck01_01_tif",
		"Run210603_Puck01_01"
		)

tifs = []
for f in listdir(dirpath):
	if f.endswith("_Stitched.tif"):
		ligation = re.sub(".*_Ligation_(\d+)_.*", "\\1", f)
		tifs.append( ( ligation , join(dirpath, f) ) )
tifs = sorted(tifs, key=lambda x: x[0])[:2]

fig, axs = plt.subplots(len(tifs), 4, figsize=(4,len(tifs)))

for i, (ligation, path) in enumerate(tifs):

	print(i)

	X = io.imread(path)

	for c in range(X.shape[2]):
		pixels = range(1, 100)
		#pixels = X[:,:,c].reshape(X.shape[0]*X.shape[1], 1)[:,0].tolist()[:100]
		axs[i, c].hist(pixels, bins=1024, log=True, range=(0, 2**16))
		axs[i, c].set_yticks(ticks=[])
		axs[i, c].set_yticklabels(labels=[])
		axs[i, c].yaxis("off")


#fig.tight_layout()
#	
#cols = ['Channel {}'.format(col) for col in range(1, 5)]
#rows = ['Ligation {}'.format(row) for row in range(1, 12)]
#
#for ax, col in zip(axs[0], cols):
#	ax.set_title(col)
#
#for ax, row in zip(axs[:,0], rows):
#	ax.set_ylabel(row, rotation=0, size='large')


plt.savefig( join("tmp", "hist.pdf") )
#plt.savefig( join("tmp", "hist.png") )

