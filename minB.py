import csv
import nvector as nv
from geopy.distance import vincenty
import googlemaps

def readcsv(filename):
    interviewcoords = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            interviewcoords.append(row)
    return interviewcoords

class Vertex:
    def __init__(self, lat, lon ):
        self.lat = lat
        self.lon = lon

def GetGeodeticMidpoint(vert1, vert2):
    """Given two Vertices, return the geodetic midpoint of the great circle arc between them, on the WGS84 ellipsoid. Uses nvector."""
    # see http://nvector.readthedocs.org/en/latest/src/overview.html?highlight=midpoint#description
    wgs84 = nv.FrameE(name='WGS84')
    n_EB_E_t0 = wgs84.GeoPoint(vert1.lat, vert1.lon, degrees=True).to_nvector()
    n_EB_E_t1 = wgs84.GeoPoint(vert2.lat, vert2.lon, degrees=True).to_nvector()
    path = nv.GeoPath(n_EB_E_t0, n_EB_E_t1)
    halfway = 0.5
    g_EB_E_ti = path.interpolate(halfway).to_geo_point()
    lat_ti, lon_ti = g_EB_E_ti.latitude_deg, g_EB_E_ti.longitude_deg
    return Vertex(float(lat_ti), float(lon_ti))

def get_locations(place):
    # Replace with a valid API key.
    gmaps = googlemaps.Client(key='')
    geocode_result = gmaps.geocode(place)
    print geocode_result
    NE = [geocode_result[0]["geometry"]["viewport"]["northeast"]["lat"],geocode_result[0]["geometry"]["viewport"]["northeast"]["lng"]]
    SW = [geocode_result[0]["geometry"]["viewport"]["southwest"]["lat"], geocode_result[0]["geometry"]["viewport"]["southwest"]["lng"]]
    # radius of minimum bounding circle of rectangle is half the diagonal
    radius = vincenty(NE, SW).meters/2
    # get midpoint of rectangle
    ne_bound = Vertex(lat=NE[0], lon=NE[1])
    sw_bound = Vertex(lat=SW[0], lon=SW[1])
    mp = GetGeodeticMidpoint(ne_bound, sw_bound)
    return [place, radius, mp.lat, mp.lon]


def save_csv(content):
    with open("bolivia.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(content)
    print "All done."


if __name__ == '__main__':
    f = 'p2.csv'
    mydata = readcsv(f)
    centroids =[["Place, Radius, Lat, Lon"]]
    for row in mydata:
        try:
            centroids.append(get_locations(row[0]))
        except:
            centroids.append([row[0], "Error", "Error", "Error"])
    save_csv(centroids)
