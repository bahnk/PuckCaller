#!/usr/bin/python

from os import makedirs
from os.path import join
import pandas as pd
from shutil import copyfile
from skimage.io import imread, imsave

puck_dir = "../pucks"
work_dir = "."
date = "210611"
out_dir = join(work_dir, "pucks", "z_selection")

def create_dir(path):
	try:
		makedirs(path)
	except OSError as e:
		pass
create_dir(out_dir)

def create_df(puck, ligation):
	rows = []
	for i in range(1, 5):
		rows.append({"Puck": puck, "Ligation": ligation, "Channel": i, "Z": 1})
	return pd.DataFrame.from_records(rows)

df = pd.read_csv( join(work_dir, "order.csv") )

for puck in range(15):
	for l, row in df.iterrows():

		num = str(puck+1).zfill(2)
		ligation = str(l+1).zfill(2)

		#########################################################################
		z = create_df(puck, ligation)
		print(z)

		#########################################################################
		directory = \
			join(
				puck_dir,
				f"Run{date}_Puck{num}_01",
				f"Run{date}_Puck{num}_01_tif",
				f"Run{date}_Puck{num}_01"
		)
		filename = f"Run{date}_Puck{num}_01_Ligation_{ligation}_Stitched.tif"
		path = join(directory, filename)
		print(path)
		X = imread(path)
		print(X)

		#########################################################################
		new_num = str(puck).zfill(2)
		base = str(row.base).zfill(2)
		new_ligation = str(row.ligation).zfill(2)
		primer = row.primer
		basename = f"puck{new_num}_base{base}_ligation{new_ligation}_{primer}"
		basepath = join(out_dir, basename)
		print(basepath)

		#########################################################################
		z.to_csv(basepath+"_zselect.csv", index=False)
		#copyfile(path, basepath+"_zselect.tif")
		imsave(basepath+"_zselect.tif", X)

