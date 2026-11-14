
# LangChain Notes

LangChain is a framework for building applications powered by Large Language Models (LLMs). It provides components to connect models with prompts, data sources, tools, and workflows.

## LLMs

LLMs are models trained on large amounts of text data. They understand and generate human-like text based on the input they receive.

### Popular LLMs

- GPT by OpenAI
- Gemini by Google
- Claude by Anthropic
- Llama by Meta

### Important Concepts

- Temperature controls the randomness of the model's responses.
- Max tokens controls the maximum number of tokens generated.
- An LLM generates responses based on patterns learned during training.

## Prompts

A prompt is the instruction or input given to an LLM to guide its response.

### Prompt Templates

Prompt templates allow us to create reusable prompts with dynamic values.

### Chat Prompt Templates

Chat prompt templates help structure messages using roles such as system, human, and AI.

## Document Loaders

Document loaders are used to load data from different sources into LangChain.

### TextLoader

Loads content from text files. Usually creates one Document object for each file.

### PyPDFLoader

Loads PDF files. Typically creates one Document object per PDF page.

### CSVLoader

Loads CSV files. By default, creates one Document object per row.

### WebBaseLoader

Loads and extracts content from web pages.

## Text Splitters

Text splitters divide large documents into smaller chunks.

### CharacterTextSplitter

Splits text using a specified separator, such as a newline.

### RecursiveCharacterTextSplitter

Tries different separators hierarchically to split text into manageable chunks.

### TokenTextSplitter

Splits text based on tokens rather than characters.

### MarkdownHeaderTextSplitter

Splits Markdown documents based on headings and stores heading information in metadata.

## Retrieval-Augmented Generation (RAG)

RAG combines information retrieval with LLM generation. It allows an LLM to use external documents when answering questions.

### Indexing

- Load documents.
- Split documents into chunks.
- Generate embeddings.
- Store embeddings in a vector database.

### Retrieval

- Receive a user question.
- Convert the question into an embedding.
- Search for similar chunks.
- Retrieve relevant information.

### Generation

The retrieved information is added to the prompt, and the LLM generates an answer using that context.
