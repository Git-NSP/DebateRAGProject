from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(documents, chunk_size=1000,chunk_overlap=200):
    """Split documents into smaller chunks for better RAG performance"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")
    
    if chunks:
        print(f"\nExample chunk:")
        print(f"Content: {chunks[0].page_content[:20]}...")
        print(f"Metadata: {chunks[0].metadata}")
    
    return chunks
    
