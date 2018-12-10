import sys

import csv
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import imageio

from scipy.ndimage.filters import gaussian_filter
from matplotlib.colors import Normalize
from scipy.misc.pilutil import imread

def heatmap(x, y, s, bins=100):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent

if len(sys.argv) != 2 and sys.argv[1] != 'ERANGEL' and sys.argv[1] != 'MIRAMAR':
    raise Exception("Please take Game Map 'ERANGEL' or 'MIRAMAR' as argument.")

all_records = pd.read_csv('kill_match_stats_final_0.csv')

if sys.argv[1] == 'ERANGEL':
    title = "Final circle analysis of ERANGEL map"
    scale = 4096
    bg = imageio.imread('erangel.jpg')
    final_records_map1 = all_records.loc[(all_records['map'] == 'ERANGEL')&(all_records['victim_placement'] == 2)
                                            &(all_records['victim_position_x']>0)&(all_records['killer_position_x']>0), :].dropna()
    final_circle_pos = np.vstack([final_records_map1[['victim_position_x', 'victim_position_y']].values, 
                                    final_records_map1[['killer_position_x', 'killer_position_y']].values])*scale/800000
elif sys.argv[1] == 'MIRAMAR':
    title = "Final circle analysis of MIRAMAR map"
    scale = 1000
    bg = imageio.imread('miramar.jpg')
    final_records_map2 = all_records.loc[(all_records['map'] == 'MIRAMAR')&(all_records['victim_placement'] == 2)
                                            &(all_records['victim_position_x']>0)&(all_records['killer_position_x']>0), :].dropna()
    final_circle_pos = np.vstack([final_records_map2[['victim_position_x', 'victim_position_y']].values,
                                    final_records_map2[['killer_position_x', 'killer_position_y']].values])*scale/800000

hmap, extent = heatmap(final_circle_pos[:,0], final_circle_pos[:,1], 1.5)
alphas = np.clip(Normalize(0, hmap.max(), clip=True)(hmap)*1.5, 0.0, 1.)
colors = Normalize(0, hmap.max(), clip=True)(hmap)
colors = cm.Reds(colors)
colors[..., -1] = alphas

fig, ax = plt.subplots(figsize=(7,7))
ax.set_xlim(0, scale); ax.set_ylim(0, scale)
ax.imshow(bg)
ax.imshow(colors, extent=extent, origin='lower', cmap=cm.Reds, alpha=0.9)
plt.gca().invert_yaxis()
plt.title(title)
plt.show()