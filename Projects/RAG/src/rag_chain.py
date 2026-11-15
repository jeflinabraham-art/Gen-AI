import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

from src.schemas import RAGResponse, SourceCitation
from src.vector_store import format_docs, get_retriever, load_vectorstore

load_dotenv()

DEFAULT_PROMPT_PATH = Path("prompts/rag_prompt.txt")
DEFAULT_CHAT_MODEL = "gemini-3.8-flash"


# Read your prompt from a text file and convert it into a LangChain PromptTemplate object.
def load_rag_prompt(prompt_path: str|Path   = DEFAULT_PROMPT_PATH) -> PromptTemplate:
    path = Path(prompt_path)
    if not path.exists():
        raise FileNotFoundError(f"RAG prompt file not found: {path}")

    # Reads the entire contents of the text file and stores them in a string.
    template_text = path.read_text(encoding="utf-8")
    return PromptTemplate(
        template=template_text,
        input_variables=["context", "chat_history", "question"],
    )


def get_llm() -> GoogleGenerativeAI:
    api_key = os.getenv("GEMINI_API_KEY").strip()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    model_name = os.getenv("GEMINI_CHAT_MODEL", DEFAULT_CHAT_MODEL)

    try:
        # temperature=0 keeps answers more focused for educational demos.
        return GoogleGenerativeAI(
            model=model_name,
            api_key=api_key,

            # temperature=0 → Makes the model's output less random and generally more consistent.
            # Higher temperature → More variation and creativity in responses.
            # Lower temperature → More predictable and focused responses.
            temperature=0,
        )
    except Exception as exc:
        raise RuntimeError(
            "Could not create the GeminiAI chat client. Check GEMINI_API_KEY in your .env file."
        ) from exc


def get_llm_display_name() -> str:
    model_name = os.getenv("GEMINI_CHAT_MODEL", DEFAULT_CHAT_MODEL)
    return f"GeminiAI / {model_name}"


# Convert chat history into a properly formatted string that can be included in your LLM prompt. eg:
# messages = [
#     {"role": "user", "content": "What is Python?"},
#     {"role": "assistant", "content": "Python is a programming language."}
# ]
def format_chat_history(messages: list[dict]) -> str:
    if not messages:
        return "No previous conversation."

    lines = []
    for message in messages:
        # Gets the role from the dictionary. If role is missing, it defaults to "user".
        role = message.get("role", "user")
        content = message.get("content", "").strip()

        # if content is empty, move to the next iteration.
        if not content:
            continue

        # Convert the role into a readable label
        label = "User" if role == "user" else "Assistant"
        lines.append(f"{label}: {content}")

    # This combines all list elements into one string, separating them with newline characters.
    return "\n".join(lines) if lines else "No previous conversation."


# Extract source information from retrieved documents and convert it into a list of SourceCitation objects.
def extract_sources(docs: list[Document]) -> list[SourceCitation]:
    citations: list[SourceCitation] = []

    # seen is a set where every element is a tuple containing a string and an optional integer.
    # Why do we need this?
    # To avoid adding the same file and page combination multiple times.
    seen: set[tuple[str, int | None]] = set()

    for doc in docs:
        filename = doc.metadata.get("filename")
        page = doc.metadata.get("page")
        res = (str(filename), page)
        if res in seen:
            continue
        seen.add(res)

        # .replace("\n", " ") → Replaces newline characters with spaces to make the preview display as a single line rather than multiple lines.
        preview = doc.page_content.strip().replace("\n", " ")
        if len(preview) > 160:
            preview = preview[:157] + "..."

        citations.append(
            SourceCitation(
                filename=str(filename),
                page=page,
                preview=preview,
            )
        )

    return citations


def ask_question(
    question: str = "",
    chat_history: list[dict] | None = None,
    k: int | None = None,
) -> RAGResponse:
    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("Please enter a question.")

    history = chat_history if chat_history else []

    # Load knowledge base and retrieve relevant chunks for this question.
    vectorstore = load_vectorstore()
    retriever = get_retriever(vectorstore, k=k)

    try:
        retrieved_docs = retriever.invoke(cleaned_question)
    except Exception as exc:
        raise RuntimeError(
            "Retrieval failed. Try rebuilding the knowledge base."
        ) from exc

    context = format_docs(retrieved_docs)
    history_text = format_chat_history(history)
    prompt = load_rag_prompt()
    llm = get_llm()

    # Fill the prompt with:
    # - retrieved document context (facts)
    # - conversation history (memory for follow-ups)
    # - the current user question
    final_prompt = prompt.format(
        context=context,
        chat_history=history_text,
        question=cleaned_question,
    )

    try:
        result = llm.invoke(final_prompt)

        # hasattr(result, "content"): Checks whether the returned object has an attribute named content.
        answer = result.content if hasattr(result, "content") else str(result)
    except Exception as exc:
        message = str(exc).lower()
        if "api key" in message or "authentication" in message or "unauthorized" in message:
            raise ValueError(
                "GeminiAI authentication failed. Check GEMINI_API_KEY in your .env file."
            ) from exc
        if "rate limit" in message:
            raise RuntimeError(
                "GeminiAI rate limit reached. Please wait a moment and try again."
            ) from exc
        raise RuntimeError(
            "The LLM failed to generate an answer. Check your GeminiAI API key, model name, and internet connection."
        ) from exc

    return RAGResponse(
        answer=str(answer).strip(),
        sources=extract_sources(retrieved_docs),
        num_chunks=len(retrieved_docs),
    )