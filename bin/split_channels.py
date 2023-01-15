#!/usr/bin/python

import sys
import json
import numpy as np
from tifffile import TiffFile, imread, imsave

tiff = TiffFile(sys.argv[1])

stk = {}

for page in tiff.pages:
   for tag in page.tags:
      if tag.code == 51123:
         channel = tag.value["ChannelIndex"] + 1
         frame = tag.value["SliceIndex"] + 1
         if channel not in stk.keys():
            stk[channel] = []
         stk[channel].append( (frame, page.asarray()) )

for channel, frames in stk.items():
   shape = (len(frames), frames[0][1].shape[0], frames[0][1].shape[0])
   I = np.zeros(shape=shape, dtype=np.uint16)
   for z, frame in sorted(frames, key=lambda x:x[0]):
      I[z-1,:,:] = frame
   imsave(f"{sys.argv[2]}_channel{channel}.tif", I)

