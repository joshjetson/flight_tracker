import json
import math
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st

#''' This program is intended to illustrate a specific use case of the streamlit platform.
#    It shows that you can create a real time web gui based flight tracking system using data provided by 
#    on board instruments from either a file or an api.
#    The application, in its current state,  simulates a flights possible path and updates the flights
#    position in real time. It provides the user with the distance of two airports, the average flight 
#    time between them and a map which they can simulate the flight on.'''
#------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Flight Tracker Simulator",
    page_icon="tv.png",
    layout="wide",
)
#The decorator is simply storing the functions return value in memory once.
#This makes the program run faster as it doesn't have to load these values each time the app runs.
#The json file is just a list of all airports in the U.S which fly to each other.
#I made this json file and formatted it in a specific way to make certain things easier in this program.
@st.experimental_memo
def from_to():
    with open('airports.json','r',encoding='utf-8') as o:
        return json.load(o)
fromto = from_to()
#The haversine function returns the distance in km and miles
#between two geographical long/lat locations on earth.
def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return (round(c * r), round(c * 3956))
#The midpoint function allows me to get the mid point location between two points by utilizing their respective latitudes and longitudes.
#I use the midpoint function to tell the map to center its camera between the two locations.
#This makes both locations viewable in the map window.
def midpoint(x1, x2, y1, y2):
#Input values as degrees

#Convert to radians
    lat1 = math.radians(x1)
    lon1 = math.radians(x2)
    lat2 = math.radians(y1)
    lon2 = math.radians(y2)
    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
           math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
           + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)
    return round(math.degrees(lat3), 2), round(math.degrees(lon3), 2)
#Here I load in a file containing more details on each airport including their geographical points.
#I use this file to create a data frame later on.
@st.experimental_memo
def raw_d():
    air_dir = 'us-airports.csv'
    return pd.read_csv(air_dir)
raw = raw_d()
#A list which will be populated with airport iata codes and the airports city.
airports = []
#A dictionary that will be used to grab an airports lat and lon a little easier.
lat_long = {}
#A loop which pulls out the specific data I need and leaves behind the unneeded stuff.
for x , y, z, lat, lng in zip(raw['region_name'], raw['municipality'], raw['iata_code'], raw['latitude_deg'], raw['longitude_deg']):
    if isinstance(z, str):
        airports.append(f'{x}, {y} ({z})')
        lat_long[f'{x}, {y} ({z})'] = [[lat, lng]]
#Easier to work with sorted list
airports = sorted(airports)
# Using object notation
#Select boxes which contain all of the airports a user can select
slct_bx_one = st.sidebar.selectbox(
    "Choose your departure airport",
    airports
)
slct_bx_two = st.sidebar.selectbox(
    "Choose your destination airport",
    airports
)
#This data frame is used because pydeck layers only work with data in a specific format.
#To note pydeck doesn't have a standardized method for every layer so you need to play around with the formats.
data = pd.DataFrame({
    'City_Airport' : [slct_bx_one, slct_bx_two],
    'lat' : [lat_long[slct_bx_one][0][0], lat_long[slct_bx_two][0][0]],
    'lon' : [lat_long[slct_bx_one][0][1], lat_long[slct_bx_two][0][1]],
    'profit':[1,1],
    'employees':[2000,300]
})
#Just stripping the iata airport codes so I can detect if two airports actually have flights
#from one another.
ap1 = slct_bx_one[slct_bx_one.find('(')+1:slct_bx_one.find(')')]
ap2 = slct_bx_two[slct_bx_two.find('(')+1:slct_bx_two.find(')')]
#This condition checks if two airports fly to each other.
#If they are in the fromto list ex.LAXLAS than I take the average flight time
#which I calculated from historical data (thousands of flights) from one of
#these airports to another.
if ap1+ap2 in fromto:
    d, m = divmod(fromto[ap1+ap2], 60)
    st.write('The average flight time from ', ap1, ' to ',ap2,' is ', round(d),' hours and', round(m), ' minutes')
    flights = True
else:
    st.write('Note: There are no direct flights between the selected airports.')
    flights = False
#The calculated distance in km and miles from one airport to another.
distance = haversine(data['lat'][0], data['lon'][0], data['lat'][1], data['lon'][1])
# Using "with" notation
with st.sidebar:
    st.write('Distance:', str(distance[1]), ' Miles')
    with st.container():
        pitch = st.slider('Angle', 0, 60, 25)
        bearing = st.slider('Orientation',0,360,0) 
#    add_radio = st.radio(
#        "some selection",
#        ("option 1", "option 2")
#)

mid = midpoint(data['lat'][0], data['lon'][0], data['lat'][1], data['lon'][1])
distance = haversine(data['lat'][0], data['lon'][0], data['lat'][1], data['lon'][1])
zoom = 2 if distance[1] > 2500 else 4 if distance[1] < 1400 and distance[1] > 500  else 5 if distance[1] < 500 else 3

