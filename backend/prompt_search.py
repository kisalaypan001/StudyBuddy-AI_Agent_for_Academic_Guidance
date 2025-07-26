#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

from flask import Flask, render_template, request
import groq
from langchain_community.tools import DuckDuckGoSearchResults
import re

app = Flask(__name__)

# Function to classify if a query is education-related
def is_query_education_related(api_key, query, model="gemma2-9b-it"):
    client = groq.Client(api_key=api_key)
    
    validation_prompt = f"""
    Classify the following query: "{query}"
    - If the query is related to **any educational topic**, including science, history, psychology, university learning, research, artificial intelligence, machine learning, data structures, programming languages,algorithms, or computer science, respond with "Education".
    - If the query is about **writing or debugging code**, respond with "Programming".
    - If the query is about **movies, music, entertainment, gaming, or sports**, respond with "Entertainment".
    - If the query does not fit any of these, respond with "Other".
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": validation_prompt}]
    )
    result = response.choices[0].message.content.strip().lower()
    
    return result == "education"

# Function to get AI response if query is education-related
def get_ai_response(api_key, query, model="gemma2-9b-it"):
    client = groq.Client(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content.strip()

# Function to format search results (excluding links)
def format_search_results(result):
    md_output = "## **Education-Related Search Results**\n\n"
    
    pattern = r"title:\s*(.*?)\s*snippet:\s*(.*?)\s*(?=title:|$)"
    matches = re.findall(pattern, result, re.DOTALL)

    if not matches:
        return "No relevant educational search results were found."

    for title, snippet in matches:
        summary = " ".join(snippet.strip().split()[:40])  # Limit summary to ~40 words
        md_output += f"**{title.strip()}**\n"
        md_output += f"{summary}...\n\n"

    return md_output

# Function to perform an education-specific search using DuckDuckGo
def search_results(query):
    try:
        search = DuckDuckGoSearchResults()
        result = search.invoke(query)
        return format_search_results(result)
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")
        return "No relevant search results found."


if __name__ == "__main__":
    app.run(debug=True)
