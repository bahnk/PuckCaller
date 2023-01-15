#!/usr/bin/python

import sys
import re
from os import listdir
from os.path import join
from shutil import copyfile

from math import floor
import numpy as np
import pandas as pd

from skimage.io import imread, imsave
from skimage.transform import rescale

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages

from pyairtable import Table
from pyairtable.utils import attachment

###############################################################################

#date = "210603"
#nslices = 41
#in_dir = "tmp/upload"
#out_dir = "tmp/out"

date = sys.argv[1]
nslices = int(sys.argv[2])
in_dir = sys.argv[3]
out_dir = sys.argv[4]

www = "/camp/stp/babs/www/shiny/external/users/bahn/rodriquess/pucks"
url = "https://bioinformatics.crick.ac.uk/shiny/users/bahn/rodriquess/pucks"

API_KEY = "keyPVzvAqFrxvZIRt"
TABLE_ID = "appC4CQxYI8BAL3H7"

###############################################################################

zselect_dfs = []
for f in listdir(in_dir):
	if f.endswith("_zselect.csv"):
		zselect_dfs.append( pd.read_csv( join(in_dir, f) ) )

zselect = pd.concat(zselect_dfs, axis=0)

pdf1 = PdfPages(join(out_dir, f"Run{date}_zselection.pdf"))
pdf2 = PdfPages(join(www, f"{date}_zselection.pdf"))

colors = {1: "red", 2: "blue", 3: "green", 4: "purple"}

mpl.rc('font', size=22)

for puck, df in zselect.groupby("Puck"):

	fig = Figure(figsize=(12,12))
	axes = [ fig.add_subplot(2, 2, i+1) for i in range(4) ]

	for channel, ddf in df.groupby("Channel"):
		ax = axes[ int(channel) - 1 ]
		ax.scatter(ddf.Ligation, ddf.Z, color=colors[channel], s=60)
		ax.set_ylim(0, nslices)
		ax.set_title(f"Channel {channel}")
		ax.set_xticks([ l for l in range(1, ddf.Ligation.max()+1) ])
		xticklabels = []
		for l in range(1, ddf.Ligation.max()+1):
			xticklabels.append( str(l) if l % 2 == 1 else "" )
		ax.set_xticklabels(xticklabels)
		ax.set_xlabel("Ligation")
		ax.set_ylabel("Z selection")

	fig.suptitle(f"Puck {int(puck)}")
	fig.tight_layout(rect=[0, 0, 1, 0.99])
	fig.savefig(join(www, f"{date}_{str(puck).zfill(2)}_zselection.pdf"))
	pdf1.savefig(fig)
	pdf2.savefig(fig)

pdf1.close()
pdf2.close()

###############################################################################
acquisitions_key = "Acquisition date"
acquisitions_tbl = Table(API_KEY, TABLE_ID, "tblk69rrKfujc1uW6")

acqs = {}
acq_recs = []

for acq in acquisitions_tbl.all():
	acq_recs.append( ( acq["fields"]["Date"] , acq["id"] ) )

if len(acq_recs) > 0:
	acqs = dict(acq_recs)

if date not in acqs.keys():
	acq_rec = acquisitions_tbl.create({"Date": date})
	acqs[date] = acq_rec["id"]

###############################################################################
tbl = Table(API_KEY, TABLE_ID, "tblfMP4cTaDWHnDma")
recs = []
for rec in tbl.all():
	recs.append( ( rec["fields"]["Name"] , rec["id"] ) )
recs = dict(recs)

nums = []
for f in listdir(in_dir):
	if f.endswith("_image.tif"):
		nums.append( re.sub("puck(\\d+)_.*", "\\1", f) )
nums = sorted( list( set( nums ) ) )

ratios = pd.Series()
barcodes = pd.Series()
records = []

fig = Figure(figsize=(12,10))
grid = {"wspace":.01, "hspace":.01}
axes = fig.subplots(5, 6, gridspec_kw=grid, squeeze=True)

for num in nums:

	i = int(num)

	key = f"{date}_{num}"
	print(key)

	X = imread( join(in_dir, f"puck{num}_image.tif") )

	# overview
	ax = axes[ floor(i/6) ][ i % 6 ]
	ax.imshow( rescale(X, .1) , cmap=cm.Greys_r )
	ax.annotate(
			str(i), xy=(.99, .99), xycoords="axes fraction",
			ha="right", va="top", color="yellow"
			)
	ax.set_axis_off()

	# coverage
	vals, cnts = np.unique(X, return_counts=True)
	ratio = round(cnts[1]/cnts[0], 3)
	s = pd.Series(ratio, index=[f"Puck_{num}"])
	ratios = ratios.append(s)

	# locations
	locs = pd.read_csv( join(in_dir, f"puck{num}_locations.unsorted.csv") )
	locs = locs.sort_values("Barcode")
	locs.to_csv(join(out_dir, f"puck{num}_locations.csv"), index=False)
	locs.to_csv(join(www, f"{date}_{num}.csv"), index=False)

	# barcodes
	bcs = pd.read_csv( join(in_dir, f"puck{num}_barcodes.unsorted.txt") , header=None)
	bcs = bcs.sort_values(0)
	bcs.to_csv(join(out_dir, f"puck{num}_barcodes.txt"), index=False)
	s = pd.Series(bcs.shape[0], index=[f"Puck_{num}"])
	barcodes = barcodes.append(s)

	# uploaded image
	Y = rescale(X, .4)
	png = f"{key}.png"
	imsave( join(www, png ) , Y )

	d = {
		"Name": key,
		"Acquisition": [acqs[date]],
		"Barcodes": bcs.shape[0],
		"Coverage": ratio,
		"Image": [attachment(f"{url}/{png}", f"{png}")],
		"Spatial": [attachment(f"{url}/{date}_{num}.csv", f"{date}_{num}.csv")],
		"Z selection": [attachment(f"{url}/{date}_{num}_zselection.pdf")]
	}

	if key in recs.keys():
		tbl.update(recs[key], d)
	else:
		tbl.create(d)

fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
fig.savefig(join(out_dir, f"Run{date}_overview.png"))
fig.savefig(join(www, f"{date}.png"))
acquisitions_tbl.update(
		acqs[date],
		{
			"Image": [attachment(f"{url}/{date}.png", f"{date}.png")],
			"Z selection": [
				attachment(f"{url}/{date}_zselection.pdf", f"{date}_zselection.pdf")
			]
		}
		)

###############################################################################

df = pd.merge(
	barcodes.to_frame().reset_index(),
	ratios.to_frame().reset_index(),
	on="index"
	)\
	.rename(columns={"index": "Puck", "0_x": "Barcode", "0_y": "ImageCoverage"})\
	.sort_values("Puck")\
	.to_csv(join(out_dir, f"Run{date}_metrics.csv"), index=False)

