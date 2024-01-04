

# ------------------------ Try cartopy pcolourmesh - THIS WORKS THE BEST ------------------------------------------
# NB lat and lon vectors have to be +1 the dims of the data matrix because they represent the corners
# see https://scitools.org.uk/cartopy/docs/v0.13/matplotlib/advanced_plotting.html

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from matplotlib import colormaps
import matplotlib as mpl


# First get the loactions of the cell corners
#degrees = 2.5 # Step size -- resolution of grid

#start = -180  # Starting number
#end = 180   # Ending number (adjust as needed)
#cornerlons = [start + i * degrees for i in range(int((end - start) / degrees) + 1)]

#start = -90  # Starting number
#end = 90   # Ending number (adjust as needed)
#cornerlats = [start + i * degrees for i in range(int((end - start) / degrees) + 1)]
    
# Read in the data    
shp_df_sum_grid = pd.read_csv("/home/dveytia/test-mordecai/outputs/geoparsed-text_grid-sums.csv")
gridlons = shp_df_sum_grid.LON.unique()
gridlats = shp_df_sum_grid.LAT.unique()
shape = (len(gridlats), len(gridlons))
n = np.array(shp_df_sum_grid.n_articles_weighted).reshape(shape)

# make matrices of lons

# quick check
plt.imshow(n, cmap='viridis')
plt.colorbar()
plt.show()


# set up a map
fig=plt.figure()
ax = plt.axes(projection=ccrs.Robinson())

#plt.pcolormesh(cornerlons, cornerlats, n,
#              cmap=colormaps['magma_r'], norm=mpl.colors.LogNorm(), transform=ccrs.PlateCarree()) 

# Can use the regular grid lons and lats with the shading ='nearest' option
im = plt.pcolormesh(gridlons, gridlats, n, shading = 'nearest',
              cmap=colormaps['magma_r'], norm=mpl.colors.LogNorm(), transform=ccrs.PlateCarree()) 

ax.coastlines()

## Colourbar
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])
cbar = plt.colorbar(im, cax=cax) 
cbar.ax.get_yaxis().labelpad = 15
cbar.set_label('Weighted # of articles', rotation=270)


plt.savefig(f'/home/dveytia/test-mordecai/figures/geoparsed-text-map.pdf',bbox_inches="tight") # Save plot, change file path and name
plt.show()


# ------------------------ Try cartopy pcolourmesh multipanel ------------------------------------------

## THIS NEEDS FIXING
# Read in the data    
shp_df_sum_grid = pd.read_csv("/home/dveytia/test-mordecai/outputs/geoparsed-text_grid-sums.csv")
gridlons = shp_df_sum_grid.LON.unique()
gridlats = shp_df_sum_grid.LAT.unique()
shape = (len(gridlats), len(gridlons))
n = np.array(shp_df_sum_grid.n_articles).reshape(shape)


## set up a map
fig, ax = plt.subplots(nrows=1, ncols=2, figsize = (10,10))

# Panel 0
ax[0].set_title("a) Research affiliation", y=1.0, pad = 20)
plt.axes(projection=ccrs.Robinson())
ras = plt.pcolormesh(gridlons, gridlats, n, shading = 'nearest',
              cmap=colormaps['magma_r'], norm=mpl.colors.LogNorm(), transform=ccrs.PlateCarree()) 
ax[0].coastlines()

# Panel 1
ax[1].set_title("b) Geoparsed locations", y=1.0, pad = 20)
plt.axes(projection=ccrs.Robinson())
ras = plt.pcolormesh(gridlons, gridlats, n, shading = 'nearest',
              cmap=colormaps['magma_r'], norm=mpl.colors.LogNorm(), transform=ccrs.PlateCarree()) 
ax[1].coastlines()

# Plot the colourbar
cbar_ax = fig.add_axes([0, 0.275, 0.02, 0.45])
cb = fig.colorbar(ras, cax=cbar_ax, label='Number of articles')
#levels = np.arange(0,50,10)
#cb.ax.yaxis.set_ticks(levels)
#cbar_ax.set_yticklabels(levels) 
#cb.ax.yaxis.set_ticks_position('left')
#cb.ax.yaxis.set_label_position('left')

ax[1].set_axis_off()

plt.show()

plt.savefig(f'/home/dveytia/test-mordecai/figures/geoparsed-text-map.pdf',bbox_inches="tight") # Save plot, change file path and name




############# OTHER METHODS ############


# -------------------------------------Try iris and basemap ------------------------------------------
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import geopandas as gpd
import shapely
from descartes import PolygonPatch
import pandas as pd
from shapely.geometry import Point, Polygon


## read in dataframe of grid matches
shp_df_sum_grid = pd.read_csv("/home/dveytia/test-mordecai/outputs/geoparsed-text_grid-sums.csv")


fig, ax = plt.subplots(nrows=1, ncols=1)

m = Basemap(
    ax = ax,
    projection='robin',lon_0=0,
    resolution='i',round=True
)  

m.drawcoastlines()

## Transform dataframe to projection 
xy = m(shp_df_sum_grid['LON'],shp_df_sum_grid['LAT'])
z = shp_df_sum_grid['n_articles']

    

## Plot the interpolated result
cont = m.pcolormesh(shp_df_sum_grid['LON'],shp_df_sum_grid['LAT'],shp_df_sum_grid['n_articles'], cmap = 'viridis', latlon=True)  # set my own breaks


# plot the colourbar
cbar_ax = fig.add_axes([0.1, 0.275, 0.02, 0.45])
cb = fig.colorbar(cont, cax=cbar_ax, label='Number of articles')
levels = np.arange(0,2700,10)
cb.ax.yaxis.set_ticks(levels)
cbar_ax.set_yticklabels(levels) 
cb.ax.yaxis.set_ticks_position('left')
cb.ax.yaxis.set_label_position('left')


# Title
ax.set_title("Gridded locations", y=1.0, pad=30)

# Continents
m.fillcontinents()
plt.show()



# ---------------------- Using EOmaps -----------------
# https://eomaps.readthedocs.io/en/latest/api_data_visualization.html
from eomaps import Maps
import pandas as pd

shp_df_sum_grid = pd.read_csv("/home/dveytia/test-mordecai/outputs/geoparsed-text_grid-sums.csv")

shp_df_sum_grid = pd.read_csv("/home/dveytia/test-mordecai/outputs/geoparsed-text_grid-sums.csv")
gridlons = shp_df_sum_grid.LON.unique()
gridlats = shp_df_sum_grid.LAT.unique()
shape = (len(gridlats), len(gridlons))
n = np.array(shp_df_sum_grid.n_articles).reshape(shape)

m = Maps(Maps.CRS.Mollweide(), figsize=(8,4))
m.set_data(np.transpose(n), x=gridlons, y=gridlats, parameter="number of articles", crs=4326)
m.add_feature.preset.coastline() # THIS FREEZES
m.set_shape.raster()  
m.plot_map(cmap="viridis", zorder=1, vmin=1, vmax=500)    
# DO I WANT TO MAKE SURE THAT THE COLOURS ARE DIVIDED/WEIGHTED BY TOTAL AREA OF THE COVERAGE?