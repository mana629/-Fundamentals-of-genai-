import os
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

def get_llm_response(messages):
    provider = os.getenv('PROVIDER', 'google').lower()
    
    if provider == 'google':
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment or .env file.")
            
        model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        
        # Build prompt from messages
        prompt = ""
        for m in messages:
            role = m.get('role', 'user')
            content = m.get('content', '')
            prompt += f"{role}: {content}\n"
            
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text

    elif provider == 'openai':
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment or .env file.")
            
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content
    else:
        raise ValueError(f"Invalid provider: '{provider}'. Supported providers are 'google' and 'openai'.")

