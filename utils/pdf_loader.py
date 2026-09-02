from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(pdf_path):
    """
    Load a single PDF file and return a list of LangChain Document objects.

    Args:
        pdf_path: Path to the uploaded PDF.

    Returns:
        List of LangChain Document objects.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    # Add custom metadata
    for doc in documents:
        doc.metadata["source_file"] = pdf_path.name
        doc.metadata["file_type"] = "pdf"

    return documents


