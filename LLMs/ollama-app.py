import ollama

prompt = "WHat is the currency of Japan?"

response = ollama.chat(
    model="mistral",
    messages=[{"role": "user", "content": prompt}]
)

print(f"Response: {response}")
print(response["message"]["content"])