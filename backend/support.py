import os
import pickle
import re
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class SupportChat:
    def __init__(self):
        # Load or create FAISS vector store
        self.vector_store = self.load_or_create_faiss()
        self.groq_llm = ChatGroq(
            temperature=0.2, 
            model_name="deepseek-r1-distill-llama-70b", 
            api_key=GROQ_API_KEY
        )

    def load_or_create_faiss(self):
        if Path("support_faiss_index.pkl").exists():
            with open("support_faiss_index.pkl", "rb") as f:
                return pickle.load(f)
        
        print("Fetching data and creating FAISS index...")
        urls = ["https://docs.google.com/document/u/1/d/e/2PACX-1vQB7SYIXQPJr0-WcfekVVSt488MdlkNzRUPacbRh2QgOALXcinPybopWIFlY83tdr_mH1QtrhCIsFUq/pub"]
        docs = WebBaseLoader(urls).load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(docs)
        texts = [doc.page_content for doc in split_docs]

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        faiss_index = FAISS.from_texts(texts, embeddings)

        with open("support_faiss_index.pkl", "wb") as f:
            pickle.dump(faiss_index, f)

        return faiss_index
     

    def chat(self, user_input):
        relevant_docs = self.vector_store.similarity_search(user_input, k=3)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"Context: {context}\n\nQuestion: {user_input}\n\nAnswer:"
        response= self.groq_llm.invoke(prompt).content
        cleaned_response = re.sub(r"<think>.*?</think>\s*", "", response, flags=re.DOTALL).strip()
        return cleaned_response

# Example usage
if __name__ == "__main__":
    bot = SupportChat()
    print(bot.chat("How many courses are there in foundation level?"))