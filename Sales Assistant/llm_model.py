import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def generate_llm_response(prompt):
    """
    Sends a prompt to the Together AI endpoint using Meta-LLaMA 3 and returns the response.

    Parameters:
        prompt (str): The input user prompt.

    Returns:
        str: The LLM's response or an error message.
    """
    url = "https://api.together.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  
        data = response.json()

    
        if "choices" in data and isinstance(data["choices"], list) and len(data["choices"]) > 0:
            message = data["choices"][0].get("message", {})
            content = message.get("content", "").strip()

            if content:
                return content
            else:
                return " LLM response had no content."
        else:
            print(" Malformed LLM response:", data)
            return " LLM response was empty or malformed."

    except requests.exceptions.RequestException as e:
        print(" Network/API Error:", str(e))
        return " Failed to contact LLM service."

    except (KeyError, IndexError) as e:
        print(" Parsing Error:", str(e))
        print(" Full response:", response.text)
        return " Unexpected format in LLM response."

