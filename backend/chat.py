import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import re


GROQ_API_KEY=os.getenv("GROQ_API_KEY")

# os.environ['GOOGLE_API_KEY']=GOOGLE_API_KEY

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
def chatAI(user_input):
    """
    Function to interact with the ChatGoogleGenerativeAI model.
    Accepts a query as input and returns the model's response.
    Handles any errors gracefully by returning the error type as a string.
    """
    try:
        # Initialize the AI model
        llm = ChatGroq(model_name="deepseek-r1-distill-llama-70b", temperature=0.4)
        
        # Define the prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an AI agent designed to help students understand various concepts asked by the user. "
                    "When a user asks about a concept, provide a general explanation in less than 100 words. "
                    "If a query falls beyond academics, politely direct the student to ask something related to academics. "
                    "Do not provide direct code; instead, suggest a method to solve the problem.",
                ),
                ("human", "{input}"),
            ]
        )
        
        # Combine the prompt and LLM into a chain
        chain = prompt | llm
        
        # Get the result from the model
        results = chain.invoke({"input": user_input})

        # Extract content after </think> using regex
        ai_response = results.content.strip()
        match = re.search(r"</think>\s*(.*)", ai_response, re.DOTALL)

        # Return only the content after </think>
        return match.group(1).strip() if match else ai_response  # If no <think>, return full response

    except Exception as e:
        return f"An error occurred: {type(e).__name__}"
