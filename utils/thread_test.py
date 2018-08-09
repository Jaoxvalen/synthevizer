import threading
import time
import reverse_geocoder as rg

exitFlag = 0


class Task (threading.Thread):
    def __init__(self, minLon, maxLon, minLat, maxLat, step, id):
        threading.Thread.__init__(self)
        self.minLon = minLon
        self.maxLon = maxLon
        self.minLat = minLat
        self.maxLat = maxLat
        self.step = step
        self.id = id
        self.coords = []

    def run(self):
        lon = self.minLon
        lat = self.minLat
        step = self.step
        while lon <= self.maxLon:
            while lat <= self.maxLat:
                #print('id thread: ', self.id, ' lat: ', lat)
                coordinates = (lat, lon)
                results = rg.search(coordinates)
                name = results[0]['name']
                if name != 'Bayswater':
                    self.coords.append((coordinates))
                else:
                    print('water')
                lat = lat+step
            lat = self.minLat
            lon = lon+step
            print('id thread: ', self.id, ' lon: ', lon)


# Create new threads

minLon = -180.0
maxLon = 180.0
minLat = -85.0
maxLat = 85.0
step = 0.5
nThreads = 8

segment = (maxLon - minLon)/float(nThreads)

lsThreads = []

for i in range(nThreads):
    oThread = Task()
    lsThreads.append()


# thread1 = myThread(-180, -180, minLat, maxLat, step, 1)

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

# print(thread1.coords)
# print('----')
# print(thread2.coords)

# print("Exiting Main Thread")
