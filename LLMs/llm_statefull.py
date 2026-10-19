from llm_client import get_llm_response

print("--- Stateful Chatbot (With Memory)")
print("Type 'exit' to quit\n")


chat_history = []

MAX_TURNS = 5

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    # Keep the latest 5 exchanges (10 messages)
    recent_history = chat_history[-(MAX_TURNS * 2):]

    response = get_llm_response(recent_history)
    print(f"Bot: {response}")

    chat_history.append({
        "role": "assistant",
        "content": response
    })