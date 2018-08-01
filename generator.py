import pmap as mp
import pdataset as ds


odataset = ds.PDataset('assets/eeuu_countries.dat')
omap = mp.PMap(odataset, 'merc', 'jet', 20, -130, 50, -60, 20, 'i')
omap.draw()