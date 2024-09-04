from flask import Flask, request, jsonify
import chromadb
from openai import OpenAI
from pdf_process import pdf_to_text_chunks
from embeddings import create_embeddings

app = Flask(__name__)

# Assuming you have set your OpenAI API key properly
client = OpenAI()

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        # Initialize ChromaDB client
        chroma_client = chromadb.Client()
        collection = chroma_client.get_collection("pdf_chunks")
        
        # Retrieve text chunks from ChromaDB
        text_chunks = [item['metadata']['text'] for item in collection.get_items()]

        # Create embeddings for text chunks
        embeddings = create_embeddings(text_chunks)

        # Perform similarity search to find the most similar chunk
        query_embedding = openai.Embedding.create(input=user_query, model="text-embedding-ada-002")['data'][0]['embedding']
        results = collection.query(query_embedding, n_results=1)
        most_similar_chunk = results[0]['metadata']['text']

        # Construct prompt for LLAMA Index
        prompt = f"Answer the user question based on the following context:\n\n{most_similar_chunk}\n\nUser question: {user_query}"

        # Generate response using LLAMA Index
        response = openai.Completion.create(prompt=prompt, model="text-llama-index")

        return jsonify({"response": response['choices'][0]['text']}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error handling query: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
