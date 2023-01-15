#!/usr/bin/python

import sys
import numpy as np
import pandas as pd
from skimage.io import imread, imsave

name = sys.argv[1]
puck = sys.argv[2]
ligation = sys.argv[3]

slices = []
nums = []

for path in sys.argv[4:]:
   X = imread(path)
   z = np.std(X, axis=(1,2)).argmax()
   slices.append( X[z,:,:] )
   nums.append(z)

shape= (len(slices), slices[0].shape[0], slices[0].shape[1])
I = np.zeros(shape=shape, dtype=np.uint16)
for s, S in enumerate(slices):
   I[s,:,:] = S
imsave(f"{name}.tif", I)

d = {
      "Puck": [puck] * len(slices),
      "Ligation": [ligation] * len(slices),
      "Channel": [ c + 1 for c in range(len(slices)) ],
      "Z": nums
      }
df = pd.DataFrame(d)
df.to_csv(f"{name}.csv", index=False)

