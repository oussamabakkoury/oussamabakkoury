import streamlit as st
import pandas as pd
import numpy as np

def app():
    
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
    
    # TITLE
    # ----------------------------------------------------------------------------
    st.title('HapPy Factory')
    
    # IMPORT USEFULL LIBRARIES
    # ----------------------------------------------------------------------------
    from streamlit_folium import folium_static
    import folium
    import os
    import seaborn as sns
    import matplotlib.pyplot as plt
    from bokeh.palettes import Category20_10
    
        # TITLE AND TEXT
    # ----------------------------------------------------------------------------
    st.subheader("Carte du score de bonheur")
    
    # SLIDER TO SELECT A YEAR
    # ----------------------------------------------------------------------------
    st.sidebar.write("")
    st.sidebar.subheader("Paramètres de la carte :")
    year_side = st.sidebar.slider("Sélectionner une année à observer :", value=(2015), min_value=(2005), 
                                  max_value=(2020),step=(1))
    #st.write("The choosen year is ",year_side )
    
    # MULTISELECT TO SELECT ONE OR MORE REGION(S)
    # ----------------------------------------------------------------------------
    #.sidebar
    def data_list(dataframe, col):
        list_data = dataframe[col].sort_values().unique().tolist()
        return list_data
    
    options = st.sidebar.multiselect('Sélectionner une ou plusieurs région(s) :',
                                     data_list(df,'Region'),
                                     data_list(df,'Region')[:4])
    
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
    
    column_select = st.sidebar.selectbox('Sélectionnez une variable à étudier :',(column_list(df)), index=1)
    #st.write("The cloumn is ",option)
    
    # PRINT MAPS
    # ----------------------------------------------------------------------------
    df_map = df_1[df_1['Year'] == year_side]
    
    country_geo = os.path.join('world-countries.json')
    
    #m = folium.Map()
    m = folium.Map(location=[10, 0], zoom_start=1.5)
    m.choropleth(geo_data=country_geo, name='choropleth', data=df_map,
                 columns=['Country', column_select],
                 key_on='feature.properties.name',
                 fill_color='RdBu',
                 fill_opacity=0.7,
                 line_opacity=0.2,
                 legend_name=column_select
                )
    #folium.LayerControl().add_to(m)
    
    # call to render Folium map in Streamlit
    folium_static(m)
    
    # BOXPLOT
    # ----------------------------------------------------------------------------
    
    
    # Region study
    # ----------------------------------------------------------------------------
    #st.info('''Region study show a boxplot of the value and the region(s) selected 
    #        on all the year and on the selected year''')
    #st.info('''L'etude des région propose des visualisations de la distribution des variables pour les régions sélectionnées sur toute les années ou une selection.''')
    Region_study = st.checkbox('Etudiez les régions')
    if Region_study:
        #st.markdown("**Etudiez les régions :**")
    
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
    Country_study = st.checkbox('Etudiez les pays')
    if Country_study:
        #st.markdown("**Etudiez les pays**")
        # MULTISELECT TO SELECT ONE OR MORE COUNTRIES
        # ------------------------------------------------------------------------
        country = st.multiselect('Sélectionnez un ou plusieurs pays :',
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
        
    # INTRODUCTION
    # ----------------------------------------------------------------------------    
    st.subheader("Base de données")
    st.write("Le World Hapinness Report commandé par une instance de l'ONU est un sondage réalisé tous les ans par Gallup World Poll depuis 2015 dans une grande partie des pays du monde. Son objectif est de récolter un score de bonheur déclaré auprès de 1000 habitants, ainsi que des scores concernant la liberté, le support social, la générosité, la corruption et les sentiments négatifs ou positifs.")
    st.write("Nous avons ajouté à cette base, des données plus objectives à propos de la région du monde, de la corruption, de la démographie, des religions, du PIB par habitant (son logarithme pour éliminer la croissance), des inégalités, de l'espérance de vie et du régime politique.")
    
    dataView = st.checkbox('Aperçu de la base de données')
    if dataView:
        st.dataframe(df.head(15))
    
    st.subheader("Objectifs du projet")
    st.write("Notre objectif est de comprendre le score de bonheur observé en étudiant ses composantesà l'aide d'outils statistiques. Cette grande base de données pourrait nous permettre d'identifier quel est le poids de chaque aspect d'un pays, que ce soit les perceptions des habitants ou des données sur l'économie, la politique et la société auxquelles ils sont confrontés.")
    st.write("Le sujet étant d'une complexité absolue et relatif à un enjeu philosophique avec des biais considérables dans les données, nous prétendons étudier et éventuellement interpréter des phénomènes, plutôt que d'essayer d'obtenir la clé du bonheur.")
    st.caption("Utilisez la navigation en haut à gauche pour voir les autres pages :")
    st.markdown("<ul><li><b>Analyse d'une corrélation</b> : Comparaison du score de bonheur avec le PIB par habitant.</li><li><b>Modèle de prédiction</b> : Regression linéaire intéractive et lecture des résultats.</li></ul>", unsafe_allow_html=True)

