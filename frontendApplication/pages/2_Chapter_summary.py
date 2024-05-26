import streamlit as st
import requests

if "chapter_summary" not in st.session_state:
        st.session_state["chapter_summary"] = ""
        


# Setting the page configuration
st.set_page_config(
    page_title="STUDAI - Chapter summary",
    page_icon=":mortar_board:",
    layout="wide"
)

# Load your logo image
logo = "logo.png"

# Function to display the chapter selection page
def chapter_selection_page():
    st.image(logo, width=150)
    st.title("STUDAI - Chapter summary")

    st.markdown("""
        <style>
            div[data-testid="column"] {
                width: fit-content !important;
                flex: unset;
            }
            div[data-testid="column"] * {
                width: fit-content !important;
            }
            .chapter-button {
                padding: 1rem;
                margin: 0.5rem;
                border-radius: 10px;
                background-color: #f0f0f0;
                text-align: left;
                font-size: 1rem;
                font-weight: bold;
                color: #333;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .chapter-button:hover {
                background-color: #d0d0d0;
            }
            .level-selection {
                
                border-radius: 10px;
                background-color: #f9f9f9;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: justify; font-size: 16px; color: #333;">{st.session_state["chapter_summary"]}</div>', unsafe_allow_html=True)
    if st.button("Chapter understood!"):
        
        with st.spinner('Generating exercise'):
            api_url = "http://127.0.0.1:8000/generate-exercise"

            payload = {
                    "chapter_name": st.session_state['selected_chapter'],
                    "difficulty_selected": st.session_state['selected_level'],
                    "db_workspace_name": ""

            }

            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                # Afficher la réponse de l'API
                result = response.json()

                st.session_state['chapter_exercise'] = result['chapter_exercise']
            else:
                st.write("Erreur dans l'appel à l'API:", response.status_code)
        st.write('Exercise generated!')


if __name__ == "__main__":
    chapter_selection_page()
