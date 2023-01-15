#!/usr/bin/python

from matplotlib.figure import Figure
from os import listdir
from os.path import join
from skimage.io import imread, imsave
from skimage.transform import rescale

import re
import seaborn as sns
import sys

################################################################################

###################
def Metrics(puck):#
###################

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
	
	records = []
	
	for i, row in files.iterrows():
	
		I = imread(row.Path)
	
		for c in range(4):
	
			J = I[:,:,c]
	
			rec = row[["Ligation", "Puck", "Base", "Primer"]].to_dict()
			rec["Channel"] = c + 1
			rec["Fluo"] = channels[c][0]
			rec["Nucleotide"] = channels[c][1]
			rec["Min"] = np.min(J)
			rec["Max"] = np.max(J)
			rec["Median"] = np.median(J)
			rec["Mean"] = np.mean(J)
			rec["Variance"] = np.var(J)
	
			print(rec)
	
			records.append(rec)
	
	df = pd.DataFrame.from_records(records)
	
	return df
	###########################################################################

#dfs = []
#for i in range(30):
#	if i == 19:
#		continue
#	dfs.append( Metrics(i) )
#df = pd.concat(dfs)
#df.to_csv("tmp/summary.csv", index=False)

df = pd.read_csv("tmp/summary.csv")
df = df.loc[ df.Puck.isin([1, 3, 7, 9, 13, 22, 28]) ]

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

grid = sns.FacetGrid(df, col="Channel", hue="Puck", palette="tab20c",
		                     col_wrap=2)

grid.map(plt.plot, "Ligation", "Min")
grid.add_legend()

grid.savefig("tmp/test.png")

# grid.map(plt.plot, "step", "position", marker="o")


# Draw a horizontal line to show the starting point
# grid.refline(y=0, linestyle=":")
#
# # Draw a line plot to show the trajectory of each random walk
# grid.map(plt.plot, "step", "position", marker="o")
#
# # Adjust the tick positions and labels
# grid.set(xticks=np.arange(5), yticks=[-3, 3],
#          xlim=(-.5, 4.5), ylim=(-3.5, 3.5))
#
#          # Adjust the arrangement of the plots
#          grid.fig.tight_layout(w_pad=1)
