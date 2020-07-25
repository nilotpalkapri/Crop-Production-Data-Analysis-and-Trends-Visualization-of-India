
import streamlit as st
import pandas as pd
import numpy as np
import folium # map rendering library
import branca.colormap as cl
from streamlit_folium import folium_static


def start(df2):
    
    color = [['black', '#566573'], 
             ['blue', '#5dade2'], 
             ['green', '#82e0aa'], 
             ['white', '#fdfefe'], 
             ['yellow', '#f9e79f'], 
             ['red', '#f5b7b1']]
    def color_selection(cr):
        for i in range(6):
            try:
                if cr == select_crop[i]:
                    return color[i]
            except:
                return color[i]
        
    st.sidebar.subheader('Select Crop: ')
    select_crop = st.sidebar.multiselect('Please select as few as possible(Maximum 5) to get faster and perfect view!', 
                                         sorted([i for i in set(df2['Crop'])]), 
                                         default=['Rice',])
    user_df = df2.copy()
    user_df = user_df.loc[(user_df['Crop'].isin(select_crop))]

    st.sidebar.subheader('Select Year: ')
    select_year = st.sidebar.multiselect('Please select as few as possible to get faster view!', 
                                         (['Select All','Select All Odds','Select All Evens']+
                                          [i for i in set(user_df['Crop_Year'])]), 
                                         default=[sorted(user_df['Crop_Year'])[-1]])

    if 'Select All' in select_year:
        select_year = [i for i in set(user_df['Crop_Year'])]
    elif 'Select All Odds' in select_year:
        select_year = [i for i in set(user_df['Crop_Year']) if i%2!=0]
    elif 'Select All Evens' in select_year:
        select_year = [i for i in set(user_df['Crop_Year']) if i%2==0]
        
    user_df = user_df.loc[(user_df['Crop_Year'].isin(select_year))]

    st.sidebar.subheader('Select Season: ')
    select_season = st.sidebar.multiselect('Please select as few as possible to get faster view!', 
                                           (['Select All']+[i for i in set(user_df['Season'])]), 
                                           default=[i for i in set(user_df['Season'])])
    if 'Select All' in select_season:
        select_season = [i for i in set(user_df['Season'])]

    
    user_df = user_df.loc[(user_df['Season'].isin(select_season))]
    #user_df = df2.loc[(df2['Crop'].isin(select_crop)) & 
    #                  (df2['Crop_Year'].isin(select_year)) & 
    #                  (df2['Season'].isin(select_season))]

    lowercase = lambda x:str(x).lower()
    user_df.rename(lowercase, axis='columns', inplace=True)

    mean = np.mean(user_df['production']) #get the mean Production amount
    mini = int(np.min(user_df['production'])) #get the minimum Production amount
    maxi = int(np.max(user_df['production'])) #get the maximum Production amount


    st.sidebar.subheader('What is the minimum amount of Production?')
    min_production = st.sidebar.slider('What is the minimum amount of Production?', 
                                       min_value=0, 
                                       max_value=int(max(user_df['production'])), 
                                       value=0)

    st.sidebar.subheader('Select No of Sides for the Marker: ')
    marker_side = st.sidebar.number_input('You can leave it default for Circle.', 
                           min_value=3, 
                           max_value=100,
                           value=100, 
                           step=1)

    st.sidebar.subheader('Select Marker Radius Multiplier: ')
    multiplier = st.sidebar.number_input('You can leave it default to keep maximum radious 40.', 
                           min_value=0.5, 
                           max_value=10.0,
                           value=40*mean/maxi, 
                           step=0.5)

    st.sidebar.subheader('Select Map Type: ')
    map_tiles = st.sidebar.radio('Select style of the map you want to see.', 
             ('OpenStreetMap', 
              'Mapbox Bright', 
              'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 
              'CartoDB positron', 'CartoDB dark_matter'))
    if len(map_tiles)==0:
        map_tiles = 'OpenStreetMap'

    #for i in select_crop:
    #    pick_color = st.beta_color_picker('Pick A Color for {}'.format(i), '#00f900')

    midpoint = (np.average(user_df['latitude']),np.average(user_df['longitude'])) #get_loc('India')

    if st.sidebar.button('Proceed to Map'):
        for i in select_year:
            data = user_df.loc[(user_df['crop_year']==i)]
            data = data.query('production > @min_production').dropna(how='any')

            rad = 'Marker Radious: Min={a}, Max={b}'.format(b=round(maxi//int(mean)*multiplier,2), 
                                                            a=round(mini//int(mean)*multiplier,2))

            cap = '{} Production Data of {}. {}'.format(', '.join(map(str, select_crop)), i, rad)
            st.header(cap)

            st.subheader('Color Codes:') #Introduce the colors assigned for different crops
            color_codes = ''
            for i in range(len(select_crop)):
                try:
                    color_codes += '{}: {}; '.format(select_crop[i],color[i][0])
                except:
                    color_codes += '{}: {}; '.format(select_crop[i],color[5][0])
            st.write(color_codes)

            index = [mini, maxi*.10, maxi*.30, maxi*.60, maxi] #required for labeling

            map_india = folium.Map(location=[midpoint[0], midpoint[1]], 
                                   width=700, 
                                   height=700, 
                                   min_zoom=4, 
                                   max_zoom=12, 
                                   zoom_start=5, 
                                   min_lat=np.min(data['latitude'])-50, 
                                   max_lat=np.max(data['latitude'])+50, 
                                   min_lon=np.min(data['longitude'])-50, 
                                   max_lon=np.max(data['longitude'])+50, 
                                   max_bounds=True,  
                                   tiles=map_tiles) #create a map with fetched coordinates of India

            # add markers to map
            for lat, lng, add, cr, pr in zip(data['latitude'], 
                                             data['longitude'], 
                                             data['address'], 
                                             data['crop'], 
                                             data['production']):

                col = color_selection(cr)
                label = '{}({}), {}'.format(cr, pr, add) #label all the datapoints
                label = folium.Popup(label, parse_html=True)
                folium.RegularPolygonMarker(location=[lat, lng], 
                                            number_of_sides=marker_side, 
                                            radius=round(pr/mean*multiplier,2), 
                                            popup=label, 
                                            color=col[0], 
                                            fill=True, 
                                            fill_color=col[1], 
                                            fill_opacity=0.5, 
                                            parse_html=False).add_to(map_india) #mark the points on the map

            #specify the min and max values of your data YlOrRd_09
            colormap = cl.linear.Blues_09.scale(mini, maxi)
            colormap = colormap.to_step(index=index)
            colormap.caption = cap
            colormap.add_to(map_india) #add lagend to show caption and varition of data range.

            with st.echo():
                folium_static(map_india)
    
        st.success('Success!')
        st.balloons()
        
    
    if st.sidebar.checkbox('Show My Map Data', False):
        sh2 = user_df.shape
        st.subheader('Data as per Your Selection')
        st.markdown('This DataFrame is loaded with {} rows and {} columns.'.format(sh2[0], sh2[1]))
        st.write(user_df.head(100))
        st.success('Success!')
        st.balloons()
