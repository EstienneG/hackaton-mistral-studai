import streamlit as st
import pandas as pd

# Setting the page configuration
st.set_page_config(
    page_title="STUDAI - Score table",
    page_icon=":mortar_board:",
    layout="wide"
)

# Load your logo image
logo = "logo.png"

# Exemple de données JSON
data = [
    {"Chapter": "Chapter 1", "Good answers": 8, "Wrong answers": 2},
    {"Chapter": "Chapter 2", "Good answers": 7, "Wrong answers": 3},
    {"Chapter": "Chapter 3", "Good answers": 9, "Wrong answers": 1}
]

df = pd.DataFrame(data)

# Titre de la page
st.title("Tableau des Scores")

# Affichage du tableau des scores
st.table(df)
