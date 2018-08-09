import random
from noise import snoise3

_MAX = 999999
_MIN = -999999

def get_noise(x, y, seed, freq):

    x = int(x)
    y = int(y)
    val = snoise3(x / freq, y / freq, seed )*10 + 11
    return val

class PDataset(object):

    

    def __init__(self, pathfile):

        self.lats = []
        self.lons = []
        self.temp = []
        self.__reset_lu()
        self.minLat = _MAX
        self.maxLat = _MIN
        self.minLon = _MAX
        self.maxLon = _MIN
        self.__get_lat_log(pathfile)
        #self.__get_lat_lon_world()

    def __get_lat_log(self, pathfile):

        f = open(pathfile, 'r')
        contents = f.readlines()
        for line in range(1, len(contents)):
            line_split = contents[line].split(' ')
            lat, lon = line_split[0], line_split[1][:-1]

            val_lat = float(lat)
            val_lon = float(lon)

            self.lats.append( val_lat )
            self.lons.append( val_lon )

            self.minLat = min(val_lat, self.minLat)
            self.maxLat = max(val_lat, self.maxLat)

            self.minLon = min(val_lon, self.minLon)
            self.maxLon = max(val_lon, self.maxLon)
        
        f.close()

    
    def __reset_lu(self):
        self.lower = _MAX
        self.upper = _MIN

    def gen_noise_values(self):

        self.temp=[]

        seed = random.randint(1,255)
        freq = random.randint(10,30)
        self.__reset_lu()

        for i in range(0, len( self.lats )):
            val = get_noise(self.lats[i], self.lons[i] , seed, freq)
            self.temp.append(val)
            self.lower = min(val, self.lower)
            self.upper = max(val, self.upper)


        



