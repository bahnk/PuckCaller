#!/usr/bin/python

from matplotlib.figure import Figure
from os import listdir, makedirs
from os.path import join
from skimage.io import imread, imsave
from skimage.transform import rescale
from skimage.exposure import equalize_hist

import re
import sys

################################################################################

##################
def Export(puck):#
##################

	print(puck)
	
	channels = {0: ("GFP","T"), 1: ("Cy3","G"), 2: ("TxRed","C"), 3: ("Cy5","A")}
	
	directory = "renamed_data"
	
	regex = re.compile("puck(\\d+)_base(\\d+)_ligation(\\d+)_(\\w+)_channel(\\d+)_transform.tif")
	
	directory = join("pucks", "puck{0}".format(str(puck).zfill(2)), "transform")
	
	files = []
	
	for f in listdir(directory):
		m = regex.match(f)
		if m:
			puck = int(m.group(1))
			base = int(m.group(2))
			ligation = int(m.group(3))
			primer = m.group(4).replace("plus", "+").replace("minus", "-")
			channel = int(m.group(5))
			d = {
				"Puck": puck,
				"Ligation": ligation,
				"Channel": channel,
				"Base": base,
				"Primer": primer,
				"Path": join(directory, f)
			}
			files.append(d)
	
	files = pd.DataFrame.from_records(files)
	files = files.sort_values(["Puck", "Ligation", "Channel"])
	
	m = 5
	n = files.Ligation.unique().size + 1
	
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
	
	for i, row in files[["Ligation", "Base", "Primer"]].iterrows():
		axes[row.Ligation].annotate(
			"Ligation {0}\nBase {1}\n({2})".format(row.Ligation, row.Base, row.Primer),
			xy=(.5, .5),
			xycoords="axes fraction",
			ha="center", va="center",
			color="black", fontsize=40
		)
		axes[row.Ligation].set_axis_off()
	
	for i, row in files.iterrows():
		print(f"Puck {puck}, Ligation {row.Ligation}, Channel {row.Channel}")
		I = imread(row.Path)
		i = row.Ligation + ( row.Channel ) * n
		axes[i].imshow( equalize_hist(I) )
		axes[i].set_axis_off()
	
	
	fig.tight_layout()
	fig.savefig("tmp/timelapse_transform/puck_{0}_transform.png".format(str(puck).zfill(2)))
	############################################################################


for i in range(30):
	if i == 19:
		continue
	Export(i)

