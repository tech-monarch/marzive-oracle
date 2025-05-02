import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gemini_qa'))
from gemini_qa_infer import load_data, gemini_answer

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"})
        }
    try:
        body = request.body.decode() if hasattr(request.body, 'decode') else request.body
        data = json.loads(body)
        question = data.get('message', '')
        if not question:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "No message provided"})
            }
        data_path = os.path.join(os.path.dirname(__file__), '..', 'gemini_qa', 'prepared_documents.json')
        texts, filenames = load_data(data_path)
        context = texts[0] if texts else ""
        answer = gemini_answer(question, context)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"answer": answer})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }