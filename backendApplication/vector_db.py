import fitz  # PyMuPDF
import re
from unstructured.partition.pdf import partition_pdf
import unstructured
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain.vectorstores import Chroma
from uuid import uuid4

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.full_text = ""
        self.chapters = []
        self.section_texts = {}

    def extract_and_clean_text(self):
        doc = fitz.open(self.pdf_path)

        for page in doc:
            text = self._extract_text_from_page(page)
            cleaned_text = self._clean_extracted_text(text)
            self.full_text += cleaned_text

        return self.full_text

    def _extract_text_from_page(self, page):
        text = ""
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        is_bold = span['flags'] & 16  # Bold flag
                        is_italic = span['flags'] & 2  # Italic flag
                        if span['size'] >= 14.0:  # Title
                            text += "# " + span['text'] + "\n"
                        else:
                            text += span['text'] + "\n"
        return text

    @staticmethod
    def _clean_extracted_text(text):
        lines = text.split('\n')
        cleaned_lines = []
        last_line_was_heading = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            current_line_is_heading = line.startswith("#")
            if current_line_is_heading and last_line_was_heading:
                line = line.replace('#', '')
            last_line_was_heading = current_line_is_heading

            if re.match(r'^#\s+CHAPITRE', line):
                line = "\n\n" + line

            if line.endswith('.'):
                cleaned_lines.append(line + "\n")
            else:
                cleaned_lines.append(line + " ")

        return ''.join(cleaned_lines).strip()

    def partition_pdf(self):
        elements = partition_pdf(self.pdf_path, strategy="hi_res")
        self.chapters = [
            element.text for element in elements if isinstance(element, unstructured.documents.elements.Title)
        ]

    def split_text_by_chapters(self):
        pattern = '|'.join([re.escape(section) for section in self.chapters])
        split_text = re.split(pattern, self.full_text)
        split_text = [section for section in split_text if section.strip()]

        for i, section in enumerate(self.chapters):
            if i < len(split_text):
                self.section_texts[section] = split_text[i + 1].strip()

    def transform_sections_to_array(self):
        structured_text = []
        for section, content in self.section_texts.items():
            structured_text.append(f"Chapter: {section}\nContent: {content}")
        return structured_text

    @staticmethod
    def transform_array(array):
        transformed_array = []

        for entry in array:
            chapter_title_match = re.match(r'Chapter: ([^\n]+)', entry)
            if not chapter_title_match:
                continue
            chapter_title = chapter_title_match.group(1)

            content_match = re.search(r'Content: (.+)', entry, re.DOTALL)
            if not content_match:
                continue
            content = content_match.group(1)

            sentences = re.split(r'(?<=\.) ', content)
            for sentence in sentences:
                transformed_array.append(f'Chapter: {chapter_title}\n{sentence.strip()}')

        return transformed_array

def upload_document(pdf_path:str, api_key:str, output_path:str, embedding_model_name:str):
    #pdf_path = "hackaton-mistral-studai/data/RAGAS_09_2023.pdf"
    processor = PDFProcessor(pdf_path)

    text = processor.extract_and_clean_text()
    processor.partition_pdf()
    processor.split_text_by_chapters()
    structured_text = processor.transform_sections_to_array()
    transformed_text = processor.transform_array(structured_text)

    # Convert list to string with a space separator
    structured_text = ' '.join(structured_text)

    # Initialize the text splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20, separators=['Chapter:', '\n\n'])
    chunks = splitter.split_text(structured_text)
    docs = splitter.create_documents(chunks)

    # Initialize MistralAI embeddings and ChromaDB
    api_key = "your_api_key_here"  # Replace with your actual API key
    output_path = "hackaton-mistral-studai/data/chromadb"
    mistral_embeddings = MistralAIEmbeddings(api_key=api_key)
    mistral_embeddings.model = "mistral-embed"  
    chroma_db = Chroma.from_documents(docs, mistral_embeddings, persist_directory=output_path)


    chapters_structure = [] 
    for chapter in processor.chapters:
        chapters_structure.append({
            "chapter_name": chapter,
            "chapter_id": uuid4()
        })
    
    return chapters_structure


