import json
from llm_client import get_llm_response
from datetime import datetime

print("===== Tool-enabled Chatbot =====")
print("Type 'exit' to quit\n")

# Step1: Define Tools

def calculator(expression):
    try:
        # Evaluate the mathematical expression and convert the result to a string.
        return str(eval(expression))
    except:
        return "Invalid calculation"
    
def get_weather(city):
    return f"The weather in {city} is 16 degrees and sunny."

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Tool Registry
# This dictionary connects each tool's name to its Python function.
# The LLM provides the tool name, and our program finds the matching function.
TOOLS = {
    "calculator": calculator,
    "weather": get_weather,
    "time": get_current_time
}

# Step2: System Prompt
# Tell the LLM which tools are available and how to request a tool.
SYSTEM_PROMPT = """
You are an AI assistant with access to tools.

Available tools:
1. calculator -> for math expressions
2. weather -> for city weather
3. time -> for current time

When a tool is needed, response ONLY in this JSON format:

{
  "tool": "tool_name",
  "input": "input_for_tool"
}

If no tool is needed, response normally.
"""

# Step3: Chat Loop
# Keep accepting user messages until the user types "exit".
while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        break

    message = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    response = get_llm_response(message)
    print(f"\nRaw Response: {response}")

    try:
        # Convert the LLM's JSON response into a Python dictionary.
        data = json.loads(response)

        # Extract the requested tool name and its input.
        tool = data["tool"]
        tool_input = data.get("input", "")

        if tool in TOOLS:
            print(f"\nUsing tool: {tool}")

            # Find the requested Python function.
            selected_tool = TOOLS[tool]

            # If the tool needs input, pass the input to the function.
            # Otherwise, call the function without any arguments.
            if tool_input:
                result = selected_tool(tool_input)
            else:
                result = selected_tool()

            # Display the result returned by the tool.
            print(f"Tool output: {result}")

            # Ask LLM to generate final answer
            final = get_llm_response([
                {"role": "user", "content": f"User asked: {user_input}\n Tool result: {result}"}
            ])

            print(f"Bot's Final Answer (using tools): {final}")
        else:
            print(f"Bot's Final Answer: {response}")
    except:
        print(f"Bot's Final Answer: {response}")