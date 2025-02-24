from pdf_processor import find_page_number
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

def process_pdf(file_path): 
    # page index is page number in the pdf, and page_number is the actual page number.
    page_idx = find_page_number(file_path)
    # need to remove pages before page 1
    
    loader = PyPDFLoader(file_path)
    pages = 
    