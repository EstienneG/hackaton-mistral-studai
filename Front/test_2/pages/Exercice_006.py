import streamlit as st
import streamlit.components.v1 as components
import json

font_import = """
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;700&display=swap" rel="stylesheet">
"""

# Function to load JSON data
def load_data():
    with open('/Users/othmane/Desktop/OTHO_CODING/Mistral_AI_Hackathon/hackaton-mistral-studai/Front/test_2/pages/draft.json') as f:
        data = json.load(f)
    return data

data = load_data()

# HTML and JavaScript for drag-and-drop functionality with adaptable answer boxes
drag_and_drop_html = f"""
    <div>
        <style>
            .draggable {{
                display: inline-block;
                padding: 8px;
                margin: 4px;
                background-color: #ddd;
                border: 1px solid #ccc;
                cursor: move;
                font-family: 'Source Sans Pro', sans-serif; /* Font family for answer options */
                font-size: 16px; /* Font size for answer options */
                font-weight: bold;
                color: black;
                text-align: center;
            }}
            .droppable {{
                display: inline-block;
                min-width: 150px; /* Minimum width of the answer boxes */
                min-height: 25px; /* Minimum height of the answer boxes */
                padding: 8px;
                margin: 4px;
                background-color: #2c3e50;
                border: 2px dashed #ccc;
                vertical-align: top;
                font-family: 'Source Sans Pro', sans-serif; /* Font family for blanks */
                font-size: 16px; /* Font size for blanks */
                font-weight: bold;
                color: white;
                text-align: center;
            }}
            body {{
                font-family: 'Source Sans Pro', sans-serif;
                font-size: 22px;
                color: white;
            }}
        </style>
        <script>
            function allowDrop(ev) {{
                ev.preventDefault();
            }}

            function drag(ev) {{
                ev.dataTransfer.setData("text", ev.target.id);
            }}

            function drop(ev) {{
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                var dropbox = ev.target;
                if (dropbox.className == "droppable") {{
                    dropbox.innerHTML = document.getElementById(data).innerHTML;
                    dropbox.style.border = '2px solid green';
                    dropbox.dataset.answer = data;
                }}
            }}

            function resetDrop(ev) {{
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                var dropbox = ev.target;
                if (dropbox.className == "droppable") {{
                    dropbox.innerHTML = "";
                    dropbox.style.border = '2px dashed #ccc';
                    dropbox.dataset.answer = "";
                }}
            }}
        </script>
        <h1><strong>Drag the answers to the blanks:</strong></h1>
        <div id="answers" ondrop="resetDrop(event)" ondragover="allowDrop(event)">
"""

# Adding the options to the HTML
for option in data['options']:
    drag_and_drop_html += f"""
        <div id="{option['id']}" class="draggable" draggable="true" ondragstart="drag(event)">{option['text']}</div>
    """

# Adding the sentence with blanks to the HTML
sentence_with_blanks = data['sentence']
for blank in data['answers']:
    sentence_with_blanks = sentence_with_blanks.replace(f"<{blank}>", f'<div id="{blank}" class="droppable" ondrop="drop(event)" ondragover="allowDrop(event)"></div>')

drag_and_drop_html += f"""
        </div>
        <br/>
        <p>{sentence_with_blanks}</p>
    </div>
"""

# Display the drag-and-drop interface
components.html(drag_and_drop_html + font_import, height=600)

# Function to check the answers
def check_answers(dropped_answers):
    return all(dropped_answers[blank] == correct_answer for blank, correct_answer in data['answers'].items())

# Placeholder for user inputs
dropped_answers = {blank: "" for blank in data['answers']}

# Button to check answers
if st.button("Submit"):
    # Simulate getting the dropped answers (you would need to get these values from the actual HTML in a real scenario)
    for blank in data['answers']:
        dropped_answers[blank] = st.session_state.get(blank, "")
    
    if check_answers(dropped_answers):
        st.success("Correct!")
    else:
        st.error("Incorrect. Please try again.")
