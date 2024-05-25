import streamlit as st
import requests

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

        # Define the API endpoint
        api_url = "https://your-api-endpoint.com/upload"
        
        if st.button("Upload class material"):
            # Prepare the file for upload
            files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}

            # Send the POST request
            response = requests.post(api_url, files=files)

            # Display the response from the API
            if response.status_code == 200:
                st.success("File successfully uploaded !")
                st.session_state["page"] = "chapter_selection"
        
            else:
                st.error(f"Failed to upload file. Status code: {response.status_code}")

    st.progress(0)
    st.markdown("Accepted file formats: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX")


# Main function to handle the navigation
file_upload_page()

