# First we load our location data and drop any duplicated places within documents
import pandas as pd
import os
import pandas as pd
import warnings
import numpy as np
import cartopy.crs as ccrs
import geopandas
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colormaps


## read in dataframe of grid matches
shp_df_sum_grid = pd.read_csv("/home/dveytia/test-mordecai/outputs/geoparsed-text_grid-sums.csv")

## Plot
#fig = plt.figure(dpi=150)
ax = plt.axes(projection=ccrs.Robinson())
ax.coastlines(lw=0.2)


shape = (len(shp_df_sum_grid.LAT.unique()), len(shp_df_sum_grid.LON.unique()))
n = np.array(shp_df_sum_grid.n_articles).reshape(shape)
mesh=ax.pcolormesh(
    shp_df_sum_grid.LON.unique(), 
    shp_df_sum_grid.LAT.unique(), 
    n, 
    cmap=colormaps['magma_r'],
    norm=mpl.colors.LogNorm(),
    transform=ccrs.PlateCarree(),
)

# plt.colorbar(c)

#plt.savefig(f'/home/dveytia/test-mordecai/figures/geoparsed-text-map.pdf',bbox_inches="tight") # Save plot, change file path and name
