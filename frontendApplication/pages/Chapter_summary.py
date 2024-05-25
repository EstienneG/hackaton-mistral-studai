import streamlit as st

# Setting the page configuration
st.set_page_config(
    page_title="STUDAI - Chapter summary",
    page_icon=":mortar_board:",
    layout="wide"
)

# Load your logo image
logo = "logo.png"


summary_content = """
Course Title: The Cold War: A Fun and Friendly Introduction (300 words)\n\nNewbie:\nWelcome to our course on the Cold War! The Cold War was a state of political and military tension after World War II, between the Western Bloc (led by the United States) and the Eastern Bloc (led by the Soviet Union). It lasted from 1947 to 1991 and never resulted in direct military action between the two superpowers, but it did lead to numerous proxy wars around the world. The main goal of the Western Bloc was to "contain" the Communist ideology of the Soviet Union from spreading to other parts of the world.\n\nIntermediate:\nNow that we have a basic understanding of the Cold War, let\'s dive a little deeper. Containment was a United States policy using numerous strategies to prevent the spread of communism abroad. The policy was a response to the Soviet Union\'s efforts to spread communism and was the centerpiece of U.S. foreign policy from the late 1940s through the 1980s. The Cold War was also characterized by a high level of ideological tension between the Soviet Union\'s Communist government and the United States\' democratic government.\n\nAdvanced:\nFor those of you who are ready, let\'s take a closer look at some specific events during the Cold War. The Cuban Missile Crisis in 1962 was a 13-day confrontation between the United States and the Soviet Union initiated by the American discovery of Soviet ballistic missile deployment in Cuba. It is often considered the closest the Cold War came to escalating into a full-scale nuclear war. Another significant event was the construction of the Berlin Wall in 1961, which separated East and West Berlin and became a symbol of the Cold War, representing the division of East and West.\n\nIn summary, the Cold War was a state of political and military tension between the Western Bloc and the Eastern Bloc, with the main goal of the Western Bloc being to "contain" the spread of communism. The ideological differences between the two systems fueled the conflict, which lasted from 1947 to 1991 and never resulted in direct military action between the two superpowers, but did lead to numerous proxy wars around the world.\n\nNote: This is a simplified version of the course and it\'s not possible to cover all the aspects of the Cold War in such a limited space, but I hope it gives a good starting point for those who are new to the topic.
"""


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
    st.markdown(f"<div style='text-align: justify; font-size: 16px; color: #333;'>{summary_content}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    chapter_selection_page()
