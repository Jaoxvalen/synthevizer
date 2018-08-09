from mpl_toolkits.basemap import Basemap

def gen_world_coords(fileoutput):

    minLon = -180.0
    maxLon = 180.0
    minLat = -85.0
    maxLat = 85.0
    step = 0.5

    lon = minLon
    lat = minLat

    fo = open(fileoutput,'w') 
    
    bm = Basemap(
        projection="merc",
        resolution = 'i', 
        llcrnrlon=-180.0, 
        llcrnrlat=-85.0,
        urcrnrlon=180.0, 
        urcrnrlat=85.0
    )

    while lon<=maxLon:
        while lat<=maxLat:
            x, y = bm(lon, lat)
            if bm.is_land(x, y):
                fo.writelines(str(lat)+ ' ' + str(lon) + '\n')
            lat = lat+step
        lat = minLat
        lon = lon+step
        print(lon)

    fo.close()

def extract(filename, fileoutput):
    
    f = open(filename, 'r')
    contents = f.readlines()

    fo = open(fileoutput,'w') 

    lat = ''
    lon = ''
    for line in range(1, len(contents)):
        line_split = contents[line].split(' ')
        if (line_split[0] != lat) or line_split[1] != lon:
            fo.writelines(line_split[0]+ ' ' + line_split[1] + '\n')
        lat, lon = line_split[0] , line_split[1]

    f.close()
    fo.close()
    

#extract('../assets/weather_forecasts_EU.dat', '../assets/eeuu_countries.dat')

gen_world_coords('../assets/world_land.dat')