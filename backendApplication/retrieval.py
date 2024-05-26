from langchain.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings


class VectorDatabaseHandler:
    def __init__(self, persist_directory, api_key, model="mistral-embed"):
        self.persist_directory = persist_directory
        self.api_key = api_key
        self.model = model
        self.db = None
        self.retriever = None

    def load_vector_database(self):
        mistral_embeddings = MistralAIEmbeddings(api_key=self.api_key)
        mistral_embeddings.model = self.model
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=mistral_embeddings)
        return self.db

    def define_retriever(self, k=15):
        if self.db is None:
            raise ValueError("Vector database is not loaded. Call load_vector_database() first.")
        self.retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": k})
        return self.retriever

    def extract_context(self, docs_retrieved):
        if not docs_retrieved:
            raise ValueError("No documents retrieved. Provide a list of retrieved documents.")
        
        first_line = str(docs_retrieved[0].page_content).split('\n')[0]
        context_parts = [first_line] + [
            doc.page_content.replace(first_line, '') for doc in docs_retrieved
        ]
        context = "\n".join(context_parts)
        return context


def retrieval(persist_directory, api_key, chapter_selected):

    handler = VectorDatabaseHandler(persist_directory, api_key)

    # Load the vector database
    db = handler.load_vector_database()

    # Define the retriever
    retriever = handler.define_retriever(k=15)

    # Simulate document retrieval (replace with actual retrieval logic)
    docs_retrieved = retriever.invoke(chapter_selected)

    # Extract context from retrieved documents
    context = handler.extract_context(docs_retrieved)

    return(context)