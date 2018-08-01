


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
    

extract('../assets/weather_forecasts_EU.dat', '../assets/eeuu_countries.dat')