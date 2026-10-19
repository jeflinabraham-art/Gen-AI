import os

from dotenv import load_dotenv
load_dotenv()

provider = "gemini"

def get_llm_response(message):
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=message
        )
        response.choices[0].message.content

    elif provider == "gemini":

        # Imports Google's Gen AI Python SDK. This is the SDK used to communicate with Google's Gemini models.
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        prompt = ""

        for m in message:
            role = m["role"]
            content = m['content']
            prompt += f"{role}: {content}\n"

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text
    else:
        raise ValueError("Invalid PROVIDER. Use 'openai' or 'gemini'")