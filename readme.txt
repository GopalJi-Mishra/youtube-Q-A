The project:
- Splits a text into chunks.
- Converts the chunks into embeddings using Sentence Transformers.
- Stores the embeddings in a FAISS vector database.
- Finds the most relevant chunks for a user's question.
- Sends the retrieved context to the Gemini API to generate an answer.