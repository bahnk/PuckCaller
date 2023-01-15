#!/usr/bin/python

import sys, re
from os import listdir
from os.path import join
import numpy as np
import pandas as pd
from skimage.io import imread, imsave
from matplotlib.figure import Figure

in_dir = "pucks/puck13"
out_dir = "tmp/check"
#suffix = "balanced"
suffix = "transform"

#frames = [
#	{"name": "frame1", "x": 2214, "y": 1343, "width": 200, "height": 200},
#	{"name": "frame2", "x": 1200, "y": 2000, "width": 200, "height": 200},
#	{"name": "frame3", "x": 800, "y": 1500, "width": 200, "height": 200},
#	{"name": "frame4", "x": 1500, "y": 2500, "width": 200, "height": 200}
#]
#
################################################################################
## import images
#
#regex = "puck(\\d+)_base(\\d+)_ligation(\\d+)_(\\S+)_channel(\\d)_(\\S+).tif"
#rgx = re.compile(regex)
#
#rows = []
#
#for f in listdir(in_dir):
#	m = rgx.match(f)
#	if m and f.endswith(f"_{suffix}.tif"):
#		print(f)
#		puck = int(m.group(1))
#		base = int(m.group(2))
#		ligation = int(m.group(3))
#		channel = int(m.group(5))
#		I = imread(join(in_dir, f))
#		rows.append({
#			"Puck": puck,
#			"Base": base,
#			"Ligation": ligation,
#			"Channel":channel,
#			"Image":I}
#			)
#
#df = pd.DataFrame.from_records(rows)
#
################################################################################
## max projection
#
#######################
#def max_proj(images):#
#######################
#	print(images[0].shape)
#	II = np.zeros((len(images), *images[0].shape), images[0].dtype)
#	for i, I in enumerate(images):
#		II[i,:,:] = I
#	P = np.apply_along_axis(max, 0, II)
#	return P
#
#projections = df\
#	.groupby(["Puck", "Ligation"])\
#	.apply(lambda x: max_proj(x.Image.to_list()))\
#	.reset_index()\
#	.rename(columns={0: "Projection"})\
#	.sort_values("Ligation")
#
#PROJ = np.zeros(
#	(projections.shape[0], *projections.Projection.iloc[0].shape),
#	projections.Projection.iloc[0].dtype
#	)
#
#for i, X in enumerate(projections.Projection):
#	PROJ[i,:,:] = X
#
#imsave(join(out_dir, "max_proj.tif"), PROJ)
#
################################################################################
## indices
#
#regex = "puck(\\d+)_base(\\d+)_ligation(\\d+)_(\\S+)_(\\S+).tif"
#rgx = re.compile(regex)
#
#rows = []
#
#for f in listdir(in_dir):
#	m = rgx.match(f)
#	if m and f.endswith("_indices.tif"):
#		print(f)
#		puck = int(m.group(1))
#		base = int(m.group(2))
#		ligation = int(m.group(3))
#		I = imread(join(in_dir, f))
#		rows.append({
#			"Puck": puck,
#			"Base": base,
#			"Ligation": ligation,
#			"Image":I
#		})
#
#indices = pd.DataFrame.from_records(rows)
#indices = indices.sort_values("Ligation")
#
#INDICES = np.zeros(
#	(indices.shape[0], *indices.Image.iloc[0].shape),
#	indices.Image.iloc[0].dtype
#	)
#
#for i, X in enumerate(indices.Image):
#	INDICES[i,:,:] = X
#
#imsave(join(out_dir, "indices.tif"), INDICES)
#
################################################################################
## calling
#
#puck = "puck" + str(indices.Puck.iloc[0]).zfill(2)
#BEADS = imread(join(in_dir, f"{puck}_image.tif"))
#
#l = PROJ.shape[0]
#
#for frame in frames:
#
#	fig = Figure(figsize=(4*l,4*3))
#	axes = [ fig.add_subplot(3, l, i) for i in range(1, 3*l+1) ]
#
#	name = frame["name"]
#	x = frame["x"]
#	y = frame["y"]
#	width = frame["width"]
#	height = frame["height"]
#
#
#	for i in range(l):
#
#		print(frame, l)
#
#		X = PROJ[i,y:(y+height),x:(x+width)]
#		axes[i].imshow(X)
#		axes[i].set_axis_off()
#		axes[i].annotate(
#			str(i+1),
#			xy=(.99, .99),
#			size=20,
#			color="red",
#			xycoords="axes fraction",
#			ha="right", va="top"
#			)
#
#		if i == 0:
#			axes[i].annotate(
#				"Maximum projection",
#				xy=(.01, .01),
#				size=18,
#				color="red",
#				xycoords="axes fraction",
#				ha="left", va="bottom"
#				)
#
#		Y = INDICES[i,y:(y+height),x:(x+width)]
#		axes[i+l].imshow(Y)
#		axes[i+l].set_axis_off()
#
#		if i == 0:
#			axes[i+l].annotate(
#				"Base call",
#				xy=(.01, .01),
#				size=18,
#				color="red",
#				xycoords="axes fraction",
#				ha="left", va="bottom"
#				)
#
#		Z = BEADS[y:(y+height),x:(x+width)]
#		axes[i+2*l].imshow(Z)
#		axes[i+2*l].set_axis_off()
#
#		if i == 0:
#			axes[i+2*l].annotate(
#				"Beads",
#				xy=(.01, .01),
#				size=18,
#				color="red",
#				xycoords="axes fraction",
#				ha="left", va="bottom"
#				)
#
#
#	fig.tight_layout(pad=1.0)
#	fig.subplots_adjust(wspace=.01, hspace=.01)
#	fig.savefig(
#		join(out_dir, "frames" , f"{puck}_{name}_{suffix}.png"),
#		bbox_inches="tight"
#	)


means = []
for i in range(PROJ.shape[0]):
	means.append( np.mean(PROJ[i,:,:]) )

fig = Figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.plot(range(1, len(means)+1), means, "bo")
ax.set_title("Intensity means of the max projection per ligation")
ax.set_xlabel("Ligation")
ax.set_ylabel("Intensity mean")
fig.savefig(join(out_dir, "mean.png"))


###############################################################################
regex = "puck13_base(\\d+)_ligation(\\d+)_(\\S+)_zselect.tif"
rgx = re.compile(regex)

rows = []

in_dir = "pucks/z_selection"

for f in listdir(in_dir):
	m = rgx.match(f)
	if m:
		print(f)
		base = int(m.group(1))
		ligation = int(m.group(2))
		I = imread(join(in_dir, f))
		rows.append({
			"Puck": puck,
			"Base": base,
			"Ligation": ligation,
			"Image":I}
			)

df = pd.DataFrame.from_records(rows)
df = df.sort_values("Ligation")

means = []
for i, row in df.iterrows():
	print(row.Ligation)
	proj = np.apply_along_axis(np.max, 2, row.Image)
	mean_value = np.mean(proj)
	means.append(mean_value)

fig = Figure(figsize=(8, 8))
ax = fig.add_subplot(111)
ax.plot(range(1, len(means)+1), means, "bo")
ax.set_title("Intensity means of the max projection per ligation")
ax.set_xlabel("Ligation")
ax.set_ylabel("Intensity mean")
fig.savefig(join(out_dir, "mean_raw.png"))

