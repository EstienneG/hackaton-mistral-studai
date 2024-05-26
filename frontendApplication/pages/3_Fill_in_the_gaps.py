import streamlit as st
import json
import random

if "chapter_exercise" not in st.session_state:
    st.session_state["chapter_exercise"] = ""

def load_exercise(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data["exercise"]

def display_exercise(exercise, exercise_num):
    content = exercise["exercise"]["content"]
    answers = exercise["exercise"]["answers"]

    # Extract keys and all possible options (correct and false)
    keys = list(answers.keys())
    options = {}
    for key in keys:
        correct_answer = answers[key]["correct"]
        false_answers = answers[key]["false"]
        
        # Handle case where false answers can be a singular string or a list of strings
        if isinstance(false_answers, str):
            false_answers = [false_answers]
        
        options[key] = [correct_answer] + false_answers

    # Shuffle options for each key to randomize answer positions
    for key in options:
        random.shuffle(options[key])

    # Replace <key_n> with actual gaps
    for key in keys:
        content = content.replace(key, "_____")

    # Display content with gaps
    st.write(f"### Exercise {exercise_num}")
    st.write(content)

    # Create a form to capture user's selections
    user_answers = {}
    with st.form(f"exercise_form_{exercise_num}"):
        i = 0
        for key in keys:
            i += 1
            user_answers[key] = st.selectbox(f"Question n° {i}", options[key], key=f"selectbox_{exercise_num}_{i}")
        submit_button = st.form_submit_button("Submit")

    # Display results if form is submitted
    if submit_button:
        st.write("### Your Answers")
        correct_count = 0
        total_questions = len(keys)
        i = 0

        for key in keys:
            i += 1
            user_answer = user_answers[key]
            correct_answer = answers[key]["correct"]
            
            if user_answer == correct_answer:
                correct_count += 1
                st.write(f"Question n° {i}: Correct!")
            else:
                st.write(f"Question n° {i}: Incorrect! Your answer: {user_answer}, Correct answer: {correct_answer}")

        # Display score
        st.write(f"### You got {correct_count} out of {total_questions} correct.")

def main():
    st.title("Fill in the Gaps Exercises")
    exercise = json.loads(st.session_state['chapter_exercise'])
    display_exercise(exercise, 1)

main()
