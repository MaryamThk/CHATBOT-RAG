import json
from cleanup import load_website_data
from retriever import Retriever
from generator import Generator
import time  # Add this import for timing

class Chatbot:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def respond(self, user_query):
        """Generate a response to the user's query."""
        print("Step 1: Retrieving relevant documents...")
        start_time = time.time()
        retrieved_docs = self.retriever.retrieve(user_query)
        print(f"Retrieved {len(retrieved_docs)} documents in {time.time() - start_time:.2f} seconds.")

        print("Step 2: Combining documents into context...")
        context = " ".join(retrieved_docs)

        print("Step 3: Generating response using context...")
        prompt = f"Context: {context}\nQuestion: {user_query}\nAnswer:"
        start_time = time.time()
        response = self.generator.generate(prompt)
        print(f"Generated response in {time.time() - start_time:.2f} seconds.")

        return response

# Load website data
def load_website_data(json_file):
    """
    Load website data from a JSON file and split it into individual pages.
    """
    print("Loading website data...")
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    pages = []
    for entry in data:
        # Split the text field using the separator "===="
        page_texts = entry["text"].split("====")
        # Clean up the pages (remove leading/trailing whitespace)
        page_texts = [page.strip() for page in page_texts if page.strip()]
        pages.extend(page_texts)
    
    print(f"Loaded {len(pages)} pages.")
    return pages

# Test the chatbot
if __name__ == '__main__':
    # Load website data
    print("Initializing chatbot...")
    website_data = load_website_data("znu_pages.json")

    # Initialize the chatbot
    chatbot = Chatbot()
    print("Adding documents to the retriever...")
    start_time = time.time()
    chatbot.retriever.add_documents(website_data)
    print(f"Added documents in {time.time() - start_time:.2f} seconds.")

    # Ask a question
    user_query = "سامانه آموزش مجازی دانشکده انسانی"     
    print(f"User query: {user_query}")
    start_time = time.time()
    response = chatbot.respond(user_query)
    print(f"Total response time: {time.time() - start_time:.2f} seconds.")

    print("Chatbot Response:", response)