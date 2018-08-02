import random as ran
import pmap as mp
import pdataset as dset

class Generator(object):
    def __init__(self):
        pass

    def generate(self, projection, config,path_folder, filename ,print_parameters = False):

        ds = dset.PDataset(config['input_file'])

        is_quantized = True
        if config['color_maps']['continuous']:
            is_quantized = (ran.randint(0, 1) == 1)

        color_map = ran.choice(config['color_maps']['palette'])
        color_map_cax = (ran.randint(0, 1) == 1)
        color_map_shrink = ran.uniform(0.3, 1.0)
        color_map_orientation = ran.choice(['vertical', 'horizontal'])
        color_map_thickness = str(ran.randint(5, 15))+'%'
        color_map_pos = ran.choice(config['color_maps']['positions'])

        is_background = (ran.randint(0, 1) == 1)
        background = 'none'

        ocean_color = 'white'
        land_color = 'white'

        if is_background:
            background = ran.choice(config['background']['background'])
        else:
            ocean_color = ran.choice(config['background']['ocean_color'])
            if config['background']['land_colors'] == 'random':
                def r(): return ran.randint(0, 255)
                land_color = '#%02X%02X%02X' % (r(), r(), r())
            else:
                land_color = ran.choice(config['background']['land_colors'])

        quantized_val = 0

        if is_quantized:
            quantized_values = config['color_maps']['quantized']['nvalues']
            quantized_is_ranged = config['color_maps']['quantized']['isrange']
            if quantized_is_ranged:
                assert len(
                    quantized_values) == 2, 'if color_maps.quantized.isrange is true, color_maps.quantized.nvalues size must be 2'
                quantized_val = ran.randint(
                    quantized_values[0], quantized_values[1])
            else:
                quantized_val = ran.choice(quantized_values)

        ds.gen_noise_values()

        if config['basemap']['lon_0'] == 'auto':
            lon_0 = (ds.minLon + ds.maxLon)/2.0
        else:
            lon_0 = config['basemap']['lon_0']

        if config['basemap']['lat_0'] == 'auto':
            lat_0 = (ds.minLat + ds.maxLat)/2.0
        else:
            lat_0 = config['basemap']['lat_0']

        n_tick_lat = config['basemap']['n_tick_lat']
        n_tick_lon = config['basemap']['n_tick_lon']

        llcrnrlat = ran.randint(
            config['basemap']['llcrnrlat']['min'], config['basemap']['llcrnrlat']['max'])
        llcrnrlon = ran.randint(
            config['basemap']['llcrnrlon']['min'], config['basemap']['llcrnrlon']['max'])
        urcrnrlat = ran.randint(
            config['basemap']['urcrnrlat']['min'], config['basemap']['urcrnrlat']['max'])
        urcrnrlon = ran.randint(
            config['basemap']['urcrnrlon']['min'], config['basemap']['urcrnrlon']['max'])

        lat_ts = config['basemap']['lat_ts']
        resolution = config['basemap']['resolution']

        draw_coast_lines = (ran.randint(0, 1) == 1)
        draw_countries = (ran.randint(0, 1) == 1)
        draw_states = (ran.randint(0, 1) == 1)

        if print_parameters:
            print('projection', projection)
            print('color_map', color_map)
            print('llcrnrlat', llcrnrlat)
            print('llcrnrlon', llcrnrlon)
            print('urcrnrlat', urcrnrlat)
            print('urcrnrlon', urcrnrlon)
            print('lat_ts', lat_ts)
            print('resolution', resolution)
            print('lon_0', lon_0)
            print('lat_0', lat_0)
            print('n_quantized', quantized_val)
            print('draw_coast_lines', draw_coast_lines)
            print('draw_countries', draw_countries)
            print('draw_states', draw_states)
            print('background', background)
            print('ocean_color', ocean_color)
            print('land_color', land_color)
            print('color_map_pos', color_map_pos)
            print('color_map_cax', color_map_cax)
            print('color_map_shrink', color_map_shrink)
            print('color_map_orientation', color_map_orientation)
            print('color_map_thickness', color_map_thickness)


        oMap = mp.PMap(ds, projection, color_map, llcrnrlat,
                    llcrnrlon, urcrnrlat, urcrnrlon, lat_ts, resolution,
                    _lon_0=lon_0,
                    _lat_0=lat_0,
                    _n_tick_lat=n_tick_lat,
                    _n_tick_lon=n_tick_lon,
                    _n_quantized=quantized_val,
                    _draw_coast_lines=draw_coast_lines,
                    _draw_countries=draw_countries,
                    _draw_states=draw_states, 
                    _background=background, 
                    _ocean_color=ocean_color, 
                    _land_color=land_color, 
                    _color_map_pos=color_map_pos, 
                    _color_map_cax = color_map_cax, 
                    _color_map_shrink= color_map_shrink, 
                    _color_map_orientation = color_map_orientation, 
                    _color_map_thickness = color_map_thickness, _color_map_label = 'value')
        
        oMap.create()
        oMap.save_fig_bboxes(path_folder,filename)


