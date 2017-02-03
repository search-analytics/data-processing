import json
import urllib2
import sys


def get_geopoint(location_name, url):
    geoservice_url = url + "/api/search?s="
    location_name = location_name.strip().split(" ")
    if len(location_name)>1 :
        location_name = [x[0].upper() + x[1:].lower() for x in location_name]
        location_name = ' '.join(location_name)
    else:
        location_name = location_name[0]
        location_name = [location_name[0].upper()] + [x.lower() for x in location_name[1:]]
        location_name = ''.join(location_name)
    data = json.loads(str(urllib2.urlopen(geoservice_url + location_name.replace(" ", "%20")).read()))
    return data

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage <location string> <host:port for geo-gazetteer> \n Example 'New Brunswick' 'http://localhost:8765'"
        exit()
    location = sys.argv[1]
    url = sys.argv[2]

    data = get_geopoint(location, url)
    print data