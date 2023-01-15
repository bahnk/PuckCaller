#!/usr/bin/python

from math import floor
from os import listdir
from os.path import join
from skimage.io import imread, imsave
from skimage.transform import rescale
from matplotlib import cm
from matplotlib.figure import Figure

date = "211004"

fig = Figure(figsize=(12,10))

axes = fig.subplots(5, 6, gridspec_kw={"wspace":.01, "hspace":.01}, squeeze=True)

for i in range(30):
	puck = str(i+1).zfill(2)
	directory = f"pucks/Run{date}_Puck{puck}_01/Run{date}_Puck{puck}_01"
	X = imread( join(directory, "BeadImage.tif") )
	ax = axes[ floor(i/6) ][ i % 6 ]
	ax.imshow( rescale(X, .1) , cmap=cm.Greys_r )
	ax.annotate(
		str(i+1), xy=(.99, .99), xycoords="axes fraction",
		ha="right", va="top", color="yellow"
		)
	ax.set_axis_off()
	print(directory)

fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
fig.savefig("tmp/overview.png")

