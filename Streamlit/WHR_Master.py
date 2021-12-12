import streamlit as st
from multiapp import MultiApp
import home, data, model # import your app modules here

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

app = MultiApp()

# Add all your application here
app.add_app("Accueil", home.app)
app.add_app("Analyse d'une corrélation", data.app)
app.add_app("Modèle de prédiction", model.app)

# The main app
app.run()