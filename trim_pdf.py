from PyPDF2 import PdfReader, PdfWriter

def trim_pdf_before_page_one(input_path, output_path, page_one_index):
    """
    Remove all pages before the actual page 1 of the book from a PDF file.
    
    Args:
        input_path (str): Path to the input PDF file
        output_path (str): Path where the trimmed PDF will be saved
        page_one_index (int): The index (0-based) where page 1 of the book appears in the PDF
    """
    # Create PDF reader and writer objects
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Validate input
    if page_one_index >= len(reader.pages):
        raise ValueError("Page one index is larger than the number of pages in the PDF")
    
    # Copy pages starting from page_one_index to the end
    for page_num in range(page_one_index, len(reader.pages)):
        writer.add_page(reader.pages[page_num])
    
    # Save the trimmed PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

# Example usage
if __name__ == "__main__":
    # Example: If page 1 of the book is on page 5 of the PDF (index 4, since indexing starts at 0)
    input_file = "original_book.pdf"
    output_file = "trimmed_book.pdf"
    page_one_index = 4  # This means page 1 of the book is on page 5 of the PDF
    
    try:
        trim_pdf_before_page_one(input_file, output_file, page_one_index)
        print(f"Successfully trimmed PDF. Pages before index {page_one_index} have been removed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")