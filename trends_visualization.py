
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import seaborn as sns; sns.set(color_codes=True)

d = 0
d2=0
def start(df):
    global d
    global d2
    def plot_with_seaborn(df_var,x_var,y_var):
        try:
            plt.figure(figsize=(12, 4))
            sns.set(font_scale=1.5)
            sns.set_style('whitegrid')
            
            ax = sns.regplot(x=x_var, 
                             y=y_var, 
                             data=df_var, 
                             color='green', 
                             marker='+',  
                             scatter_kws={'s': 200})
            ax.set(xlabel=x_var, ylabel=y_var)
            ax.set_title('Trends of {} {} of {} from 1997 to 2014.'.format(j,y_var.split('_')[1],i))
            st.latex('Trends of {} {} of {} from 1997 to 2014.'.format(j,y_var.split('_')[1],i))
            st.pyplot()
        except:
            st.write('Unable to find Trends of {} {} of {} from 1997 to 2014.'.format(j,y_var.split('_')[1],i))
            pass


    def bar_plot(df_var, x_var):
        df_var = df_var[['Crop_Year','Total_Production','Total_Area']]
        ax = df_var.plot(kind='bar',
                         figsize=(12, 4), 
                         width=0.8, 
                         color=['#5cb85c','#5bc0de'], 
                         title='Trends of {} Area vs. Production of {} from 1997 to 2014.'.format(j,i))
        ax.set_xticks(range(len(df_var)))
        ax.set_xlabel(x_var)
        ax.set_xticklabels([int(i) for i in df_var[x_var]]);
        st.pyplot()


    def scatter_plot_with_pyplot(df):
        plt.scatter(df_var[x_var], df_var[y_var])
        st.pyplot()
        
    
    
    st.sidebar.subheader('Choose the States for which Production Trends to be visualized: ')
    select_state = [st.sidebar.selectbox('Please select as few as possible to get faster view!', 
                                         sorted([i for i in set(df['State_Name'])]), 
                                         index=len([i for i in set(df['State_Name'])])-1
                                        )]
    
    user_df = df.loc[(df['State_Name'].isin(select_state))]
    
    try:
        st.sidebar.subheader('Select Crop: ')
        select_crop = st.sidebar.multiselect('Please select as few as possible to get faster view!', 
                                             sorted([i for i in set(user_df['Crop'])]), 
                                             default=[sorted([i for i in set(user_df['Crop'])])[-1],])
        
        user_df = user_df.loc[(user_df['Crop'].isin(select_crop))]
        
        st.sidebar.subheader('Select Season: ')
        select_season = st.sidebar.multiselect('Please select as few as possible to get faster view!', 
                                             (['Select All']+[i for i in set(user_df['Season'])]), 
                                             default=[i for i in set(user_df['Season'])])
        if 'Select All' in select_season:
            select_season = [i for i in set(user_df['Season'])]
        
        user_df = user_df.loc[(user_df['Season'].isin(select_season))]
        e=0
    except:
        e=1
        st.error('Please select at least one from each option.')
    
    
    
    if e==0 and (st.sidebar.button('Proceed to Plot ⏩') or d>0):
        d+=1
        for i in select_state: #process for all selected states
            temp_df = user_df.copy()
            temp_df = temp_df[temp_df.State_Name==i]
            temp_df.drop(['Season'], axis = 1, inplace = True)
            for j in select_crop: #process for all selected crops under each state
                new_df = temp_df[['Crop_Year','Production','Area']][temp_df.Crop==j]
                final_df = pd.DataFrame(columns=['Crop_Year','Total_Production','Total_Area','Total_Production/Area'])
                for k in range(1997,2015): #make temporarily required dataframe
                    try:
                        total_prod = sum(new_df['Production'][new_df.Crop_Year==k])
                        total_area = sum(new_df['Area'][new_df.Crop_Year==k])
                        prod_per_area = total_prod/total_area
                    except:
                        total_prod = 0
                        total_area = 0
                        prod_per_area = 0
                    final_df = final_df.append({'Crop_Year': k, 
                                                'Total_Production': total_prod, 
                                                'Total_Area': total_area, 
                                                'Total_Production/Area': prod_per_area}, ignore_index=True)
                #print(final_df)

                plot_with_seaborn(final_df, 'Crop_Year', 'Total_Production')
                plot_with_seaborn(final_df, 'Crop_Year', 'Total_Area')
                plot_with_seaborn(final_df, 'Crop_Year', 'Total_Production/Area')
                bar_plot(final_df, 'Crop_Year')
                #scatter_plot_with_pyplot(final_df)
        
        st.success('Success!')
        st.balloons()

        
    try:
        st.sidebar.subheader('Additional Options:')
        dist_opt = st.sidebar.radio('Want to See District Wise?', ['Yes','No'], index=1)
        if dist_opt == 'Yes':
            st.sidebar.subheader('Select District:')
            select_dist = [st.sidebar.selectbox('Please select district to see trends!', 
                                                sorted([i for i in set(user_df['District_Name'])]), 
                                         index=len([i for i in set(user_df['District_Name'])])-1
                                        )]
            user_df = user_df.loc[(user_df['District_Name'].isin(select_dist))]
        e2=0
        
    except:
        e2=1
        st.error('Please select at option.')
    
    
    if (e2==0 and dist_opt == 'Yes') and (st.sidebar.button('Proceed to Plot District Data ⏩') or d2>0):
        d2+=1
        for i in select_dist: #process for all selected states
            temp_df = user_df.copy()
            temp_df = temp_df[temp_df.District_Name==i]
            temp_df.drop(['Season'], axis = 1, inplace = True)
            for j in select_crop: #process for all selected crops under each state
                new_df = temp_df[['Crop_Year','Production','Area']][temp_df.Crop==j]
                final_df = pd.DataFrame(columns=['Crop_Year','Total_Production','Total_Area','Total_Production/Area'])
                for k in range(1997,2015): #make temporarily required dataframe
                    try:
                        total_prod = sum(new_df['Production'][new_df.Crop_Year==k])
                        total_area = sum(new_df['Area'][new_df.Crop_Year==k])
                        prod_per_area = total_prod/total_area
                    except:
                        total_prod = 0
                        total_area = 0
                        prod_per_area = 0
                    final_df = final_df.append({'Crop_Year': k, 
                                                'Total_Production': total_prod, 
                                                'Total_Area': total_area, 
                                                'Total_Production/Area': prod_per_area}, ignore_index=True)
                #print(final_df)

                plot_with_seaborn(final_df, 'Crop_Year', 'Total_Production')
                plot_with_seaborn(final_df, 'Crop_Year', 'Total_Area')
                plot_with_seaborn(final_df, 'Crop_Year', 'Total_Production/Area')
                bar_plot(final_df, 'Crop_Year')
                #scatter_plot_with_pyplot(final_df)
        
        st.success('Success!')
        st.balloons()
        
            
            
    if st.sidebar.checkbox('Show My Plot Data', False):
        sh2 = user_df.shape
        st.subheader('Data as per Your Selection')
        st.markdown('This DataFrame is loaded with {} rows and {} columns.'.format(sh2[0], sh2[1]))
        st.write(user_df.head(100))
        st.success('Success!')
        st.balloons()
    
