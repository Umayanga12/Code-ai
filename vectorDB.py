from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.Client()
collection = client.createCollection("chat_memory")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def add_message_to_db(message, role="user"):
    vector = embedder.encode(message).tolist()
    collection.add(
        ids=[str(len(collection.get(include="metadatas")["metadatas"]))],
        metadatas=[{"role": role, "content": message}],
        embeddings=[vector]
    )


def get_relevant_messages(query, k=5):
    query_vector = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["metadatas"]
    )
    # Extract message content
    return [m["content"] for m in results["metadatas"][0]]
