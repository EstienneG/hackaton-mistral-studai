import streamlit as st
import requests
# Setting the page configuration
st.set_page_config(
    page_title="STUDAI - Chapter Selection",
    page_icon=":mortar_board:",
    layout="wide"
)

if "chapters_structure" not in st.session_state:
        st.session_state["chapters_structure"] = None

# Load your logo image
logo = "logo.png"

# Function to display the chapter selection page
def chapter_selection_page():
    st.image(logo, width=150)
    st.title("STUDAI - Chapter Selection")

    if st.session_state['chapters_structure']:

        chapters = st.session_state['chapters_structure']

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

        num_columns = 3
        num_chapters = len(chapters)

        # Loop through the chapters and create buttons in columns
        for i in range(0, num_chapters, num_columns):
            cols = st.columns(num_columns)
            for j, col in enumerate(cols):
                chapter_index = i + j
                if chapter_index < num_chapters:
                    chapter = chapters[chapter_index]
                    with col:
                        if st.button(
                            f"Chapter {chapter_index + 1}: {chapter['chapter_name']}",
                            key=f"chapter_{chapter_index + 1}",
                            disabled="confirmed_selection" in st.session_state,
                        ):
                            st.session_state["selected_chapter"] = chapter['chapter_name']
                            st.session_state["selected_chapter_name"] = chapter['chapter_name']


        st.title("Choose your level")
        st.markdown('<div class="level-selection">', unsafe_allow_html=True)
        level = st.radio("Level", ["Beginner", "Intermediate", "Advanced"], key="level", disabled="confirmed_selection" in st.session_state)
        st.markdown('</div>', unsafe_allow_html=True)
        st.session_state["selected_level"] = level

        # Confirmation button
        if st.button("Confirm Selection", key="confirm_selection"):
            if "selected_chapter" in st.session_state and "selected_level" in st.session_state:
                st.session_state["confirmed_selection"] = True

                api_url = "http://127.0.0.1:8000/generate-summary"

                payload = {
                        "chapter_name": st.session_state['selected_chapter'],
                        "difficulty_selected": st.session_state['selected_level'], 
                        "db_workspace_name": ""
                }

                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                            # Afficher la réponse de l'API
                            result = response.json()
                            st.session_state["chapter_summary"] = result["chapter_summary"]

                else:
                    st.write("Erreur dans l'appel à l'API:", response.status_code)


        # Display the selection if confirmed
        if "confirmed_selection" in st.session_state:
            st.write(f"Confirmed Selection: Chapter {st.session_state['selected_chapter']} at {st.session_state['selected_level']} level.")

if __name__ == "__main__":
    chapter_selection_page()
