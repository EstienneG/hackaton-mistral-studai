import streamlit as st
import requests

font_import = """
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;700&display=swap" rel="stylesheet">
"""

# HTML and JavaScript for drag-and-drop functionality with adaptable answer boxes
drag_and_drop_html = """
    <div>
        <style>
            .draggable {
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
            }
            .droppable {
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
            }
            body {
                font-family: 'Source Sans Pro', sans-serif;
                font-size: 22px;
                color: white;
            }
        </style>
        <script>
            function allowDrop(ev) {
                ev.preventDefault();
            }

            function drag(ev) {
                ev.dataTransfer.setData("text", ev.target.id);
            }

            function drop(ev) {
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                var dropbox = ev.target;
                if (dropbox.className == "droppable") {
                    dropbox.innerHTML = document.getElementById(data).innerHTML;
                    dropbox.style.border = '2px solid green';
                }
            }

            function resetDrop(ev) {
                ev.preventDefault();
                var data = ev.dataTransfer.getData("text");
                var dropbox = ev.target;
                if (dropbox.className == "droppable") {
                    dropbox.innerHTML = "";
                    dropbox.style.border = '2px dashed #ccc';
                }
            }
        </script>
        <h1><strong>Drag the answers to the blanks:</strong></h1>
        <div id="answers" ondrop="resetDrop(event)" ondragover="allowDrop(event)">
            <div id="Amazon River" class="draggable" draggable="true" ondragstart="drag(event)">Amazon River oooooooooooo AHAHA LLEL MMO</div>
            <div id="Nile River" class="draggable" draggable="true" ondragstart="drag(event)">Nile River</div>
            <div id="Mississippi River" class="draggable" draggable="true" ondragstart="drag(event)">Mississippi River</div>
            <div id="Atlantic Ocean" class="draggable" draggable="true" ondragstart="drag(event)">Atlantic Ocean</div>
            <div id="Mediterranean Sea" class="draggable" draggable="true" ondragstart="drag(event)">Mediterranean Sea</div>
            <div id="Indian Ocean" class="draggable" draggable="true" ondragstart="drag(event)">Indian Ocean</div>
            <div id="Egypt" class="draggable" draggable="true" ondragstart="drag(event)">Egypt</div>
        </div>
        <br/>
        <p>The longest river in the world is the 
        <div id="blank1" class="droppable" ondrop="drop(event)" ondragover="allowDrop(event)"></div>, 
        which flows through 
        <div id="blank2" class="droppable" ondrop="drop(event)" ondragover="allowDrop(event)"></div> 
        and empties into the 
        <div id="blank3" class="droppable" ondrop="drop(event)" ondragover="allowDrop(event)"></div>.</p>
    </div>
"""

# Function to check the answers
def check_answers(dropped_answers):
    correct_answers = {
        "blank1": "Nile River",
        "blank2": "Egypt",
        "blank3": "Mediterranean Sea"
    }
    return all(dropped_answers[blank] == correct_answer for blank, correct_answer in correct_answers.items())

# Placeholder for user inputs
dropped_answers = {"blank1": "", "blank2": "", "blank3": ""}

# Button to check answers
if st.button("Submit"):
    # Simulate getting the dropped answers (you would need to get these values from the actual HTML in a real scenario)
    dropped_answers["blank1"] = st.session_state.get("blank1", "")
    dropped_answers["blank2"] = st.session_state.get("blank2", "")
    dropped_answers["blank3"] = st.session_state.get("blank3", "")
    
    api_url = "http://127.0.0.1:8000/generate-summary"

    payload = {
            "chapter_selected": "chapitre 1",
            "difficulty_selected": "Qu'il est difficile d'être le roi de la France"
    }

    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        # Afficher la réponse de l'API
        result = response.json()
        st.write("Réponse de l'API :", result["chapter_summary"])
    else:
        st.write("Erreur dans l'appel à l'API:", response.status_code)


    if check_answers(dropped_answers):
        st.success("Correct!")
    else:
        st.error("Incorrect. Please try again.")