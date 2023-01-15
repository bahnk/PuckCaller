#!/usr/bin/python

from matplotlib.figure import Figure
from os import listdir
from os.path import join
from skimage.io import imread, imsave
from skimage.transform import rescale

import re
import sys

################################################################################

##################
def Export(puck):#
##################

	print(puck)

	channels = {0: ("GFP","T"), 1: ("Cy3","G"), 2: ("TxRed","C"), 3: ("Cy5","A")}
	
	directory = "renamed_data"
	
	regex = re.compile("puck(\\d+)_base(\\d+)_ligation(\\d+)_(\\w+)_zselect.tif")
	
	directory = join("pucks", "z_selection", "puck{0}".format(str(puck).zfill(2)))
	
	files = []
	
	for f in listdir(directory):
		m = regex.match(f)
		if m:
			puck = int(m.group(1))
			base = int(m.group(2))
			ligation = int(m.group(3))
			primer = m.group(4).replace("plus", "+").replace("minus", "-")
			d = {
				"Puck": puck,
				"Base": base,
				"Ligation": ligation,
				"Primer": primer,
				"Path": join(directory, f)
			}
			files.append(d)
	
	files = pd.DataFrame.from_records(files)
	files = files.sort_values(["Puck", "Ligation"])
	files = files.set_index("Ligation")
	
	m = 5
	n = files.shape[0] + 1
	
	fig = Figure(figsize=(n*4, m*4))
	
	axes = [ fig.add_subplot(m, n, i+1) for i in range(m*n) ]
	
	axes[0].annotate(
		f"Puck {puck}",
		xy=(.5, .5),
		xycoords="axes fraction",
		ha="center", va="center",
		color="black", fontsize=40
	)
	axes[0].set_axis_off()
	
	for channel, c in channels.items():
		fluo = c[0]
		base = c[1]
		i = ( channel + 1 ) * n
		axes[i].annotate(
			f"{fluo}\n{base}",
			xy=(.5, .5),
			xycoords="axes fraction",
			ha="center", va="center",
			color="black", fontsize=40
		)
		axes[i].set_axis_off()
	
	
	for ligation, path in files.iterrows():
	
		axes[ligation].annotate(
			"Ligation {0}\nBase {1}\n({2})".format(ligation, path.Base, path.Primer),
			xy=(.5, .5),
			xycoords="axes fraction",
			ha="center", va="center",
			color="black", fontsize=40
		)
	
		axes[ligation].set_axis_off()
	
		I = imread(path.Path)
	
		for channel in range(4):
			i = ligation + ( channel + 1 ) * n
			axes[i].imshow( I[:,:,channel] )
			axes[i].set_axis_off()
	
	
	fig.tight_layout()
	fig.savefig("tmp/timelapse/puck_{0}.png".format(str(puck).zfill(2)))
	############################################################################


for i in range(20, 30):
	if i == 19:
		continue
	Export(i)

