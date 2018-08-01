import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


class PMap(object):

    def __init__(self, _data, _projection, _color_map, _llcrnrlat,
                 _llcrnrlon, _urcrnrlat, _urcrnrlon, _lat_ts, _resolution,
                 _n_quantized=0, _draw_coast_lines=True, _draw_countries=False, _draw_states=True):

        self.projection = _projection
        self.llcrnrlat = _llcrnrlat
        self.urcrnrlat = _urcrnrlat
        self.llcrnrlon = _llcrnrlon
        self.urcrnrlon = _urcrnrlon
        self.lat_ts = _lat_ts
        self.resolution = _resolution
        self.n_quantized = _n_quantized
        self.draw_coast_lines = _draw_coast_lines
        self.draw_countries = _draw_countries
        self.draw_states = _draw_states
        self.data = _data
        self.color_map = plt.cm.get_cmap(_color_map)

    def draw(self):

        self.basemap = Basemap(projection=self.projection, llcrnrlat=self.llcrnrlat, urcrnrlat=self.urcrnrlat,
                               llcrnrlon=self.llcrnrlon, urcrnrlon=self.urcrnrlon, lat_ts=self.lat_ts, resolution=self.resolution)

        if self.draw_coast_lines:
            self.basemap.drawcoastlines()
        if self.draw_countries:
            self.basemap.drawcountries()
        if self.draw_states:
            self.basemap.drawstates()

        parallels = np.arange(-90., 91., 5.)
        meridians = np.arange(-180., 181., 10.)

        self.fig_parallels = self.basemap.drawparallels(
            parallels, labels=[True, False, False, True])
        self.fig_meridians = self.basemap.drawmeridians(
            meridians, labels=[True, False, False, True])

        self.basemap.drawmapboundary(fill_color='white')

        x, y = self.basemap(self.data.lons , self.data.lats)

        l, u, temperature = self.data.get_noise_values()

        sc = plt.scatter(x, y, c=temperature, vmin=l,
                         vmax=u, cmap=self.color_map, s=20, edgecolors='none')

        cbar = plt.colorbar(sc, shrink=.5)
        cbar.set_label('value')
        plt.show()
