
import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import webbrowser
from ipywidgets import Button, Layout, jslink, IntText, IntSlider


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
<a href="https://wa.me/+918159853451">
  <img src="https://www.stickpng.com/assets/images/580b57fcd9996e24bc43c543.png" alt="Whatsapp" style="width:25px;height:25px;border:0">
</a> -->

<a href="https://www.facebook.com/nilu.kapri/">
  <img src="http://img2.wikia.nocookie.net/__cb20140429004607/jamescameronstitanic/images/4/4a/Facebook_favicon.png" alt="Facebook" style="width:22px;height:22px;border:0">
</a>

<a href="https://instagram.com/Nilotpal__Kapri">
  <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width:22px;height:22px;border:0">
</a> 

<a href="https://m.me/106286494269703">
  <img src="https://maxcdn.icons8.com/Share/icon/Logos/facebook_messenger1600.png" alt="Messenger" style="width:25px;height:25px;border:0">
</a>

<a href="https://twitter.com/nilotpalkapri">
  <img src="https://low-carb-scams.com/wp-content/uploads/2014/04/Twitter-Bird-Logo.png" alt="Twitter" style="width:25px;height:25px;border:0">
</a>

<a href="https://www.youtube.com/channel/UCe_4uLTNbOvhJGHRVqqbHeQ">
  <img src="https://image.flaticon.com/icons/svg/174/174883.svg" alt="YouTube" style="width:22px;height:22px;border:0">
</a>

<a href="mailto:nilotpal623401@gmail.com">
  <img src="https://www.freepngimg.com/download/gmail/66419-account-google-icons-computer-email-gmail.png" alt="Mail" style="width:25px;height:19px;border:0">
</a>

<a href="https://www.linkedin.com/in/nilotpalkapri">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Linkedin.svg/1200px-Linkedin.svg.png" alt="Linkedin" style="width:19px;height:19px;border:0">
</a>



<a href="https://independent.academia.edu/nilotpalkapri">
  <img src="https://image.flaticon.com/icons/png/512/25/25645.png" alt="Academia" style="width:19px;height:19px;border:0">
</a>
<a href="https://orcid.org/0000-0001-7803-5957">
  <img src="http://nitens.org/img/sm-icons/orcid.png" alt="Orcid" style="width:19px;height:19px;border:0">
</a>
<a href="https://www.mendeley.com/profiles/nilotpal-kapri/">
  <img src="http://cdn.onlinewebfonts.com/svg/img_435968.png" alt="Mendeley" style="width:22px;height:17px;border:0">
</a>

<!-- <p>We have added "border:0" to prevent IE9 (and earlier) from displaying a border around the image.</p> </p> -->


 </center>     
</body>
</html>

                """, unsafe_allow_html=True
                )
    
