import json

def load_website_data(json_file):
    """
    Load website data from a JSON file and split it into individual pages.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    pages = []
    for entry in data:
        # Split the text field using the separator "===="
        page_texts = entry["text"].split("%#$%#$")
        # Clean up the pages (remove leading/trailing whitespace)
        page_texts = [page.strip() for page in page_texts if page.strip()]
        pages.extend(page_texts)
    
    return pages