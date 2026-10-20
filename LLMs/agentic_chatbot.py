import json
from llm_client import get_llm_response
import random


print("===== Multi-Tool AI Agent =====")
print("Type 'exit' to quit\n")


# Tools
def get_weather(city):
    weather_opt = [f"The weather in {city} is 20 degrees and pleasent.", f"The weather in {city} is 16 degrees and raining.", f"The weather in {city} is 38 degrees and sunny."]
    return random.choice(weather_opt)
    
def suggest_activity(weather):
    if "raining" in weather.lower() or "sunny" in weather.lower():
        return "Stay indoors, do yoga or light streatching."
    else:
        return "Go for a run or outdoor walk."
    
    
def calorie_estimator(activity):
    if "yoga" in activity.lower():
        return "Estimated calories burned: 150 kcal"
    elif "run" in activity.lower():
        return "Estimated calories burned: 600 kcal"
    else:
        return "Estimated calories burned: 50 kcal"
    

TOOLS = {
    "weather": get_weather,
    "activity": suggest_activity,
    "calories": calorie_estimator
}


SYSTEM_PROMPT = """
You are an intelligent planning agent.

You must solve the user's problem step-by-step using tools.

Available Tools:
1. weather -> city weather
2. activity -> based on weather
3. calories -> based on activity

Rules:
- Think step-by-step
- Use tools when needed
- You can call multiple tools in sequence
- Use previous results to decide next step

Respond ONLY in JSON:

Step format:
{
  "tool": "tool_name",
  "input": "input"
}

Final format:
{
  "final_answer": "complete answer"
}
"""

# Agent Loop:
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # The context variable stores the information the agent will send to the LLM. Initially, it contains only the user's question.
    context = user_input

    # Keeps track of the agent's current step.
    step = 1

    while True:
        print(f"\n----- Step: {step} -----")

        message = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ]

        response = get_llm_response(message)
        print(f"\nAgent Decision: {response}")

        try:
            # It converts a JSON string into a Python dictionary.
            data = json.loads(response)

            if "final_answer" in data:
                print(f"\nFinal Plan:\n{data['final_answer']}\n")
                break

            # tool calling
            tool = data.get("tool")
            tool_input = data.get("input", "")

            if tool in TOOLS:
                print(f"Using tool: '{tool}', with input: '{tool_input}'")

                if tool_input:
                    result = TOOLS[tool](tool_input)
                else:
                    result = TOOLS[tool]()
                print(f"Observation via tool: {result}")

                # Why is this necessary?
                # Because on the next iteration, the LLM needs to know what happened in the previous step. Without the updated context, the LLM might see only the original question again and not know the weather tool's result. With the updated context, it can decide what to do next.
                context += f"\nResult of {tool}: {result}"
            else:
                print("Unknown tool!!\n\n")
                break

        except:
            print("Failed to parse response!!\n\n")
            break

        step += 1