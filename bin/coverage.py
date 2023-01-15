#!/usr/bin/python

import re
from os import listdir
from os.path import join
import numpy as np
from skimage.io import imread, imsave
from skimage.color import gray2rgb

#B = imread("pucks/puck00/puck00_image.tif")
#
#I = np.zeros((5120, 5120, 4))
#
#for c in range(4):
#	path = f"pucks/puck00/puck00_base01_ligation02_T-1_channel{c+1}_balanced.tif"
#	I[:,:,c] = imread(path)
#
#M = np.apply_along_axis(max, 2, I)
#imsave("tmp/gray.tif", M.astype(np.uint16))
#M = gray2rgb(M)
#imsave("tmp/rgb.png", M)
#x, y = np.where( B == 255 )
#M[x,y] = (255*255, 0, 0)
#imsave("tmp/red.png", M)


#num = "00"
#base = "01"
#directory = f"pucks/puck{num}"
#pattern = f"puck{num}_base(\\d+)_ligation(\\d+)_[^_]+_channel(\\d)_balanced.tif"
#regex = re.compile(pattern)
#files = []
#for f in listdir(directory):
#	m = regex.match(f)
#	if m:
#		files.append( (m.group(1) , m.group(3) , join(directory, f) ) )
#files = sorted(files, key=lambda x: (x[0], x[1]))
#
#X = np.zeros((5120,5120,11,4))
#
#for l, c, f in files:
#	print(f)
#	X[:,:,int(l)-1,int(c)-1] = imread(f)
#
#I = np.zeros((11,5120,5120))
#
#for l in range(11):
#	print(l)
#	I[l,:,:] = np.apply_along_axis(max, 2, X[:,:,l,:])
#
#imsave("tmp/max.tif", I)

num = "00"
base = "01"
directory = f"pucks/puck{num}"
pattern = f"puck{num}_base(\\d+)_ligation(\\d+)_[^_]+_channel(\\d)_transform.tif"
regex = re.compile(pattern)
files = []
for f in listdir(directory):
	m = regex.match(f)
	if m:
		files.append( (m.group(1) , m.group(3) , join(directory, f) ) )
files = sorted(files, key=lambda x: (x[0], x[1]))

X = np.zeros((5120,5120,11,4))

for l, c, f in files:
	print(f)
	X[:,:,int(l)-1,int(c)-1] = imread(f)

I = np.zeros((11,5120,5120))

for l in range(11):
	print(l)
	I[l,:,:] = np.apply_along_axis(max, 2, X[:,:,l,:])

imsave("tmp/transform.tif", I)

