import os
import requests
import faiss
import numpy as np
import threading
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModel
from groq import Groq
from urllib.parse import urljoin

# Flask App Setup
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Set API Key for Groq
os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual API key
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Load Embedding Model (Sentence Transformers)
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# FAISS Vector Store
dimension = 384  # Embedding size for all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)
text_data = []

# Store visited URLs to avoid duplicates
visited_urls = set()

# Selenium Setup for JavaScript-rendered pages
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_embeddings(text):
    """Convert text to embeddings using Hugging Face model."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].detach().numpy()  # Extract CLS token

def get_child_urls(main_url):
    """Extract all internal links from the main website."""
    try:
        response = requests.get(main_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        child_urls = set()

        for link in soup.find_all("a", href=True):
            url = urljoin(main_url, link["href"])  # Convert relative URLs to absolute
            if url.startswith(main_url):  # Ensure it's an internal link
                child_urls.add(url)

        return child_urls

    except requests.RequestException as e:
        print(f"Error fetching {main_url}: {e}")
        return set()

def fetch_webpage(url):
    """Fetch webpage content, including JavaScript-rendered elements using Selenium."""
    if url in visited_urls:
        return None  # Skip already visited URLs

    visited_urls.add(url)

    try:
        driver.get(url)  # Load the page with JavaScript
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract page content
        title = soup.title.text if soup.title else "No Title"
        text = " ".join([p.text.strip() for p in soup.find_all("p")])
        headings = " ".join([h.text.strip() for h in soup.find_all(["h1", "h2", "h3"])])
        lists = " ".join([li.text.strip() for li in soup.find_all("li")])

        return {
            "url": url,
            "title": title,
            "text": text,
            "headings": headings,
            "lists": lists,
        }

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def crawl_website(start_url, max_pages=50):
    """Crawls website starting from the main URL, fetching child pages."""
    pages_to_visit = get_child_urls(start_url)

    while pages_to_visit and len(visited_urls) < max_pages:
        url = pages_to_visit.pop()
        print(f"Scraping: {url}")

        data = fetch_webpage(url)
        if data:
            store_in_faiss(data)
            new_links = get_child_urls(url)
            pages_to_visit.update([link for link in new_links if link not in visited_urls])

def store_in_faiss(data):
    """Stores extracted text in FAISS vector database."""
    global text_data
    for section in ["title", "text", "headings", "lists"]:
        content = data.get(section, "")
        if content:
            embedding = get_embeddings(content)
            index.add(embedding)  # Store in FAISS
            text_data.append(content)  # Store original text

def query_rag(question):
    """Query RAG system with improved general knowledge handling."""
    query_embedding = get_embeddings(question)
    distances, indices = index.search(query_embedding, 1)

    # Determine if FAISS context is relevant
    has_relevant_context = (
        len(text_data) > 0
        and indices.shape[0] > 0
        and indices[0][0] >= 0
        and indices[0][0] < len(text_data)
        and distances[0][0] < 1.0  # Only consider relevant context
    )

    retrieved_text = text_data[indices[0][0]] if has_relevant_context else "No specific context available."

    response = groq_client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI assistant providing detailed, general, and well-structured answers. "
                    "Offer a comprehensive overview with multiple perspectives, detailed explanations, and relevant external links. "
                    "Include the context as a reference only if relevant, but prioritize providing a general answer. "
                    "Format your response in Markdown with clear headings, bullet points, paragraphs, and links."
                ),
            },
            {
                "role": "user",
                "content": f"Context: {retrieved_text}\n\nQuestion: {question}",
            },
        ],
        max_tokens=1000,  # Increase token limit for detailed answers
        temperature=0.2,
        top_p=0.9,
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    main_url = "https://docs.google.com/document/u/1/d/e/2PACX-1vQB7SYIXQPJr0-WcfekVVSt488MdlkNzRUPacbRh2QgOALXcinPybopWIFlY83tdr_mH1QtrhCIsFUq/pub"
    print(f"Starting website crawl: {main_url}")
    crawl_website(main_url, max_pages=20)  # Crawl main and child pages
    app.run(debug=True)