from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        text = ""
        for item in transcript:
            text += item["text"] + " "

        return text

    except Exception as e:
        return f"Error: {e}"

def create_chunks(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
def create_embeddings(chunks):
    return model.encode(chunks)

import faiss
import numpy as np
def create_faiss_index(chunk_embeddings):
    dimension = chunk_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(chunk_embeddings, dtype=np.float32))
    return index

def retrieve_chunks(query, model, index, chunks):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding, dtype=np.float32),k=3)
    context = ""
    for i in I[0]:
        context += chunks[i] + "\n"
    return context

import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model_gemini = genai.GenerativeModel("gemini-2.5-flash")

def create_prompt(query, context):

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    return prompt

def get_response(prompt):

    response = model_gemini.generate_content(prompt)

    return response.text

def main(video_id, query):
    text = get_transcript(video_id)
    chunks = create_chunks(text)
    chunk_embeddings = create_embeddings(chunks)
    index = create_faiss_index(chunk_embeddings)

    context = retrieve_chunks(query, model, index, chunks)
    prompt = create_prompt(query, context)
    answer = get_response(prompt)

    return answer