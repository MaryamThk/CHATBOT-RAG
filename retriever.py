from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch  # Add this import

class Retriever:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        # Load a pre-trained model to convert text into embeddings
        self.model = SentenceTransformer(model_name)
        # Move the model to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        # Initialize an empty FAISS index for similarity search
        self.index = None
        # Store the documents
        self.documents = []

    def add_documents(self, documents):
        """
        Add documents to the knowledge base.
        - `documents`: A list of strings (e.g., ["doc1", "doc2", ...])
        """
        self.documents = documents
        # Convert documents into embeddings (vector representations)
        embeddings = self.model.encode(documents, device=self.device)  # Use GPU if available
        # Create a FAISS index for efficient similarity search
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        # Add embeddings to the index
        self.index.add(embeddings)

    def retrieve(self, query, k=5):
        """
        Retrieve the top-k most relevant documents for a query.
        - `query`: The user's question (a string).
        - `k`: Number of documents to retrieve.
        """
        # Convert the query into an embedding
        query_embedding = self.model.encode([query], device=self.device)  # Use GPU if available
        # Search the FAISS index for the most similar documents
        distances, indices = self.index.search(query_embedding, k)
        # Return the retrieved documents
        return [self.documents[i] for i in indices[0]]