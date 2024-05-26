import fitz  # PyMuPDF
import re
from unstructured.partition.pdf import partition_pdf
import unstructured
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain.vectorstores import Chroma
from uuid import uuid4
import logging
import json
import os


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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_document(pdf_path: str, api_key: str, output_path: str, embedding_model_name: str, workspace_name: str):
    try:
        logger.info("Initializing PDF Processor...")
        processor = PDFProcessor(pdf_path)

        # Extract and clean text from the PDF
        logger.info("Extracting and cleaning text from PDF...")
        text = processor.extract_and_clean_text()
        if not text:
            raise ValueError("No text extracted from the PDF.")

        logger.info("Partitioning PDF and splitting text by chapters...")
        processor.partition_pdf()
        processor.split_text_by_chapters()
        structured_text = processor.transform_sections_to_array()

        if not structured_text:
            raise ValueError("Failed to transform sections into array.")

        logger.info(f"Structured text length: {len(structured_text)}")

        transformed_text = processor.transform_array(structured_text)

        # Convert list to string with a space separator
        structured_text_str = ' '.join(structured_text)

        # Initialize the text splitter
        logger.info("Splitting text into chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20, separators=['Chapter:', '\n\n'])
        chunks = splitter.split_text(structured_text_str)
        if not chunks:
            raise ValueError("No chunks generated from the structured text.")

        logger.info(f"Number of chunks created: {len(chunks)}")

        docs = splitter.create_documents(chunks)

        # Initialize MistralAI embeddings and ChromaDB
        logger.info("Initializing MistralAI embeddings and ChromaDB...")
        mistral_embeddings = MistralAIEmbeddings(api_key=api_key)
        mistral_embeddings.model = embedding_model_name

        output_path = f"../data/{workspace_name}/chromadb"
        os.makedirs(output_path, exist_ok=True)

        if not os.path.exists(os.path.join(output_path, 'index')):
            chroma_db = Chroma.from_documents(docs, mistral_embeddings, persist_directory=output_path)
            logger.info("ChromaDB created and persisted.")
        else:
            logger.info("ChromaDB already exists. Skipping creation.")

        chapters_structure = []
        for chapter in processor.chapters:
            chapters_structure.append({
                "chapter_name": chapter,
                "chapter_id": str(uuid4())
            })

        # Write chapters to a JSON file
        json_output_path = f"{workspace_name}_chapters.json"
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(chapters_structure, json_file, ensure_ascii=False, indent=4)
        
        logger.info(f"Chapters information written to {json_output_path}")
        logger.info("Document processing completed successfully.")
        return chapters_structure

    except Exception as e:
        logger.error(f"Failed to process document: {e}")
        raise e

