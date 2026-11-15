"""
This module is responsible for loading PDF/DOCX files, converting them into LangChain Documents, splitting them into chunks, and counting the uploaded files.
"""

# Path is a class from Python's built-in pathlib module. It helps you work with file and folder paths.
# You can then use methods such as: .exists(), .iterdir(), .suffix
from pathlib import Path

# These document loaders extract text and convert it into LangChain Document objects. PyPDFLoader generally creates one Document per PDF page, whereas Docx2txtLoader generally creates one Document for the extracted DOCX content.
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader

# A Document is a data structure that contains two important things:
# - page_content: the actual text.
# - metadata: additional information about that text.
from langchain_core.documents import Document

# It splits large documents into smaller chunks.
from langchain_text_splitters import RecursiveCharacterTextSplitter


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def load_documents(folder_path: str) -> list[Document]:

    # Converts the string path into a Path object.
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Document folder not found: {folder_path}")

    # files will contains file paths.
    files = []

    # folder.iterdir(): Returns the items directly inside the folder.
    for path in folder.iterdir():
        # path.is_file(): Checks whether the current entry is a file. It returns False for directories.
        if path.is_file():
            # path.suffix.lower(): Gets the file extension and converts it to lowercase.
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)

    if not files:
        raise ValueError(
            "No supported documents found. Please upload PDF or DOCX files."
        )

    documents: list[Document] = []
    for file_path in files:

        # This function returns a list of Documents. A PDF with 5 pages will generally return 5 Documents.
        loaded = _load_single_document(file_path)

        # Adds all the returned Document objects to the main documents list.
        documents.extend(loaded)

    # Remove empty pages / sections that would create useless embeddings.
    filtered_documents = []
    for doc in documents:
        if doc.page_content and doc.page_content.strip():
            filtered_documents.append(doc)

    documents = filtered_documents

    if not documents:
        raise ValueError(
            "Documents were found, but they appear to be empty or unreadable."
        )

    return documents


# This function loads one individual PDF or DOCX file.
# In Python, a leading underscore is a naming convention that indicates a function is intended for internal use within its module.
def _load_single_document(file_path: Path) -> list[Document]:

    # Get the file extension
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".pdf":
            # PyPDFLoader creates one Document per page and includes page numbers.
            loader = PyPDFLoader(file_path)
            docs = loader.load()
        elif suffix == ".docx":
            # DOCX loaders usually do not provide page numbers.
            loader = Docx2txtLoader(file_path)
            docs = loader.load()
        else:
            raise ValueError(
                f"Unsupported file type: {file_path.name}. "
                "Only PDF and DOCX files are supported."
            )
    # except catches an error that occurs inside the try block.
    # raise without an argument re-raises the original exception.
    except ValueError:
        raise

    # This handles other errors, such as:
    # - PDF is corrupted.
    # - File cannot be accessed.
    # - DOCX parsing fails.
    # - Unexpected loading errors occur.

    # Exception as exc catches the original error.
    # raise ValueError(...) creates a new, user-friendly error.
    # from exc preserves the original error as the cause.
    except Exception as exc:
        raise ValueError(
            f"Could not read '{file_path.name}'. "
            "The file may be invalid or corrupted."
        ) from exc

    for doc in docs:
        doc.metadata["filename"] = file_path.name
        # PDF loaders usually set "page" (0-based). Convert to 1-based for display.
        if "page" in doc.metadata and doc.metadata["page"] is not None:
            try:
                doc.metadata["page"] = int(doc.metadata["page"]) + 1
            # TypeError: You're trying to perform an operation using an incompatible data type. 
            # eg: int(None) ----- int() argument must be a string.

            # ValueError: The data type is acceptable, but the actual value is invalid for that operation.
            # eg: int("hello")
            except (TypeError, ValueError):
                doc.metadata["page"] = None
        else:
            doc.metadata["page"] = None

    return docs


def split_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[Document]:

    if not documents:
        raise ValueError("No documents to split.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,

        # why overlap? Imagine a sentence gets divided between two chunks. Without overlap, the second chunk might lose important context from the first.
        chunk_overlap=chunk_overlap,

        # It first tries to split at paragraph boundaries.
        # If a paragraph is too large, it tries line boundaries.
        # If a line is too large, it tries spaces.
        # As a final fallback, it can split at character boundaries.

        # This is why it is called RecursiveCharacterTextSplitter. It recursively tries smaller separators when the previous separator isn't sufficient to meet the target chunk size. No need to mention separators, RecursiveCharacterTextSplitter uses below separator by deafult.
        separators=["\n\n", "\n", " ", ""],
    )

    # Split large documents into smaller chunks before creating embeddings.
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Document splitting produced no chunks.")

    return chunks


def count_source_files(folder_path: str) -> int:
    folder = Path(folder_path)
    if not folder.exists():
        return 0

    count = 0
    for path in folder.iterdir():
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            count += 1

    return count