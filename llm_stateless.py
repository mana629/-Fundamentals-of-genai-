import warnings
warnings.filterwarnings('ignore')

from llm_client import get_llm_response

print("--- stateless chat bot (memory)---")
print("Type 'quit' to exit")
 
messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    messages = [{'role':'user','content':user_input}]

    response=get_llm_response(messages)

    print(f"bot: {response}")
 
    