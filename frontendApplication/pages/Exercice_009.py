import streamlit as st
import json

# Load JSON data
file_path = '/Users/othmane/Desktop/OTHO_CODING/Mistral_AI_Hackathon/hackaton-mistral-studai/Front/test_2/pages/draft_2.json'
with open(file_path, 'r') as file:
    data = json.load(file)

exercise = data["exercise"]

content = exercise["content"]
answers = exercise["answers"]

# Extract keys and options
keys = list(answers.keys())
options = {key: [answers[key]["correct"], answers[key]["false"]] for key in keys}

# Replace <key_n> with actual gaps
for key in keys:
    content = content.replace(key, "_____")

# Create Streamlit form for user interaction
st.title("Fill in the Gaps Exercise")

# Display content with gaps
st.write(content)

# Create a form to capture user's selections
user_answers = {}
with st.form("exercise_form"):
    i = 0
    for key in keys:
        i+=1
        user_answers[key] = st.selectbox(f"Question n° {i}", options[key])
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
            result = "Correct"
            st.write(f"Question n° {i}: Correct!")

        else:
            result = "Incorrect"
            st.write(f"NOT TRUE -> Your answer: {user_answer}, Correct answer: {correct_answer}")

    # Display score
    st.write(f"### You got {correct_count} out of {total_questions} correct.")
