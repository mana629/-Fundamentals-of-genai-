from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

from llm_client import get_llm_response

def calculator(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(city: str) -> str:
    """Returns weather information for a given city."""
    return f"The current weather in {city} is sunny and 25°C."

def get_current_time(city: str = "") -> str:
    """Returns current time."""
    return datetime.now().strftime("%H:%M:%S")

# tools 
TOOLS = {
    "calculator": calculator,
    "get_weather": get_weather,
    "get_current_time": get_current_time
}

SYSTEM_PROMPT = """
You are a helpful assistant that can answer questions and perform calculations. You have access to the following tools: 
calculator - use it when you need to calculate something
get_weather - use it when you need to get the weather of a city
get_current_time - use it when you need to get the current time

Return your tool call strictly as a JSON object formatted like:
{
  "tool": "tool_name",
  "input": "tool_input"
}

If no tool is needed, respond normally.
"""

if __name__ == "__main__":
    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_input}
        ]

        response = get_llm_response(messages)
        
        try:
            clean = response.strip()
            if clean.startswith("```json"):
                clean = clean[7:-3].strip()
            elif clean.startswith("```"):
                clean = clean[3:-3].strip()
            
            data = json.loads(clean)
            tool = data.get("tool")
            tool_input = data.get("input", "")

            if tool in TOOLS:
                print(f"\nusing tool : {tool}")
                result = TOOLS[tool](tool_input) if tool_input else TOOLS[tool]()
                print(f"bot (tool output): {result}")
            else:
                print(f"bot: {response}")
        except Exception:
            print(f"bot: {response}")