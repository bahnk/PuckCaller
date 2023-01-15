#!/usr/bin/python

from matplotlib.figure import Figure
from os import listdir
from os.path import join
from skimage.io import imread, imsave

import numpy as np
import pandas as pd
import re
import sys

suffixes = [
	"base01_ligation04_Tminus1",
	"base02_ligation05_T",
	"base03_ligation06_Tplus1",
	"base04_ligation07_Tplus2",
	"base05_ligation01_Tplus3",
	"base06_ligation14_3UPplus1",
	"base07_ligation13_3UP",
	"base08_ligation12_3UPminus1",
	"base09_ligation08_UPminus1",
	"base10_ligation09_UP",
	"base11_ligation10_UPplus1",
	"base12_ligation11_UPplus2",
	"base13_ligation02_UPplus3",
	"base14_ligation03_UPplus4"
]

color = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)]

for suffix in suffixes:

	image = np.zeros((500, 500, 3), np.ubyte)

	max_value = 0

	for j in range(4):
		channel = j + 1
		filename = f"puck22_{suffix}_channel{channel}_balanced.tif"
		path = join("pucks", "puck22", "balanced", filename)
		I = imread(path)[1500:2000,1500:2000]
		max_value = max(max_value, np.max(I))
	
	print(max_value)

	for j in range(4):
		channel = j + 1
		filename = f"puck22_{suffix}_channel{channel}_balanced.tif"
		path = join("pucks", "puck22", "balanced", filename)
		I = imread(path)[1500:2000,1500:2000]
		normalize = np.vectorize(lambda x: np.ubyte(255 * x / max_value))
		J = normalize(I)
		for i in range(3):
			image[:,:,i] = np.ubyte(image[:,:,i] + .25 * color[j][i] * J)
		#imsave(join("tmp", "test", re.sub("tif", "jpg", filename)), RGB)

	#image = np.zeros((500, 500, 3), np.ubyte)
	#for j in range(4):
	#	for i in range(3):
	#		image[:,:,i] = np.ubyte(image[:,:,i] + .2 * images[j][:,:,i])
	#print(len(images))
	print(image)
	imsave(join("tmp", "test", re.sub("tif", "jpg", filename)), image)

	




