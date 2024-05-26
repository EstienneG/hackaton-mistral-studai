import streamlit as st
import json

if "chapter_qcm" not in st.session_state:
    st.session_state["chapter_qcm"] = ""

# Function to load a question from a JSON file
def load_question(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

# Function to display a quiz
def display_quiz(data, quiz_index):
    question = data["question"]
    options = data["options"]
    correct_answer = data["correct_answer"]

    if f'selected_option_{quiz_index}' not in st.session_state:
        st.session_state[f'selected_option_{quiz_index}'] = None
    if f'submitted_{quiz_index}' not in st.session_state:
        st.session_state[f'submitted_{quiz_index}'] = False

    def submit_answer(option):
        st.session_state[f'selected_option_{quiz_index}'] = option
        st.session_state[f'submitted_{quiz_index}'] = True

    st.markdown(f"<h1 style='text-align: center;'>{question}</h1>", unsafe_allow_html=True)

    cols = st.columns(4)
    for idx, option in enumerate(options):
        with cols[idx]:
            if st.session_state[f'submitted_{quiz_index}']:
                if option == correct_answer:
                    btn_color = "green"
                else:
                    btn_color = "red"
                st.button(option, key=f'{option}_{quiz_index}', disabled=True, on_click=submit_answer, args=(option,))
            else:
                st.button(option, key=f'{option}_{quiz_index}', on_click=submit_answer, args=(option,))

    if st.session_state[f'submitted_{quiz_index}']:
        if st.session_state[f'selected_option_{quiz_index}'] == correct_answer:
            st.success("Correct!")
        else:
            st.error(f"Incorrect! The correct answer is {correct_answer}.")

# Function to load multiple quizzes
def load_multiple_quizzes(json_paths):
    #st.write(json.loads(st.session_state["chapter_qcm"])["exercise"])
    for idx, data in enumerate(json.loads(st.session_state["chapter_qcm"])["exercise"]):
        st.write(f"### Quiz {idx + 1}")
        #data = load_question(json_path)
        display_quiz(data, idx)
        # Add a separating line between exercises
        st.markdown("<hr style='border: 3px solid grey; margin: 25px 0;'>", unsafe_allow_html=True)

# Specify the list of JSON files
json_files = ['/Users/othmane/Desktop/OTHO_CODING/Mistral_AI_Hackathon/hackaton-mistral-studai/Front/test_2/pages/quizz_2.json', '/Users/othmane/Desktop/OTHO_CODING/Mistral_AI_Hackathon/hackaton-mistral-studai/Front/test_2/pages/quizz.json']  # Add your JSON file paths here

# Load and display the quizzes
if "chapter_qcm" in st.session_state:
    load_multiple_quizzes(json_files)

# Apply custom CSS for button colors
st.markdown("""
    <style>
    .btn-green {
        background-color: green;
        color: white;
    }
    .btn-red {
        background-color: red;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
