import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl
import folium
from opencage.geocoder import OpenCageGeocode
# key = 'eb6b80413896491c882adeb4203d4aa8'
# key = 'd8cb447f8f7a4eccbdef25d14c3c69e2'
key = 'c17f6de615c24211850b949928c91bd5'
geocoder = OpenCageGeocode(key)


def find_info(data):
    """
    dict -> lst
    Returns the information about persons' nickname and they location.
    """
    lst = []
    for line in data['users']:
        var_l = [line['screen_name'], line['name'], line['location']]
        lst.append(var_l)
    return lst


def coordinates(data):
    """
    lst -> lst
    Returns the old info of the data
    and coordinates of the specified locations.
    """
    lst = []
    print('Map is creating, please wait!')
    for line in data:

        results = geocoder.geocode(line[-1])
        try:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
        except IndexError:
            continue
        lst.append([line[0], line[1], line[2], lat, lng])
    return lst


def creating_map(data):
    """
    lst -> str
    Returns the created map,
    which displays the analyzed information.
    """
    m = folium.Map(zoom_start=3)
    tooltip = '<b>Name<b>'
    fg = folium.FeatureGroup(name="markers")

    for i in data:
        popup = str(i[0]) + ' ' + str(i[1])
        folium.Marker(
            location=[i[-2], i[-1]],
            popup=popup,
            tooltip=tooltip,
            icon=folium.Icon(color='blue', icon='info-sign')).add_to(fg)
    fg.add_to(m)
    folium.LayerControl().add_to(m)
    m.save('twitter_friends_map.html')
    return 'Finished.'


def creating_app():
    """
    Create App and get the four strings, put them in hidden.py
    This app shows the location of friends twitter account.
    """
    twitter_url = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while True:
        print('')
        acct = input('Enter Twitter Account:')
        if len(acct) < 1:
            break
        url = twurl.augment(twitter_url,
                            {'screen_name': acct, 'count': '100'})
        print('Retrieving', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        j_read = json.loads(data)
        f_info = find_info(j_read)
        coo = coordinates(f_info)
        c_map = creating_map(coo)
        return c_map


if __name__ == '__main__':
    print(creating_app())
