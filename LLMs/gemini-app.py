import os
from dotenv import load_dotenv

# Import Google's Gemini Python SDK to interact with Gemini models through the Gemini API.
from google import genai

# Load variables from the .env file
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

