import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma(
    persist_directory="embedding",
    collection_name="book_by_page",
    embedding_function=embeddings
)

def extract_filters(query):
    filters = {}
    # Extract a page number if present (e.g., "page 15")
    page_match = re.search(r'page\s*(\d+)', query, re.IGNORECASE)
    # Extract a chapter number if present (e.g., "Chapter 2")
    chapter_match = re.search(r'chapter\s*(\d+)', query, re.IGNORECASE)
    # Extract a chapter name if mentioned with a syntax like "chapter name: Introduction"
    chapter_name_match = re.search(r'chapter\s*name\s*:\s*([\w\s]+)', query, re.IGNORECASE)
    
    if page_match:
        filters['page'] = int(page_match.group(1))
    if chapter_match:
        filters['chapter_number'] = int(chapter_match.group(1))
    if chapter_name_match:
        filters['chapter_name'] = chapter_name_match.group(1).strip()
    
    return filters

def build_chroma_filter(filters):
    if not filters:
        return None
    if len(filters) == 1:
        return filters
    # Combine multiple filter conditions using "$and"
    return {"$and": [{k: v} for k, v in filters.items()]}

def search_vectorstore(query, k=5):
    # Extract metadata filters from the query
    filters = extract_filters(query)
    print('This is the filter', filters)
    chroma_filter = build_chroma_filter(filters)
    print('This is the chorma filter', chroma_filter)
    
    # Perform the semantic search with the filter applied
    results = vector_store.similarity_search(query, k=k, filter=chroma_filter)
    
    # # Optional: Further manual filtering if needed
    # if filters:
    #     filtered_results = []
    #     for doc in results:
    #         match = True
    #         for key, value in filters.items():
    #             if doc.metadata.get(key) != value:
    #                 match = False
    #                 break
    #         if match:
    #             filtered_results.append(doc)
    #     results = filtered_results[:k]
    # else:
    #     results = results[:k]
    
    return results

def build_system_message(query):
    filter_result = search_vectorstore(query)
    
    print('vectorstore results', filter_result)
    
    base_message = (
        "You are a book expert answering questions using precise text references. "
        "Always cite sources using chapter name and page number. "
    )
    
    combined_context = f"{base_message}: {query}\n\n Supported text:\n" 
    for doc in filter_result:
        combined_context += f"{doc.page_content}\n\n"
        
    images = []
    for doc in filter_result:
        
        if doc.metadata.get('image_paths'):
            images.append(doc.metadata.get('image_paths'))
            
    print('combined context and images', combined_context, images)
            
    return combined_context, images