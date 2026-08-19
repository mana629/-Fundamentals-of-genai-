from datetime import datetime

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
