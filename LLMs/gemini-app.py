# Imports Python's built-in os module, which allows you to interact with operating-system features, including environment variables.
import os

# This function reads variables from a .env file and loads them into your environment.
from dotenv import load_dotenv

# Import Google's Gemini Python SDK to interact with Gemini models through the Gemini API.
from google import genai

# Loads the variables from the .env file so Python can access them using os.getenv().
load_dotenv()

# Retrieve the API key
api_key = os.getenv("GEMINI_API_KEY")

# Create the client to communicate with the Gemini API
client = genai.Client(api_key=api_key)

# Define the input
prompt = "Give a beginner-friendly explanation of LLMs in under 200 words."

# Generate a response using the selected model
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

# Print input and output
print(f"User: {prompt}")
print(f"Model's Response: {response.text}")

