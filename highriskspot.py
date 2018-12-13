import pandas
import imageio
import numpy
from scipy.ndimage.filters import gaussian_filter
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import time


def heatmap(x, y, s, bins=100):
    heatmap, xedges, yedges = numpy.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent


def high_risk(map_name):
	title = "High-Risk Landing Spots"
	match_stats = pandas.read_csv('pubg-match-deaths/aggregate/agg_match_stats_0.csv')
	kill_stats = pandas.read_csv('pubg-match-deaths/deaths/kill_match_stats_final_0.csv')
	unique_matches = match_stats.loc[match_stats['party_size'] == 1, 'match_id'].unique()
	kills_solo = kill_stats[kill_stats['match_id'].isin(unique_matches)]
	death_180_seconds_erg = kills_solo.loc[(kills_solo['map'] == 'ERANGEL')&(kills_solo['time'] < 180)&(kills_solo['victim_position_x']>0), :].dropna()
	death_180_seconds_mrm = kills_solo.loc[(kills_solo['map'] == 'MIRAMAR')&(kills_solo['time'] < 180)&(kills_solo['victim_position_x']>0), :].dropna()
	data_erg = death_180_seconds_erg[['victim_position_x', 'victim_position_y']].values
	data_mrm = death_180_seconds_mrm[['victim_position_x', 'victim_position_y']].values
	data_erg = data_erg*4096/800000
	data_mrm = data_mrm*1000/800000
	if map_name == 'miramar':
		data = data_mrm
		map = 'miramar.jpg'
	elif map_name == 'erangle':
		data = data_erg
		map = 'erangle.jpg'
	else:
		raise Exception("invalid map name")
	hmap, extent = heatmap(data[:,0], data[:,1], 4.5)
	alphas = numpy.clip(Normalize(0, hmap.max(), clip=True)(hmap)*4.5, 0.0, 1.)
	colors = Normalize(0, hmap.max(), clip=True)(hmap)
	colors = cm.Reds(colors)
	colors[..., -1] = alphas
	fig, ax = plt.subplots(figsize=(24,24))
	ax.set_xlim(0, 1000); ax.set_ylim(0, 1000)
	bg = imageio.imread(map)
	ax.imshow(bg)
	ax.imshow(colors, extent=extent, origin='lower', cmap=cm.Reds, alpha=0.9)
	plt.gca().invert_yaxis()
	plt.title(title)
	time.sleep(2)
	plt.show()
