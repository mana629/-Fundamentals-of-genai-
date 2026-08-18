import warnings
warnings.filterwarnings('ignore')

from llm_client import get_llm_response

print("--- stateless chat bot (no memory)---")
print("Type 'quit' to exit")
 
#messages = []

chat_histroy = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    chat_histroy.append({'role':'user','content':user_input})

    #messages = [{'role':'user','content':user_input}]

    response=get_llm_response(chat_histroy)

    print(f"bot: {response}")
