import json
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


load_dotenv()

# :str — a type hint suggesting that config_path should be a string.
# = "config.json" — the default value. If you don't provide a path, it uses "config.json".
# -> dict — a return type hint indicating that the function is expected to return a dictionary.
def load_config(config_path:str = "config.json") -> dict:
    with open(config_path, "r") as file:

        # json.load(file) reads the JSON data from the opened file and converts it into Python objects.
        return json.load(file)


def get_llm():
    config = load_config()
    provider = config["provider"].lower()

    # configure client for the provider
    if provider == "openai":
        return ChatOpenAI(
            model=config["openai"]["model"],
            temperature=config["openai"]["temperature"],
            max_tokens=config["openai"]["max_tokens"],
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=config["gemini"]["model"],
            temperature=config["gemini"]["temperature"],
            max_tokens=config["gemini"]["max_tokens"],
            api_key=os.getenv("GEMINI_API_KEY"),
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")



# Temperature ??

# Low temperature (0.1) — predictable
# More consistent, focused answers. Good for coding, factual questions, and structured tasks.
# The model strongly favors the highest-probability tokens.

# Medium temperature (0.7) — balanced
# A balance between predictable answers and variety. Useful for general chatbots.
# Alternative tokens have a greater chance of being selected.

# Higher temperature (1.0) — more varied
# Can produce more diverse and creative responses, but may be less consistent.
# The distribution is flatter, so less likely tokens become more competitive.

# temperature doesn't directly tell the model which answer to give. It changes the probability distribution from which the next token is selected.