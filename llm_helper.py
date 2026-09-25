from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

print("API KEY LOADED:", bool(os.getenv("GROQ_API_KEY")))
llm = ChatGroq(groq_api_key = os.getenv("GROQ_API_KEY"), model_name="qwen/qwen3.8-27b")

if __name__ == "__main__":
    response = llm.invoke("what are the two main ingredients in Samosa?")
    print(response.content)