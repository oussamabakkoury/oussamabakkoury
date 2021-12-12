# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# IMPORT USEFULL LIBRARIES
# ----------------------------------------------------------------------------
import streamlit as st
from streamlit_folium import folium_static
import folium
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.palettes import Category20_10

# TITLE AND TEXT
# ----------------------------------------------------------------------------
st.title("Life ladder world map")


# IMPORT DATABASE AND CLEAR THE DATA (If needed and need to be checked)
# ----------------------------------------------------------------------------
#whr_raw = pd.read_csv("world-happiness-report.csv")
whr_raw = pd.read_csv("whr_NoNA_all.csv", sep=';',index_col = 0)

new_names =  {'Tanzania':'United Republic of Tanzania','United States':
              'United States of America','Palestinian Territories':'Palestine',
              'Taiwan Province of China':'Taiwan','North Macedonia':
            'Macedonia','Serbia':'Republic of Serbia','Congo (Brazzaville)':
            'Republic of the Congo','North Cyprus':'Northern Cyprus', 
            'Swaziland':'eSwatini','Czech Republic':'Czechia',
            'Congo (Kinshasa)':'Democratic Republic of the Congo',
            'Somaliland region':'Somaliland'}

#df= whr_raw[["Country","Year","Life Ladder","Region"]]
df = whr_raw
df["Country"] = df["Country"].replace(new_names)

st.write("Dataframe example: ")
st.dataframe(df.head())

st.markdown("**First map**")

# SLIDER TO SELECT A YEAR
# ----------------------------------------------------------------------------
year_side = st.sidebar.slider("choose a year to plot", min_value=(2005), 
                              max_value=(2020),step=(1))
#st.write("The choosen year is ",year_side )

# MULTISELECT TO SELECT ONE OR MORE REGION(S)
# ----------------------------------------------------------------------------
#.sidebar
def data_list(dataframe, col):
    list_data = dataframe[col].sort_values().unique().tolist()
    return list_data

options = st.sidebar.multiselect('Select one or more Region:',
                                 data_list(df,'Region'),
                                 data_list(df,'Region')[0])

#st.write("RESULT: ",options)

df_1 = pd.DataFrame()
for i in options:
    df_op = df[df['Region'] == i]
    df_1 = df_1.append(df_op)
    
# SELECT DATA
# ----------------------------------------------------------------------------
def column_list(dataframe):
    list_col = dataframe.select_dtypes('number').columns.values.tolist()
    return list_col 

column_select = st.sidebar.selectbox('Select one col:',(column_list(df)))
#st.write("The cloumn is ",option)

# PRINT MAPS
# ----------------------------------------------------------------------------
df_map = df_1[df_1['Year'] == year_side]

country_geo = os.path.join('world-countries.json')

#m = folium.Map()
m = folium.Map(location=[10, 10], zoom_start=1)
m.choropleth(geo_data=country_geo, name='choropleth', data=df_map,
             columns=['Country', column_select],
             key_on='feature.properties.name',
             fill_color='RdBu',
             fill_opacity=0.7,
             line_opacity=0.2,
             legend_name=column_select
            )
folium.LayerControl().add_to(m)

# call to render Folium map in Streamlit
folium_static(m)

# BOXPLOT
# ----------------------------------------------------------------------------


# Region study
# ----------------------------------------------------------------------------
st.info('''Region study show a boxplot of the value and the region(s) selected 
        on all the year and on the selected year''')
Region_study = st.checkbox('Region study')
if Region_study:
    st.markdown("**Region study**")

    # BOXPLOT
    # -------------------------------------------------------------------------
    df_map = df_map.sort_values(by="Region")
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    sns.boxplot(ax=axes[0],x="Region", y=column_select,data=df_map, 
                palette=Category20_10)
    axes[0].set_title((column_select+" selected year"), fontsize=10)
    axes[0].set_xticklabels(axes[0].get_xticklabels(),rotation=75)
    
    df_1 = df_1.sort_values(by="Region")
    sns.boxplot(ax=axes[1],x="Region", y=column_select,data=df_1, 
                palette=Category20_10)
    axes[1].set_title(column_select+" all years", fontsize=10)
    axes[1].set_xticklabels(axes[1].get_xticklabels(),rotation=75)
    
    st.pyplot(fig)
    # line
    # -------------------------------------------------------------------------
    
# Country study
# ----------------------------------------------------------------------------
Country_study = st.checkbox('Country study')
if Country_study:
    st.markdown("**Country study**")
    # MULTISELECT TO SELECT ONE OR MORE COUNTRIES
    # ------------------------------------------------------------------------
    country = st.multiselect('Select one or more Country:',
                             data_list(df_1,'Country'),
                             data_list(df_1,'Country')[0])
    # BOXPLOT
    # -------------------------------------------------------------------------
    #st.write("RESULT: ",country)
    
    df_c = pd.DataFrame()
    for i in country:
        df_cop = df_1[df_1['Country'] == i]
        df_c = df_c.append(df_cop)
    
    df_c = df_c.sort_values(by="Year")
    #st.dataframe(df_c)
    # line
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots()
    sns.lineplot(ax=ax, x="Year", y=column_select,
             hue="Country", data=df_c)
    
    st.pyplot(fig)