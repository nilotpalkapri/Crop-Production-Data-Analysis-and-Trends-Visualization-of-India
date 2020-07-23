
import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import map_with_folium as mf
import trends_visualization as tv

st.title('🌾Crop Production Data Analysis and Trends Visualization of India🌾')
st.sidebar.header('🌾Crop Production Data Analysis and Trends Visualization of India🌾')
st.latex('Crop Production Data Analysis and Trends Visualization of India')
st.image('Decorator/crop_front.jpg', width=700)


#@st.cache(persist=True)
def load_data(url):
    df = pd.read_csv(url)
    return df


#@st.cache(persist=True)
def process_data():
    df2 = df.copy()
    df2['Address'] = (df2['District_Name']+', '+df2['State_Name'])
    df2 = df2.drop(['District_Name','State_Name'], axis=1)
    
    state_dist_lat = {}
    state_dist_long = {}
    for add in set(df2['Address']):#zip the required column of the main dataframe
        location = get_loc(add)
        state_dist_lat[add]= location.latitude
        state_dist_long[add]= location.longitude

    df2['Latitude'] = df2['Address'].map(state_dist_lat)
    df2['Longitude'] = df2['Address'].map(state_dist_long)
    
    return df2


#define function to retrive location data of a given dist, state.
def get_loc(address):
    geolocator = Nominatim(user_agent="ny_explorer")
    location = geolocator.geocode(address)
    if location is None: #check if the location is available for the given district and state
        locationd = geolocator.geocode(address.split(',')[0])
        locations = geolocator.geocode(address.split(',')[1])
        if locationd is None: #check if the district location is not available
            location = locations
        elif locations is None: #check if the state location is not available
            location = locationd
        elif (locationd is None) and (locations is None): #check if the dist and state location both not available
            location = geolocator.geocode('India')
        elif (abs(locations.latitude-locationd.latitude)>10) or (abs(locations.longitude-locationd.longitude)>10):
            location = locations
        else:
            location = locationd
    return location

url = 'crop_production.csv'
url2 = 'processed_data.csv'
df = load_data(url)
df2 = load_data(url2)
#df2=process_data()
#df2.to_csv('processed_data.csv', header=True, index=False)

user_options = st.sidebar.selectbox('Please Choose Your Goal', 
                                    [0,1,2,3], 
                                    index=0, 
                                    format_func=lambda x:['Select','Analyse and map all the datapoints using Folium library',
                                                          'Observe the Yearly Production Trends(State Wise)', 
                                                          'Select Both'][x])

if user_options==0:
    st.write('Please Choose an Option.')
elif user_options==1:
    mf.start(df2)
elif user_options==2:
    tv.start(df)
elif user_options==3:
    mf.start(df2)
    tv.start(df)





if st.sidebar.checkbox('Show Raw Data', False):
    sh = df.shape
    st.subheader('Raw Data')
    st.markdown('This Data Set Contains {} rows and {} columns.'.format(sh[0], sh[1]))
    st.write(df.head(100))
    st.balloons()
    
if st.sidebar.checkbox('Show Processed Data', False):
    sh1 = df2.shape
    st.subheader('Processed Data')
    st.markdown('This DataFrame is loaded with {} rows and {} columns.'.format(sh1[0], sh1[1]))
    st.write(df2.head(100))
    st.balloons()
