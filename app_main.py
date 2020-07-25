
import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import webbrowser
from ipywidgets import Button, Layout, jslink, IntText, IntSlider


import map_with_folium as mf
import trends_visualization as tv

st.markdown("""<h1 align="center" style="color:DarkGreen;">
            🌾Crop Production Data Analysis and Trends Visualization of India🌾</h1>""", 
            unsafe_allow_html=True)
st.sidebar.markdown("""<h1 align="center" style="color:DarkGreen;">
                    🌾Crop Production Data Analysis and Trends Visualization of India🌾</h1>""", 
                    unsafe_allow_html=True)

#st.title('🌾Crop Production Data Analysis and Trends Visualization of India🌾')
#st.sidebar.header('🌾Crop Production Data Analysis and Trends Visualization of India🌾')
#st.latex('Crop Production Data Analysis')
st.image('Decorator/crop_front.jpg', use_column_width=True)
st.sidebar.image('Decorator/crop_front.jpg', use_column_width=True)

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

url = 'Datasets/crop_production.csv'
url2 = 'Datasets/processed_data.csv'
df = load_data(url)
df2 = load_data(url2)
#df2=process_data()
#df2.to_csv('processed_data.csv', header=True, index=False)

user_options = st.selectbox('Choose Your Goal', 
                        [0,1,2,3], 
                        index=0, 
                        format_func=lambda x:['Select','Analyse and map all the datapoints using Folium library',
                                                  'Observe the Yearly Production Trends(State Wise)', 
                                                  'Select Both'][x])



if user_options==0:
    st.write('Please Select an Option.')
elif user_options==1:
    st.markdown('Please Choose Parameters from Sidebar and Click Proceed.')
    mf.start(df2)
elif user_options==2:
    st.markdown('Please Choose Parameters from Sidebar and Click Proceed.')
    tv.start(df)
elif user_options==3:
    st.markdown('Please Choose Parameters from Sidebar and Click Proceed.')
    mf.start(df2)
    tv.start(df)



    
    
    
    
    

    
if st.button('Watch Demo Video'):
    st.video('https://youtu.be/ubvwYLdHqAM')
    
if st.sidebar.checkbox('Show Raw Data', False):
    sh = df.shape
    st.subheader('Raw Data')
    st.markdown('This Data Set Contains {} rows and {} columns.'.format(sh[0], sh[1]))
    st.write(df.head(100))
    st.success('Success!')
    st.balloons()
    
if st.sidebar.checkbox('Show Processed Data', False):
    sh1 = df2.shape
    st.subheader('Processed Data')
    st.markdown('This DataFrame is loaded with {} rows and {} columns.'.format(sh1[0], sh1[1]))
    st.write(df2.head(100))
    st.success('Success!')
    st.balloons()
    
if user_options==0:
    for i in range(7):
        st.sidebar.text(' ')
        
if user_options==0 or st.sidebar.button('Watch Demo GIF'):
    st.image('Decorator/app_demo.gif',use_column_width=True)

st.sidebar.text('©nilotpal')

#Social connections
st.sidebar.markdown("""
                <!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<center><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
.fa {
  width: 15px;
  height: 15px;
  display: inline-block;
  padding: 20px;
  font-size: 20px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;  
  border: none;
  border-radius: 50%
}

</style>
</head>
<body><center>

<!--<h2>Style Social Media Buttons</h2>-->

<!-- Add font awesome icons -->


<!-- <h2>Image Links</h2>

<p>The image is a link. You can click on it.</p> -->


<!--
<a href="https://wa.me/+918159853451" target="_blank">
  <img src="https://cdn0.iconfinder.com/data/icons/tuts/256/whatsapp.png" 
  alt="Whatsapp" style="width:25px;height:25px;border:0">
</a> -->

<a href="https://www.facebook.com/nilu.kapri/" target="_blank">
  <img src="https://cdn4.iconfinder.com/data/icons/free-social-media-icons/512/Facebook.png" 
  alt="Facebook" style="width:22px;height:22px;border:0">
</a>

<a href="https://instagram.com/Nilotpal__Kapri" target="_blank">
  <img src="https://cdn4.iconfinder.com/data/icons/social-media-2146/512/25_social-256.png" 
  alt="Instagram" style="width:22px;height:22px;border:0">
</a> 

<a href="https://m.me/106286494269703" target="_blank">
  <img src="https://cdn3.iconfinder.com/data/icons/social-media-2068/64/_Facebook_Messenger-512.png" 
  alt="Messenger" style="width:22px;height:22px;border:0">
</a>

<a href="https://twitter.com/nilotpalkapri" target="_blank">
  <img src="https://cdn3.iconfinder.com/data/icons/social-media-2068/64/_Twitter-256.png" 
  alt="Twitter" style="width:23px;height:23px;border:0">
</a>

<a href="https://www.youtube.com/channel/UCe_4uLTNbOvhJGHRVqqbHeQ" target="_blank">
  <img src="https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Youtube_colored_svg-512.png" 
  alt="YouTube" style="width:22px;height:25px;border:0">
</a>

<a href="mailto:nilotpal623401@gmail.com" target="_blank">
  <img src="https://cdn2.iconfinder.com/data/icons/once-again/48/Gmail.png" 
  alt="Mail" style="width:25px;height:25px;border:0">
</a>

<a href="https://www.linkedin.com/in/nilotpalkapri" target="_blank">
  <img src="https://cdn4.iconfinder.com/data/icons/free-social-media-icons/256/LinkedIn.png" 
  alt="Linkedin" style="width:22px;height:22px;border:0">
</a>

<a href="https://github.com/nilotpalkapri/" target="_blank">
  <img src="https://cdn4.iconfinder.com/data/icons/miu-hexagon-shadow-social/60/github-hexagon-shadow-social-media-256.png" 
  alt="Whatsapp" style="width:25px;height:25px;border:0">
</a>

<a href="https://independent.academia.edu/nilotpalkapri" target="_blank">
  <img src="https://image.flaticon.com/icons/png/512/25/25645.png" 
  alt="Academia" style="width:22px;height:22px;border:0">
</a>
<a href="https://orcid.org/0000-0001-7803-5957" target="_blank">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/ORCID_iD.svg/768px-ORCID_iD.svg.png" 
  alt="Orcid" style="width:23px;height:23px;border:0">
</a>
<a href="https://www.mendeley.com/profiles/nilotpal-kapri/" target="_blank">
  <img src="https://www.pinclipart.com/picdir/middle/568-5689345_2048-black-logo-mendeley-kecil-png-clipart.png" 
  alt="Mendeley" style="width:22px;height:21px;border:0">
</a>

<!-- <p>We have added "border:0" to prevent IE9 (and earlier) from displaying a border around the image.</p> </p> -->


 </center>     
</body>
</html>

                """, unsafe_allow_html=True
                )
    
