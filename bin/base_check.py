#!/usr/bin/python

import re
from os import listdir
from os.path import join
import numpy as np
import pandas as pd
from skimage.io import imread, imsave
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.colors import ListedColormap

box = 40

################################################################################
#puck = "13"
#directory = f"pucks/puck{puck}"
#results_directory = f"pucks/results"
#out_dir = "tmp"
#
################################################################################
#I = imread(join(directory, f"puck{puck}_indices.tif"))
#df = pd.read_csv(join(results_directory, f"puck{puck}_locations.csv"))
#df = df.rename(columns={"Barcode": "Bead"})
#regex = re.compile("puck([0-9]+)_base([0-9]+)_.*_channel([0-9])_tophat.tif")
#
################################################################################
#multipliers = pd.read_csv(f"pucks/puck{puck}/puck{puck}_multipliers.csv")
#multipliers = multipliers.set_index("Ligation")
#
################################################################################
#
#files = []
#for f in listdir(directory):
#	m = regex.match(f)
#	if m:
#		print(f)
#		base = int(m[2])
#		channel = int(m[3])
#		t = ( base , channel , imread( join(directory, f) ) )
#		files.append(t)
#files = sorted(files, key=lambda x: (x[0], x[1]))

###############################################################################

barcodes = df.Bead.sample(20)

for bc in barcodes:

	bead = df.loc[ df.Bead == bc ].index[0]

	row = float( df.iloc[bead].x )
	col = float( df.iloc[bead].y )
	xmin = np.floor( row - box / 2 ).astype(int)
	xmax = np.ceil( row + box / 2 ).astype(int)
	ymin = np.floor( col - box / 2 ).astype(int)
	ymax = np.ceil( col + box / 2 ).astype(int)
	
	n = max( list( map( lambda x: x[0], files ) ) )
	
	h = 8
	down = 1

	fig = Figure(figsize=(14/down,h/down))
	
	colors = pd.Series(["black", "red", "green", "blue", "yellow"], index=range(5))
	bases = {0: "N", 1: "T", 2: "G", 3: "C", 4: "A"}
	col_dict = {0: "black", 1: "red", 2: "green", 3: "blue", 4: "yellow"}
	col_base = {"N": "black", "T": "red", "G": "green", "C": "blue", "A": "yellow"}
	
	###############################################################################
	# indices
	
	for b in range(n):
		X = I[ b , ymin:ymax , xmin:xmax ]
		print( colors.loc[ sorted( np.unique(X) ) ].to_list() )
		cmap = ListedColormap( colors.loc[ sorted( np.unique(X) ) ].to_list() )
		ax = fig.add_subplot(h, n, b+1)
		ax.imshow(X, cmap=cmap)
		ax.scatter(x=X.shape[1]/2, y=X.shape[0]/2, c="white", s=.3, marker="x")
		ax.set_axis_off()
	
	###############################################################################
	# images
	
	for b, c, X in files:
		Y = X[ymin:ymax, xmin:xmax]
		ax = fig.add_subplot(h, n, c*n+b)
		ax.set_axis_off()
		if b == 1:
			color = col_dict[c]
			ax.annotate(
					bases[c],
					xy=(-0.3, 0.5),
					xycoords="axes fraction",
					bbox=dict(facecolor=color, edgecolor=color, boxstyle="round"),
					ha="right", va="center"
					)
		ax.imshow(Y, cmap=cm.Greys.reversed())
		ax.scatter(x=Y.shape[1]/2, y=Y.shape[0]/2, c="red", s=.3)
		ax.annotate(
				multipliers.loc[b].iloc[c-1],
				xy=(0.01, 0.01),
				color="yellow",
				size=7/down,
				xycoords="axes fraction",
				ha="left", va="bottom"
				)
	
	###############################################################################
	# base call
	
	B = imread(join(directory, f"puck{puck}_image.tif"))
	
	for b, base in enumerate(df.iloc[bead].Bead, start=1):
		Y = B[ymin:ymax, xmin:xmax]
		ax = fig.add_subplot(h, n, 5*n+b)
		ax.set_axis_off()
		ax.imshow(Y)
		ax.scatter(x=Y.shape[1]/2, y=Y.shape[0]/2, c="red", s=.3)
	
	###############################################################################
	# sequence
	for b, base in enumerate(df.iloc[bead].Bead, start=1):
		ax = fig.add_subplot(h, n, 6*n+b)
		ax.set_axis_off()
		color = col_base[base]
		ax.annotate(base, xy=(0.5, 0.5), xycoords="axes fraction",
			size=24/down, ha="center", va="center",
			bbox=dict(facecolor=color, edgecolor=color, boxstyle="round")
		)
	
	###############################################################################
	# number 
	for b, base in enumerate(df.iloc[bead].Bead, start=1):
		ax = fig.add_subplot(h, n, 7*n+b)
		ax.set_axis_off()
		ax.annotate(b, xy=(0.5, 0.5), xycoords="axes fraction",
			size=24/down, ha="center", va="center"
		)

	###############################################################################
	
	sequence = "".join( np.vectorize(bases.get)( I[:,int(col),int(row)] ) )
	##for l, base in enumerate(sequence, start=1):
	##	ax = fig.add_subplot(h, n, 7*n+l)
	##	ax.set_axis_off()
	##	color = col_base[base]
	##	ax.annotate(base, xy=(0.5, 0.5), xycoords="axes fraction",
	##		size=24, ha="center", va="center",
	##		bbox=dict(facecolor=color, edgecolor=color, boxstyle="round")
	##	)
	#
	
	fig.tight_layout()
	fig.savefig(f"tmp/base_call_{m}_{str(bead)}_{bc}.png", bbox_inches="tight")
	
	print(sequence)
	print(df.iloc[bead].Bead)
	print(bead)
	print( df.loc[ df.Bead.str.match( sequence.replace("N", "") ) ] )


