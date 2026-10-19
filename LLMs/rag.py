from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from llm_client import get_llm_response
import numpy as np

print("=== Simple RAG Chatbot ===")
print("Type 'exit' to quit.\n")


# Step1: Internal Knowledge Base
documents = [
    "Company policy states that employees get 20 days of paid leave.",
    "Vikash is a Senior Data Scientist working in the AI team.",
    "The company follows a hybrid work model with 3 days in office.",
    "Employees receive health insurance and performance bonuses."
]


# Step2: Create Embeddings
vectorizer = TfidfVectorizer()
doc_embeddings = vectorizer.fit_transform(documents)
# fit_transform(): fit() + transform()
# fit(): The vectorizer examines all four documents, builds a vocabulary of unique words, and learns the inverse document frequency (IDF) statistics.
# Transform(): It converts each document into a numerical TF-IDF vector based on that learned vocabulary and those statistics.
# The variable doc_embeddings contains the numerical representation of each document.



# Step3: Retrieval Function

# query: The user's question.
# top_k: The number of documents to retrieve.
def retrieve(query, top_k=2):

    # use transform(), not fit_transform(), Why? Because you already learned the vocabulary and IDF statistics from your knowledge base. You want the question to use that same representation.
    # [query] wraps the question in a list because the vectorizer expects a list of text documents.
    query_vec = vectorizer.transform([query])

    # This compares the user's question against every document in the knowledge base.
    # cosine_similarity() returns a 2D array, The [0] at the end extracts the first row from the similarity matrix, giving you a one-dimensional array of similarity scores.
    # [:top_k]: Since top_k = 2, this selects the first two indices.
    similarities = cosine_similarity(query_vec, doc_embeddings)[0]

    # np.argsort(similarities): Returns the indices that would arrange the scores from smallest to largest.
    # [::-1]: Reverses the order. Now the highest-scoring document comes first.
    top_indices = np.argsort(similarities)[::-1][:top_k]

    print("===== Printing variables as logs for debugging =====")
    print(f"Cosine similarity return:\n{cosine_similarity(query_vec, doc_embeddings)}")
    print(f"Cosine similarity with [0]:\n{cosine_similarity(query_vec, doc_embeddings)[0]}")
    print(f"np argsort return value: {np.argsort(similarities)}")
    print(f"np argsort [:top_k] value: {np.argsort(similarities)[::-1][:top_k]}")
    print("=======================================================")

    retrieved_documents = []
    for i in top_indices:
        retrieved_documents.append(documents[i])

    return retrieved_documents


# Step4: Chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # retrieved_docs is a list of strings. The join() method combines those strings into one string, placing a newline between each document.
    retrieved_docs = retrieve(user_input)
    context = "\n".join(retrieved_docs)

    # Step5: Augmented Prompt
    message = [
        {
            "role": "system",
            "content": "Answer ONLY using the provided context. If not found, say 'I dont know.'"
        },
        {
            "role": "user",
            "content": f"""
                Context:
                {context}

                Question:
                {user_input}
            """
        }
    ]

    response = get_llm_response(message)
    print("\n Retrieved Context: ")
    for doc in retrieved_docs:
        print(doc)

    print(f"Bot's Response: {response}\n\n")