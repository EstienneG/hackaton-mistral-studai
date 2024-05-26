import streamlit as st
import requests
import json

# Setting the page configuration
st.set_page_config(
    page_title="STUDAI",
    page_icon=":mortar_board:",
    layout="centered"
)

# Load your logo image
logo = "./logo.png"

check = 0 

# Function to display the file upload page
def file_upload_page():
    st.image(logo, width=150)
    st.title("STUDAI")

    st.markdown("## Upload your files")
    st.markdown("Drag and drop your files here or select files from your computer")
    uploaded_file = st.file_uploader("Select files to upload", type=["pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx"])

    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file.name)
        file_contents = uploaded_file.read()

        if st.button("Upload class material"):
            # Prepare the file for upload
            files = {
                "upload_file": (uploaded_file.name, file_contents, uploaded_file.type)
            }

            api_url = "http://127.0.0.1:8000/upload_document"

            # Send the file to the API
            response = requests.post(api_url, files=files)


            # Display the response from the API
            if response.status_code == 200:
                st.success("File successfully uploaded !")
                st.session_state['chapters_structure'] = json.loads(response.text)['chapters']
        
            else:
                st.error(f"Failed to upload file. Status code: {response.status_code}")

    st.progress(0)
    st.markdown("Accepted file formats: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX")


# Main function to handle the navigation
file_upload_page()

