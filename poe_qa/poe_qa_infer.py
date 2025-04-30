import os
import json
import requests

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texts = [item['content'] for item in data]
    filenames = [item['filename'] for item in data]
    return texts, filenames

def gemini_answer(question, context, api_key=None, model="gemini-pro"):
    """
    Calls the Gemini API to get an answer for the question given the context.
    """
    api_key = api_key or os.getenv('GEMINI_API_KEY', 'AIzaSyD36Nh-h8eSiZQhuwHUH2xb-ydHWV1-PDo')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
    except requests.exceptions.SSLError as ssl_err:
        return f"SSL error occurred while connecting to Gemini API: {ssl_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred while connecting to Gemini API: {conn_err}"
    except Exception as e:
        return f"Unexpected error occurred while connecting to Gemini API: {e}"
    if response.status_code == 200:
        try:
            candidates = response.json().get('candidates', [])
            if candidates and 'content' in candidates[0]:
                parts = candidates[0]['content'].get('parts', [])
                if parts and 'text' in parts[0]:
                    return parts[0]['text'].strip()
            return f"Gemini API response error: {response.text}"
        except Exception:
            return f"Gemini API response error: {response.text}"
    else:
        try:
            error_detail = response.json().get('error', response.text)
        except Exception:
            error_detail = response.text
        return f"Gemini API error ({response.status_code}): {error_detail}\nPlease check the Gemini API endpoint or your network connection."

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), 'prepared_documents.json')
    texts, filenames = load_data(data_path)
    print(f"Loaded {len(texts)} documents.")
    example_question = "What is the Marzive DAO?"
    context = texts[0] if texts else ""
    answer = gemini_answer(example_question, context)
    print(f"Gemini Answer: {answer}")