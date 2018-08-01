import random
from noise import snoise3


def get_noise(x, y, seed, freq):

    x = int(x)
    y = int(y)
    val = snoise3(x / freq, y / freq, seed )*10 + 11
    return val

class PDataset(object):

    def __init__(self, pathfile):

        self.lats = []
        self.lons = []
        self.__get_lat_log(pathfile)

    def __get_lat_log(self, pathfile):

        f = open(pathfile, 'r')
        contents = f.readlines()
        for line in range(1, len(contents)):
            line_split = contents[line].split(' ')
            lat, lon = line_split[0], line_split[1][:-1]
            self.lats.append(float(lat) )
            self.lons.append(float(lon) )
        
        f.close()

    def get_noise_values(self):

        seed = random.randint(1,255)
        freq = random.randint(10,30)
        lower = 999999
        upper = -999999
        values = []

        for i in range(0, len( self.lats )):
            val = get_noise(self.lats[i], self.lons[i] , seed, freq)
            values.append(val)
            lower = min(val, lower)
            upper = max(val, upper)
        
        return lower, upper, values


