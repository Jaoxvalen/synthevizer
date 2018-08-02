import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pbbox as pbbox



class PMap(object):

    def __init__(self,
                 _data, _projection,
                 _color_map, _llcrnrlat,
                 _llcrnrlon, _urcrnrlat, _urcrnrlon, _lat_ts, _resolution, _lon_0=0, _lat_0=0,  _n_tick_lat=6, _n_tick_lon=8,
                 _n_quantized=0, _draw_coast_lines=True, _draw_countries=False, _draw_states=True,
                 _background='none',
                 _ocean_color='white',
                 _land_color='white',
                 _color_map_pos='right', _color_map_cax=False, _color_map_shrink=0.5, _color_map_orientation='vertical',
                 _color_map_thickness='5%', _color_map_label='value'):

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
        self.n_tick_lat = _n_tick_lat
        self.n_tick_lon = _n_tick_lon
        self.lon_0 = _lon_0
        self.lat_0 = _lat_0
        self.color_map_pos = _color_map_pos
        self.color_map_cax = _color_map_cax
        self.color_map_shrink = _color_map_shrink
        self.color_map_orientation = _color_map_orientation
        self.color_map_thickness = _color_map_thickness
        self.color_map_label = _color_map_label
        self.background = _background
        self.land_color = _land_color
        self.ocean_color = _ocean_color

        if _n_quantized != 0:
            self.color_map = plt.cm.get_cmap(_color_map, _n_quantized)
        else:
            self.color_map = plt.cm.get_cmap(_color_map)

    def create(self):

        mpl.rcParams.update({'font.size': 8})

        if self.projection == 'moll':
            step_tick_lat = 30.0
            step_tick_lon = 60.0

        else:
            step_tick_lat = int(
                (self.urcrnrlat - self.llcrnrlat) / self.n_tick_lat)
            step_tick_lon = int(
                (self.urcrnrlon - self.llcrnrlon) / self.n_tick_lon)

        self.basemap = Basemap(projection=self.projection, llcrnrlat=self.llcrnrlat, urcrnrlat=self.urcrnrlat,
                               llcrnrlon=self.llcrnrlon, urcrnrlon=self.urcrnrlon, lat_ts=self.lat_ts, lon_0=self.lon_0, lat_0=self.lat_0, resolution=self.resolution)

        if self.draw_coast_lines:
            self.basemap.drawcoastlines()
        if self.draw_countries:
            self.basemap.drawcountries()
        if self.draw_states:
            self.basemap.drawstates()

        if self.background == 'bluemarble':
            self.basemap.bluemarble()
        elif self.background == 'shadedrelief':
            self.basemap.shadedrelief()
        elif self.background == 'etopo':
            self.basemap.etopo()
        else:
            self.basemap.drawlsmask(
                land_color=self.land_color, ocean_color=self.ocean_color, lakes=True)

        parallels = np.arange(-90., 91., step_tick_lat)
        meridians = np.arange(-180., 181., step_tick_lon)

        self.fig_parallels = self.basemap.drawparallels(
            parallels, labels=[True, False, False, True])
        self.fig_meridians = self.basemap.drawmeridians(
            meridians, labels=[True, False, False, True])

        x, y = self.basemap(self.data.lons, self.data.lats)

        sc = plt.scatter(x, y, c=self.data.temp, vmin=self.data.lower,
                         vmax=self.data.upper, cmap=self.color_map, s=20, edgecolors='none')

        if self.color_map_cax:

            if self.color_map_pos == 'top':
                orientation = 'horizontal'
                pad = '30%'
            elif self.color_map_pos == 'bottom':
                orientation = 'horizontal'
                pad = '10%'
            elif self.color_map_pos == 'right':
                orientation = 'vertical'
                pad = '15%'
            elif self.color_map_pos == 'left':
                orientation = 'vertical'
                pad = '30%'

            divider = make_axes_locatable(plt.gca())
            cax = divider.append_axes(
                position=self.color_map_pos, size=self.color_map_thickness, pad=pad)

            cbar = plt.colorbar(sc, cax=cax, orientation=orientation)

        else:
            cbar = plt.colorbar(sc, shrink=self.color_map_shrink,
                                orientation=self.color_map_orientation, pad=0.1)


        cbar.set_label(self.color_map_label)

        self.cbar = cbar
        

    #save the figure and bboxes
    def save_fig_bboxes(self, pathfile, name_fig):

        plt.gcf().canvas.draw()

        fig = plt.gcf()
        size = fig.get_size_inches()*fig.dpi


        lsbbox = []
        lspara = list(self.fig_parallels.values())
        lsmeri = list(self.fig_meridians.values())

        for l in lspara:
            if len(l[1]) > 0:
                o = l[1][0].get_window_extent()
                obbox = pbbox.Pbbox(o.x0, size[1]-o.y0, o.x1, size[1]-o.y1, l[1][0].get_text(), 'lat_label')
                lsbbox.append(obbox)

        for l in lsmeri:
            if len(l[1]) > 0:
                o = l[1][0].get_window_extent()
                obbox = pbbox.Pbbox(o.x0, size[1]-o.y0, o.x1, size[1]-o.y1, l[1][0].get_text(), 'lon_label')
                lsbbox.append(obbox)

        for l in self.cbar.ax.get_yticklabels():
            o = l.get_window_extent()
            obbox = pbbox.Pbbox(o.x0, size[1]-o.y0, o.x1, size[1]-o.y1, l.get_text(), 'legend_tick_label')
            lsbbox.append(obbox)
        
        for l in self.cbar.ax.get_xticklabels():
            o = l.get_window_extent()
            obbox = pbbox.Pbbox(o.x0, size[1]-o.y0, o.x1, size[1]-o.y1, l.get_text(), 'legend_tick_label')
            lsbbox.append(obbox)

        #color bar legend
        o = self.cbar.ax.get_window_extent()
        obbox = pbbox.Pbbox(o.x0, size[1]-o.y0, o.x1, size[1]-o.y1, '', 'legend')
        lsbbox.append(obbox)

        llabel = self.cbar.ax.yaxis.get_label()

        if len(llabel.get_text())>0:
            o = llabel.get_window_extent()
            obbox = pbbox.Pbbox(o.x0, size[1]-o.y0, o.x1, size[1]-o.y1, llabel.get_text(), 'legend_label')
            lsbbox.append(obbox)
 
        llabel = self.cbar.ax.xaxis.get_label()

        if len(llabel.get_text())>0:
            o = llabel.get_window_extent()
            obbox = pbbox.Pbbox(o.x0, size[1]-o.y0, o.x1, size[1]-o.y1, llabel.get_text(), 'legend_label')
            lsbbox.append(obbox)

        
        path = pathfile+name_fig

        plt.savefig(path+'.png')

        fout = open(path+'.json','w')

        i = 0
        fout.writelines('{"bboxes":[')
        for bbox in  lsbbox:
            if i == len(lsbbox)-1:
                fout.writelines('{"type":"'+bbox.typeb+'","text":"'+bbox.text+'","x0":'+str(bbox.x0)+',"y0":'+str(bbox.y0)+',"x1":'+str(bbox.x1)+',"y1":'+str(bbox.y1) +'}\n')
            else:
                fout.writelines('{"type":"'+bbox.typeb+'","text":"'+bbox.text+'","x0":'+str(bbox.x0)+',"y0":'+str(bbox.y0)+',"x1":'+str(bbox.x1)+',"y1":'+str(bbox.y1) +'},\n')
            i+=1

        fout.writelines(']}')
        fout.close()

        #plt.gcf().clear()
        plt.clf()
        plt.cla()
        plt.close()
