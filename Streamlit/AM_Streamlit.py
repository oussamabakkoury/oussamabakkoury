import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV

#st.set_page_config(layout="wide")

def Previous_Life_ladder(df):
    """
    Description : Add a column life ladder Year-1 to a given dataframe
    Input : Dataframe with the columns 'Country', 'Year', 'Life Ladder'
    Output : Dataframe with the column 'Life Ladder-1' added and other years range dropped.
    """
    df_whr_previous = pd.DataFrame()
    
    for i in df["Country"].unique():
        df_filtered = df[df["Country"]==i]
        df_filtered["Year-1"] = df_filtered["Year"].shift(1)
        df_filtered["Life Ladder-1"] = df_filtered["Life Ladder"].shift(1)
        
        df_whr_previous = df_whr_previous.append(df_filtered)
        df_whr_previous = df_whr_previous.fillna(method="bfill")
    
    df_whr_previous["diff_Y"] = df_whr_previous["Year"]-df_whr_previous["Year-1"]
    df_whr_previous = df_whr_previous[df_whr_previous["diff_Y"]==1]
    df_whr_previous = df_whr_previous.drop(['Year-1','diff_Y'], axis=1)
    
    return df_whr_previous

st.title('HapPy Factory')

st.header("Regression linéaire de Lasso")

LogGDP = True
LifeExpectancy = True
PopAnnualGrowthRate = True
PopDensity = True
InfantMortalityRate = True
GiniCoeff21 = True
Corrup = True
Regime = True
Region = True
Religion = True

Freedom = False
SocialSupport = False
Generosity = False
Corruption = False
PostAffect = False
NegAffect = False
Inertie = False

def varSet():
    whr = pd.read_csv('whr_NoNA_all_topia.csv', sep=';',index_col = 0)
    whr = whr.replace(to_replace="Congo (Brazzaville)", value="Congo")
    varOn = []
    varNames = ["LogGDP","SocialSupport","LifeExpectancy","Freedom",
                "Generosity","Corruption","PosAffect","NegAffect",
                "PopAnnualGrowthRate","PopDensity","InfantMortalityRate",
                "GiniCoeff21","Corrup", "Regime", "Region"]
    varCheck = [LogGDP, SocialSupport, LifeExpectancy, Freedom, Generosity, Corruption, PostAffect, NegAffect,
                PopAnnualGrowthRate, PopDensity, InfantMortalityRate, GiniCoeff21, Corrup, Regime, Region]
    j=0
    for i in varCheck :
        if i == True :
            varOn.append(varNames[j])
        j+=1
    if Religion == True :
        varOn.extend(("Judaisme", "Islam", "Hindouisme", "Christianisme", 
                     "Sans-religion", "Bouddhisme", "Religions traditionnelles", "Autres"))
    if Inertie == True :
        whr = Previous_Life_ladder(whr)
        varOn.append("Life Ladder-1")
        #st.write(whr.head())
    return varOn, whr

st.sidebar.subheader("Sélection des variables du modèle :")


LogGDP = st.sidebar.checkbox("PIB par tête", value=LogGDP, on_change=varSet)
SocialSupport = st.sidebar.checkbox("Support social", value=SocialSupport, on_change=varSet)
LifeExpectancy = st.sidebar.checkbox("Espérance de vie", value=LifeExpectancy, on_change=varSet)
Freedom = st.sidebar.checkbox("Sentiment de liberté", value=Freedom, on_change=varSet)
Generosity = st.sidebar.checkbox("Sentiment de générosité", value=Generosity, on_change=varSet)
Corruption = st.sidebar.checkbox("Sentiment de corruption", value=Corruption, on_change=varSet)
PostAffect = st.sidebar.checkbox("Sentiments positifs", value=PostAffect, on_change=varSet)
NegAffect = st.sidebar.checkbox("Sentiments négatifs", value=NegAffect, on_change=varSet)
PopAnnualGrowthRate = st.sidebar.checkbox("Taux de croissance (population)", value=PopAnnualGrowthRate, on_change=varSet)
PopDensity = st.sidebar.checkbox("Densité de population", value=PopDensity, on_change=varSet)
InfantMortalityRate = st.sidebar.checkbox("Taux de mortalité infantile", value=InfantMortalityRate, on_change=varSet)
GiniCoeff21 = st.sidebar.checkbox("Indice d'inégalités (Gini)", value=GiniCoeff21, on_change=varSet)
Corrup = st.sidebar.checkbox("Indice de corruption", value=Corrup, on_change=varSet)

Regime = st.sidebar.checkbox("Régime politique", value=Regime, on_change=varSet)
Region = st.sidebar.checkbox("Régions du monde", value=Region, on_change=varSet)
Religion = st.sidebar.checkbox("Religions", value=Religion, on_change=varSet)

st.sidebar.caption("(au moins une doit être sélectionnée)")

st.sidebar.subheader("Activation de l'inertie du bonheur :")
Inertie = st.sidebar.checkbox("Score de bonheur n-1", value=Inertie, on_change=varSet)

