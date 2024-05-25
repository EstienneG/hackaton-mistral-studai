import streamlit as st

# Setting the page configuration
st.set_page_config(
    page_title="STUDAI - Chapter Selection",
    page_icon=":mortar_board:",
    layout="wide"
)

# Load your logo image
logo = "/Users/othmane/Desktop/OTHO_CODING/Streamlit/001/test_2/logo.png"

# Function to display the chapter selection page
def chapter_selection_page():
    st.image(logo, width=100)
    st.title("STUDAI - Chapter Selection")

    chapters = [
        {"number": 1, "title": "Introduction", "description": "An overview of the course."},
        {"number": 2, "title": "Basics", "description": "Learn the basics of the subject."},
        {"number": 3, "title": "Advanced Concepts", "description": "Deep dive into advanced topics."},
        {"number": 4, "title": "Case Studies", "description": "Explore practical case studies."}
    ]

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

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(f"Chapter 1: Introduction\nAn overview of the course.", key="chapter_1", disabled="confirmed_selection" in st.session_state, help="An overview of the course."):
            st.session_state["selected_chapter"] = 1

    with col2:
        if st.button(f"Chapter 2: Basics\nLearn the basics of the subject.", key="chapter_2", disabled="confirmed_selection" in st.session_state, help="Learn the basics of the subject."):
            st.session_state["selected_chapter"] = 2

    with col3:
        if st.button(f"Chapter 3: Advanced Concepts\nDeep dive into advanced topics.", key="chapter_3", disabled="confirmed_selection" in st.session_state, help="Deep dive into advanced topics."):
            st.session_state["selected_chapter"] = 3

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button(f"Chapter 4: Case Studies\nExplore practical case studies.", key="chapter_4", disabled="confirmed_selection" in st.session_state, help="Explore practical case studies."):
            st.session_state["selected_chapter"] = 4

    st.title("Choose your level")
    st.markdown('<div class="level-selection">', unsafe_allow_html=True)
    level = st.radio("Level", ["Beginner", "Intermediate", "Advanced"], key="level", disabled="confirmed_selection" in st.session_state)
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state["selected_level"] = level

    # Confirmation button
    if st.button("Confirm Selection", key="confirm_selection"):
        if "selected_chapter" in st.session_state and "selected_level" in st.session_state:
            st.session_state["confirmed_selection"] = True

    # Display the selection if confirmed
    if "confirmed_selection" in st.session_state:
        st.write(f"Confirmed Selection: Chapter {st.session_state['selected_chapter']} at {st.session_state['selected_level']} level.")

if __name__ == "__main__":
    chapter_selection_page()
