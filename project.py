from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai

text = "Python is used for AI. FastAPI is a web framework. ML helps computers learn."

chunks = text.split(".")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

embeddings = np.array(embeddings, dtype=np.float32)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

genai.configure(api_key="YOUR_API_KEY")

gemini = genai.GenerativeModel("gemini-2.5-flash")


def ask(question):

    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding, dtype=np.float32)

    distances, indexes = index.search(question_embedding, 2)

    context = ""

    for i in indexes[0]:
        context = context + chunks[i] + " "

    prompt = "Context: " + context + "\nQuestion: " + question + "\nAnswer:"

    response = gemini.generate_content(prompt)

    return response.text


user_question = input("Ask your question: ")

answer = ask(user_question)

print(answer)