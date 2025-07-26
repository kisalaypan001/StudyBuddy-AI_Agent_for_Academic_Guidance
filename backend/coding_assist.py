import os
from groq import Groq
from dotenv import load_dotenv
from typing import Dict
import re

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



def programming_assist(problem_statement: str, error_code: str) -> str:
    """
    Assist with code error analysis by providing insights and solutions.
    
    Args:
        problem_statement (str): The context or question about the code's purpose.
        error_code (str): The error message or traceback.
    
    Returns:
        str: A formatted analysis report with root causes, solutions, and best practices.
    """
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is not set. Please configure it in your environment variables."

    try:
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        model = "deepseek-r1-distill-llama-70b"
        
        # Construct the prompt
        prompt = f"""Analyze this coding attempt and provide structured guidance:

Context of what the code was trying to do:
{problem_statement}

Error Code:
{error_code}

Provide analysis covering:
1. Error categorization and common causes
2. Step-by-step debugging strategy (no direct code)
3. Prevention best practices
4. Related programming concepts to review

Format your response as a structured analysis focused on understanding and learning.
"""

        # Call the Groq API
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You're a senior developer mentoring programming students. Provide conceptual guidance focused on fundamental understanding."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        # Extract the response content
        response = completion.choices[0].message.content
        
        # Remove AI reasoning within <think> tags
        cleaned_response = re.sub(r"<think>.*?</think>\s*", "", response, flags=re.DOTALL).strip()

        # Format the response into a report
        report = f"""
Code Error Analysis Report
========================

Context
-------
Problem Statement: {problem_statement}

Error Code
------------
{error_code}

Analysis
--------
{cleaned_response}
"""
        return report

    except Exception as e:
        return f"Error occurred: {str(e)}\nSuggestion: Please check your API key, input data, and network connection."