#st.write("Liste des variables actives :")
#st.write(varSet())

columns, whr = varSet()
if columns == []:
    st.error("Veuillez sélectionner au moins une variable.")
score = whr[['Life Ladder']]
data = whr[columns]



# TRANSFORMATION DES REGIMES POLITIQUES EN DUMMIES
if Regime == True:
    data = data.drop(columns=['Regime'])
    politics = whr[['Regime']]
    politics = pd.get_dummies(politics)
    data = data.join(politics)

# TRANSFORMATION DES REGIONS EN DUMMIES
if Region == True:
    data = data.drop(columns=['Region'])
    regions = whr[['Region']]
    regions = pd.get_dummies(regions)
    data = data.join(regions).drop(columns=['Region_Topia'])

# ENSEMBLES, ENTRAINEMENT ET PERFORMANCES
X_train, X_test, y_train, y_test = train_test_split(data, score, test_size=0.2, random_state=123) 
model_lasso = LassoCV(cv=10, alphas=([10, 1, 0.1, 0.01, 0.001])).fit(X_train, y_train)
pred_test = model_lasso.predict(X_test)

# RESULTATS
st.write("La régression linéaire avec la méthode de Lasso permet de sélectionner des variables explicatives pour prédire une variable expliquée, ici le score de bonheur.")
r2train2, r2test2 = round(model_lasso.score(X_train, y_train),3), round(model_lasso.score(X_test, y_test),3)
st.metric("Score sur l'ensemble de test (%)*", r2test2*100, delta=None, delta_color="normal")
st.caption("*taux de variance du score de bonheur expliqué par le modèle")
st.text("")

coef_list = list(model_lasso.coef_)
coef_list_round = list(np.around(np.array(coef_list),3))

coeff_table = pd.DataFrame(
    {'Variable': list(X_train.columns),
     'Coeff': coef_list_round
    })

st.subheader("Table des coefficients associés à chaque variable :")
st.table(coeff_table[coeff_table['Coeff'] != 0].sort_values(by='Coeff', ascending=False).style.background_gradient(cmap='RdYlGn', vmin=-1, vmax=2).set_precision(3))

if st.checkbox('Afficher les variables éliminées par la méthode de Lasso', value=False):
    st.write(coeff_table[coeff_table['Coeff'] == 0])

pred = model_lasso.predict(data)
whr['error']=whr['Life Ladder']-pred

st.subheader("Erreur de prédiction par rapport au score de bonheur* :")

whrB = whr.groupby(by=['Country'], as_index=False).mean().merge(whr[['Country', 'Region']], on='Country')
whrB = whrB.drop_duplicates(keep='first')

from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource,LabelSet, Label, CategoricalColorMapper
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10_10
from bokeh.models import Range1d
output_notebook()

source = ColumnDataSource(data={'error':whrB['error'].values,
                                'Life Ladder':whrB['Life Ladder'].values,
                                'Country':whrB['Country'].values,
                                'Region_color': whrB['Region'].values})
color_mapper = CategoricalColorMapper(factors=whrB['Region'].unique(), palette=Category10_10)

p = figure(title='', plot_width = 1000, plot_height = 600)
p.circle(x = 'error', y= 'Life Ladder', size = 15, color = {'field': 'Region_color', 'transform': color_mapper},
             source = source,  legend_field='Region_color', fill_alpha = 0.2)
output_file("dark_minimal.html")
curdoc().theme = 'dark_minimal'
p.add_tools(HoverTool(tooltips=[("error", "$x"),("Life Ladder", "$y"), ("Country", "@Country")]))
p.xaxis.axis_label = 'error'
p.yaxis.axis_label = 'Life Ladder'
p.add_layout(LabelSet(x='error', y='Life Ladder', text='Country',text_font_size='6pt',
                  x_offset=0, y_offset=5, source=source, render_mode='canvas'))
p.legend.location = "top_right"
p.x_range = Range1d(-2, 2)
p.y_range = Range1d(1, 10)
from bokeh.models import BoxAnnotation
green_box = BoxAnnotation(left=-0.5, right=0.5, fill_color='green', fill_alpha=0.1)

p.legend.location = "top_left"

p.add_layout(green_box)

st.bokeh_chart(p)
st.caption("*Pour faciliter la lecture, nous la moyenne sur l'ensemble des années des deux séries de données.")

if st.checkbox('Afficher les pays dont le modèle à mal estimé le score de bonheur', value=False):
    col1, col2 = st.columns(2)
    col1.write('Pays dont le score a été sous-estimé par le modèle :')
    col1.write(whr[whr['error'] > 1][['Country', 'Life Ladder', 'error']].sort_values(by='error', ascending=False).head(25).set_index("Country", drop=True, append=False, verify_integrity=False))
    col2.write('Pays dont le score a été sur-estimé par le modèle :')
    col2.write(whr[whr['error'] < -1][['Country', 'Life Ladder', 'error']].sort_values(by='error', ascending=False).tail(25).set_index("Country", drop=True, append=False, verify_integrity=False))