view_state = pdk.ViewState(latitude=mid[0],longitude=mid[1],zoom=zoom,bearing=bearing,pitch=pitch)

arc_data = [{"name": slct_bx_one,"color": "#ed1c24","path": [[lat_long[slct_bx_one][0][1],lat_long[slct_bx_one][0][0]],
    [lat_long[slct_bx_two][0][1],lat_long[slct_bx_two][0][0]]]
  },{"name": slct_bx_two,"color": "#faa61a","path": [[lat_long[slct_bx_two][0][1],lat_long[slct_bx_two][0][0]],
    [lat_long[slct_bx_one][0][1],lat_long[slct_bx_one][0][0]]]}
    ]
with st.sidebar:
    btn = st.button('Simulate Flight Path')
spdata = {'location':[lat_long[slct_bx_one][0][1],lat_long[slct_bx_one][0][0]],
           'destination':[lat_long[slct_bx_two][0][1],lat_long[slct_bx_two][0][0]] }
placeholder = st.empty()
dc, dcp = .00001, 5
o_lon, o_lat, d_lon, d_lat = spdata['location'][0],spdata['location'][1],spdata['destination'][0],spdata['destination'][1]
reset = [o_lon, o_lat]
rnd = lambda ln_lt,sign: np.round(ln_lt + dc,decimals=dcp) if sign == '+' else np.round(ln_lt - dc, decimals=dcp)
def rnd_rng(cln_clt,sign):
    if sign == '+':
        return np.fromiter((np.round(cln_clt + (x * dc), decimals=dcp) for x in np.arange(5000)),dtype=float)
    return np.fromiter((np.round(cln_clt - (x * dc), decimals=dcp) for x in np.arange(5000)),dtype=float)
d_lon, d_lat = rnd(d_lon,'-'), rnd(d_lat,'-')
spdata = pd.DataFrame(spdata)
arc_data = pd.DataFrame(arc_data)
switch = False
def run_it(o_lon=o_lon, o_lat=o_lat):
    global switch
    lon_range , lat_range = [o_lon],[o_lat]
    GREEN_RGB = [255, 255, 20, 180]
    RED_RGB = [238, 130, 238, 180]
    rad = 30000 if zoom == 5 else 40000 if zoom == 4 else 70000 if zoom == 3 else 80000
    if switch and o_lon != d_lon:
        current_lon = rnd(o_lon, '+') if o_lon < d_lon else rnd(o_lon, '-')
        lon_range = rnd_rng(current_lon,'+') if o_lon < d_lon else rnd_rng(current_lon, '-')
    if switch and o_lat != d_lat:
        current_lat = rnd(o_lat, '+') if o_lat < d_lat else rnd(o_lat, '-')
        lat_range = rnd_rng(current_lat, '+') if o_lat < d_lat else rnd_rng(current_lat, '-')
    if switch and o_lon != d_lon or o_lat != d_lat:
        if o_lon != d_lon:
            o_lon = lon_range[-1] if d_lon not in lon_range else d_lon
        if o_lat != d_lat:
            o_lat = lat_range[-1] if d_lat not in lat_range else d_lat
    with placeholder.container():
        #  st.write(o_lon,d_lon,o_lat,d_lat, switch)
        layer_g = pdk.Layer(type='HeatmapLayer',data=data,opacity=0.1,get_position=['lon','lat'],get_weight='profit / employees > 0 ? profit / employees : 0')
        layer_c = pdk.Layer(type='ScatterplotLayer',data=spdata,get_position=[o_lon, o_lat],get_color=[200, 30, 0, 160], get_radius=rad)
        layer_d = pdk.Layer(type='ArcLayer',data=arc_data,get_width=5,get_source_position='path[0]',get_target_position='path[1]', get_tilt=0,get_source_color=RED_RGB, get_target_color=GREEN_RGB,pickable=True, auto_highligh=True)
        r = pdk.Deck(map_style='mapbox://styles/mapbox/navigation-night-v1',layers=[layer_d, layer_c, layer_g], initial_view_state=view_state, tooltip={'text': '{name}'})
        map_ = st.pydeck_chart(r)
    #This is the peculiar bit. Without the if not condition streamlit simply ignores the if switch condition
    #and proceeds to run the code inside the condition even though the condition is not met. I tested alot!
    #I am still confused as to what exactly is going on and why it happens.
    if not switch:
        return
    if switch and o_lon != d_lon or o_lat != d_lat:
        #Many ways of achieving this. I chose recursion after trying a for and while loop.
        return run_it(o_lon, o_lat)
    if o_lon == d_lon and o_lat == d_lat:
        with st.sidebar:
            st.write('You have reached your destination')
        switch = False
        o_lon, o_lat = reset[0], reset[1]
        return o_lon, o_lat
    return
if not flights:
    with st.sidebar:
        st.write('There are no direct flights between these two airports')
if btn and flights:
    switch = True
    run_it()
elif not btn:
    run_it()
