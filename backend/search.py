from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import GoogleSerperAPIWrapper
import re
import os
from dotenv import load_dotenv
load_dotenv()

# SERPER_API_KEY=os.getenv("SERPER_API_KEY")
SERPER_API_KEY= "dd017ef332d8912e858162e7a36d0377cd97e8ca"


CS_KEYWORDS = {
    "machine learning", "deep learning", "artificial intelligence", "AI",
    "neural networks", "NLP", "computer vision", "data science",
    "cloud computing", "software engineering", "big data",
    "blockchain", "cybersecurity", "quantum computing",
    "algorithm", "data structures", "distributed systems",
    "operating systems", "computer architecture", "IoT",
    "database systems", "web development", "API", "RESTful",
    "graph theory", "cryptography", "natural language processing",
    "cloud storage", "LLM", "transformers", "GANs",
    "backpropagation", "reinforcement learning", "compiler design","algorithm", "complexity", "big_o", 
    "pseudocode", "flowchart", "efficiency", "optimization", 
    "procedure", "steps", "process", "logic", "solution", "problem_solving", "divide_conquer", "greedy",
     "recursive", "iteration", "sequence","algorithm", "pseudocode", "time complexity", "space complexity",
    "asymptotic notations", "recursion", "divide and conquer", "greedy algorithm",
    "dynamic programming", "backtracking", "if", "else", "elif",
    "boolean logic", "logical operators", "comparison operators",
    "ternary operator", "match-case", "truthy", "falsy", "guard clauses",
    "for loop", "while loop", "range", "loop control statements",
    "iterators", "generators", "list comprehension", "enumerate", "zip",
    "map", "filter", "list", "tuple", "set", "dictionary",
    "defaultdict", "OrderedDict", "nested data structures",
    "Counter", "sorting", "stacks", "queues", "priority queues",
    "heapq", "file handling", "open", "read", "write", "close",
    "with open", "CSV", "JSON", "os module", "file exception handling",
    "import", "built-in modules", "third-party modules", "custom modules",
    "virtual environments", "pip", "NumPy", "ndarray", "np.array",
    "np.zeros", "np.ones", "np.linspace", "array indexing",
    "array slicing", "mathematical operations", "broadcasting",
    "reshaping", "flattening", "random number generation",
    "pandas", "DataFrame", "Series", "pd.read_csv", "pd.to_csv",
    "df.head", "df.tail", "df.info", "df.describe", "df['column']",
    "filtering data", "handling missing data", "groupby", "aggregation",
    "merging DataFrames", "joining DataFrames",
     # General Computer Science
    "algorithm", "pseudocode", "time complexity", "space complexity",
    "asymptotic notations", "recursion", "divide and conquer", "greedy algorithm",
    "dynamic programming", "backtracking", "graph algorithms", "sorting",
    "binary search", "hashing", "data structures", "linked list", "stack",
    "queue", "priority queue", "heap", "tree", "binary tree", "BST", "trie",
    "graph", "BFS", "DFS", "shortest path", "Dijkstra", "Bellman-Ford", "Floyd-Warshall",
    "database", "SQL", "NoSQL", "ACID properties", "CAP theorem", "normalization",
    "operating system", "process scheduling", "memory management", "virtual memory",
    "distributed systems", "cloud computing", "serverless computing", "microservices",
    "blockchain", "cryptography", "hash functions", "zero-knowledge proofs",
    "cybersecurity", "authentication", "authorization", "firewall", "penetration testing",
    "web development", "API", "RESTful", "GraphQL", "frontend", "backend", "full stack",

    # Machine Learning (ML)
    "machine learning", "supervised learning", "unsupervised learning",
    "semi-supervised learning", "reinforcement learning", "self-supervised learning",
    "classification", "regression", "clustering", "anomaly detection",
    "ensemble learning", "bagging", "boosting", "stacking",
    "decision tree", "random forest", "gradient boosting", "XGBoost", "LightGBM",
    "SVM", "support vector machine", "logistic regression", "linear regression",
    "KNN", "k-nearest neighbors", "naive bayes", "PCA", "dimensionality reduction",
    "feature engineering", "feature selection", "hyperparameter tuning",
    "cross-validation", "overfitting", "underfitting", "bias-variance tradeoff",
    "model evaluation", "confusion matrix", "precision", "recall", "F1-score",
    "AUC-ROC", "RMSE", "MSE", "MAE", "regularization", "L1", "L2", "dropout",

    # Deep Learning (DL)
    "deep learning", "neural networks", "feedforward network", "backpropagation",
    "activation function", "ReLU", "sigmoid", "softmax", "tanh",
    "gradient descent", "stochastic gradient descent", "SGD", "Adam optimizer",
    "batch normalization", "dropout regularization", "convolutional neural network",
    "CNN", "image processing", "ResNet", "VGG", "EfficientNet", "Inception",
    "transformers", "self-attention", "multi-head attention", "BERT", "GPT",
    "LLM", "large language model", "fine-tuning", "transfer learning",
    "sequence-to-sequence", "RNN", "LSTM", "GRU", "encoder-decoder", "attention mechanism",
    "word embeddings", "word2vec", "GloVe", "fastText",

    # Generative AI (GenAI)
    "generative AI", "GAN", "generative adversarial network", "diffusion model",
    "Stable Diffusion", "DALL·E", "image synthesis", "text-to-image",
    "text generation", "style transfer", "autoencoder", "VAE", "variational autoencoder",
    "latent space", "sampling", "stochastic processes",

    # Large Language Models (LLMs)
    "LLM", "GPT-3", "GPT-4", "GPT-4 Turbo", "Claude", "Mistral", "Gemini",
    "open-weight models", "model inference", "prompt engineering", "chain-of-thought",
    "temperature", "top-k sampling", "top-p nucleus sampling", "zero-shot learning",
    "few-shot learning", "instruction tuning", "RLHF", "human feedback",
    "alignment problem", "tokenization", "bpe", "byte pair encoding",
    "context window", "self-supervised learning", "transformer architecture",

    # Agentic AI
    "agentic AI", "autonomous agents", "multi-agent systems", "AI reasoning",
    "memory-enabled AI", "retrieval-augmented generation", "RAG",
    "vector search", "knowledge graphs", "AI planning", "decision making",
    "LLM agents", "AutoGPT", "BabyAGI", "LangChain", "AI workflows",
    "reflection", "self-improvement", "self-learning AI",

    # AI Safety & Ethics
    "AI alignment", "AI safety", "AI bias", "explainability", "XAI",
    "ethical AI", "fairness in AI", "model interpretability", "adversarial attacks",
    "robustness", "hallucinations in AI", "trustworthy AI",

    # Tools & Libraries
    "TensorFlow", "PyTorch", "Keras", "Hugging Face", "Transformers library",
    "sklearn", "scikit-learn", "OpenAI API", "LangChain", "ChromaDB",
    "FAISS", "Weaviate", "Pinecone", "vector embeddings", "text embeddings",
    "fast.ai", "Matplotlib", "Seaborn", "Plotly", "pandas", "NumPy"
}

