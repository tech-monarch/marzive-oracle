import os
import json
import google.generativeai as genai

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texts = [item['content'] for item in data]
    filenames = [item['filename'] for item in data]
    return texts, filenames

def gemini_answer(question, context, api_key=None, model=None):
    """
    Calls the Gemini API to get an answer for the question given the context using the official Google Generative AI SDK.
    Tries all available models until one works.
    Returns concise, focused answers optimized for brevity.
    """
    api_key = api_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "Gemini API key not found. Please set the GEMINI_API_KEY environment variable."
    genai.configure(api_key=api_key)
    try:
        models = genai.list_models()
        model_names = [m.name for m in models if hasattr(m, 'supported_generation_methods') and 'generateContent' in getattr(m, 'supported_generation_methods', [])]
        if not model_names:
            return "No available Gemini models support content generation."
        prompt = f"""Context: {context}

Question: {question}

Instructions:
- Respond as Marzive Oracle
- Keep your answer extremely concise (max 2-3 sentences)
- Focus only on directly answering the question
- If you don't know, simply state it's beyond your knowledge
- Avoid unnecessary explanations or context repetition
- Be precise and informative despite brevity

Answer:"""
        for model_name in model_names:
            try:
                model_obj = genai.GenerativeModel(model_name)
                response = model_obj.generate_content(prompt)
                if hasattr(response, "text") and response.text.strip():
                    # Post-process to ensure brevity
                    answer = response.text.strip()
                    # Remove any lengthy preambles like "Based on the context..."
                    if len(answer.split()) > 60:  # If answer is too long
                        sentences = answer.split('.')
                        # Keep only first 2-3 meaningful sentences
                        filtered = [s for s in sentences if len(s.strip()) > 10][:3]
                        answer = '.'.join(filtered) + ('.' if not filtered[-1].endswith('.') else '')
                    return answer
            except Exception as e:
                continue
        return "All available Gemini models failed to generate a response."
    except Exception as e:
        return f"Error occurred while connecting to Gemini API: {e}"

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), 'prepared_documents.json')
    texts, filenames = load_data(data_path)
    print(f"Loaded {len(texts)} documents.")
    example_question = "What is the Marzive DAO?"
    context = texts[0] if texts else ""
    answer = gemini_answer(example_question, context)
    print(f"Gemini Answer: {answer}")
