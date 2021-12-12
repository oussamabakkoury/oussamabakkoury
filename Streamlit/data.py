import streamlit as st
import numpy as np
import pandas as pd

def app():
    st.title('HapPy Factory')
    
    import os
    from streamlit_folium import folium_static
    import folium
    ### Titre
    st.subheader("Comparaison entre le score de bonheur et le PIB")
    ###Sidebar
    year_side = st.sidebar.slider("Choisir une année pour l'affichage", min_value=(2005), max_value=(2020),step=(1), value=2015)
    st.write("L'année choisie est : ",year_side )
    ### Préparation des données
    whr_raw = pd.read_csv("world-happiness-report.csv")
    new_names =  {'Tanzania' : 'United Republic of Tanzania', 'United States' : 'United States of America', 'Palestinian Territories':'Palestine',
                 'Taiwan Province of China': 'Taiwan','North Macedonia' : 'Macedonia', 'Serbia': 'Republic of Serbia',
                 'Congo (Brazzaville)' : 'Republic of the Congo', 'North Cyprus' : 'Northern Cyprus', 'Swaziland' : 'eSwatini',
                 'Czech Republic':'Czechia', 'Congo (Kinshasa)':'Democratic Republic of the Congo', 'Somaliland region':'Somaliland'}
    df= whr_raw[["Country name","year","Life Ladder","Log GDP per capita"]]
    df["Country name"] = df["Country name"].replace(new_names)
    df_2005 = df[df['year'] == year_side]
    whr21 = pd.read_csv("world-happiness-report-2021.csv")
    region_map=whr21[['Country name','Regional indicator']]
    whr_raw_region=whr_raw.merge(region_map,on='Country name',how='left')
    region_indic={'Angola':'Sub-Saharan Africa', 'Belize':'Latin America and Caribbean',
                  'Bhutan':'South Asia', 'Central African Republic':'Sub-Saharan Africa',
                  'Congo (Kinshasa)':'Sub-Saharan Africa', 'Cuba':'Latin America and Caribbean',
                  'Djibouti':'Sub-Saharan Africa', 'Guyana':'Latin America and Caribbean',
                  'Oman':'Middle East and North Africa', 'Qatar':'Middle East and North Africa',
                  'Somalia':'Sub-Saharan Africa', 'Somaliland region':'Sub-Saharan Africa',
                  'South Sudan':'Sub-Saharan Africa', 'Sudan':'Sub-Saharan Africa',
                  'Suriname':'Latin America and Caribbean', 'Syria':'South Asia',
                  'Trinidad and Tobago':'Latin America and Caribbean'}
        ## Application du dictionnaire region_indic au dataframe
    for i, country in enumerate(whr_raw_region['Country name']):
        if country in region_indic:
            whr_raw_region.loc[i,'Regional indicator']=region_indic[country]
    df_region= whr_raw_region[["Country name","year","Life Ladder","Log GDP per capita","Regional indicator"]]
    df_region["Country name"] = df_region["Country name"].replace(new_names)
        ##DataFrames régions
        
            #Western Europe
    df_we=df_region[df_region['Regional indicator']=='Western Europe']
    df_we_2005 = df_we[df_we['year'] == year_side]
            #Latin America & Carabbian
    df_la=df_region[df_region['Regional indicator']=='Latin America and Caribbean']
    df_la_2005 = df_la[df_la['year'] == year_side]
            #Middle East and North Africa
    df_mena=df_region[df_region['Regional indicator']=='Middle East and North Africa']
    df_mena_2005 = df_mena[df_mena['year'] == year_side]
    ### Affichage 
        ##Selectbox
    affichage=st.selectbox("Choisir la partie du monde à afficher",["Monde entier","Europe Occidentale",
                                                                    "Amérique latine",
                                                                    "Afrique du Nord et Moyen-Orient"])
        ##Affichage des cartes
    country_geo = os.path.join('world-countries.json')
    def imp(affichage):
        if affichage=="Monde entier":
            m = folium.Map()
            m = folium.Map(location=[10, 0], zoom_start=1.5)
            m.choropleth(geo_data=country_geo, name='choropleth', data=df_2005,
                 columns=['Country name', 'Life Ladder'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name='Taux de bonheur'
                )
            #folium.LayerControl().add_to(m)
    # call to render Folium map in Streamlit
            folium_static(m)
            
            m1 = folium.Map()
            m1 = folium.Map(location=[10, 0], zoom_start=1.5)
            m1.choropleth(geo_data=country_geo, name='choropleth', data=df_2005,
                 columns=['Country name', 'Log GDP per capita'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name='PIB par habitant'
                )
            #folium.LayerControl().add_to(m1)
    # call to render Folium map in Streamlit
            folium_static(m1)
          
        elif affichage=="Europe Occidentale":
            col1, col2 = st.columns(2)
            col1.write('Life Ladder:')
            col2.write('LogGDP:')
            m = folium.Map()
           # m = folium.Map(width=300,height=500,location=[54.525961, 15.255119], zoom_start=3)
            m = folium.Map(location=[54.525961, 15.255119], zoom_start=3)
            m.choropleth(geo_data=country_geo, name='choropleth', data=df_we_2005,
                 columns=['Country name', 'Life Ladder'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name='Taux de bonheur'
                )
            #folium.LayerControl().add_to(m)
    # call to render Folium map in Streamlit
            #with col1:
            #    folium_static(m)
            folium_static(m)
            
             
            m1 = folium.Map()
            #m1 = folium.Map(width=300,height=500,location=[54.525961, 15.25511], zoom_start=3)
            m1 = folium.Map(location=[54.525961, 15.25511], zoom_start=3)
            m1.choropleth(geo_data=country_geo, name='choropleth', data=df_we_2005,
                 columns=['Country name', 'Log GDP per capita'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name='PIB'
                )
            #folium.LayerControl().add_to(m1)
    # call to render Folium map in Streamlit
            #with col2:
            #    folium_static(m1)
            folium_static(m1)
            
        elif affichage=="Amérique latine":
            m = folium.Map()
            m = folium.Map(location=[-8.7832, -55.4915], zoom_start=3)
            m.choropleth(geo_data=country_geo, name='choropleth', data=df_la_2005,
                 columns=['Country name', 'Life Ladder'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name='Taux de bonheur'
                )
            #folium.LayerControl().add_to(m)
    # call to render Folium map in Streamlit
            folium_static(m)
            
            m1 = folium.Map()
            m1 = folium.Map(location=[-8.7832, -55.4915], zoom_start=3)
            m1.choropleth(geo_data=country_geo, name='choropleth', data=df_la_2005,
                 columns=['Country name', 'Log GDP per capita'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name='PIB'
                )
            #folium.LayerControl().add_to(m1)
    # call to render Folium map in Streamlit
            folium_static(m1)
            
        elif affichage=="Afrique du Nord et Moyen-Orient":
            m = folium.Map()
            m = folium.Map(location=[31.268205, 29.995368], zoom_start=3)
            m.choropleth(geo_data=country_geo, name='choropleth', data=df_mena_2005,
                 columns=['Country name', 'Life Ladder'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name='Taux de bonheur'
                )
            #folium.LayerControl().add_to(m)
    # call to render Folium map in Streamlit
            folium_static(m)
            
            m1 = folium.Map()
            m1 = folium.Map(location=[31.268205, 29.995368], zoom_start=3)
            m1.choropleth(geo_data=country_geo, name='choropleth', data=df_mena_2005,
                 columns=['Country name', 'Log GDP per capita'],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 range_color=(0, 10),
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name="PIB"
                )
            #folium.LayerControl().add_to(m1)
    # call to render Folium map in Streamlit
            folium_static(m1)
            
    st.write(imp(affichage))