def is_computer_science_related(query):
    """
    Checks if the query is related to Computer Science by matching keywords.
    """
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in CS_KEYWORDS)

def string_to_md(result):
    """
    Converts search results into Markdown format.
    """
    md_output = "## **Search Results**\n\n"

    # Check if results exist
    if "organic" not in result or not result["organic"]:
        return "No relevant results found."

    # Iterate through search results
    for entry in result["organic"]:
        title = entry.get("title", "No title")
        link = entry.get("link", "#")
        snippet = entry.get("snippet", "No snippet available.")
        
        md_output += f"### **[{title}]({link})**\n"
        md_output += f"*Snippet*: {snippet}\n\n"

    return md_output

def SearchResults(query):
    """
    Takes a query as input, checks if it's related to Computer Science, 
    performs a Google Serper search (if relevant), and returns the results in Markdown format.
    """
    if not is_computer_science_related(query):
        return "❌ **Not relevant to the course.**"

    if not SERPER_API_KEY:
        return "Error: SERPER_API_KEY is not set. Please configure your API key in the .env file."

    # Initialize Google Serper search tool
    search = GoogleSerperAPIWrapper(api_key=SERPER_API_KEY, gl="us", hl="en", type="search")

    try:
        # Perform the search
        result = search.results(query)

        # Convert the result to Markdown
        md_results = string_to_md(result)
        return md_results
    except Exception as e:
        return f"Error: {e}"
