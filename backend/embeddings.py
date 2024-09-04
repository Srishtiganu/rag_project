import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
# from chromadb.utils import embedding_functions

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# given text chunk list, create embeddings function:
def create_embeddings(text_chunks):
    embeddings = []
    for chunk in text_chunks: 
        #make embedding for chunk w/ openai
        response = client.embeddings.create(input=chunk, model="text-embedding-ada-002")  # openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")
        embeddings.append(response['data'][0]['embedding']) #add to the embeddings list
    return embeddings

# put embeddings in chromadb function
def store_embeddings(embeddings, text_chunks):
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="pdf_chunks")
    for i in range(len(embeddings)): #for each embedding
        embedding = embeddings[i]  # get embedding @ index i
        text = text_chunks[i]      # get corresponding text chunk @ index i
        # Add embedding and its text to chromadb collection  
        collection.add(embedding=embedding, metadata={"text": text})