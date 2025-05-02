from flask import Flask, request, jsonify
import os
import sys
from flask_cors import CORS
sys.path.append(os.path.join(os.path.dirname(__file__), 'gemini_qa'))
from gemini_qa_infer import load_data, gemini_answer

data_path = os.path.join(os.path.dirname(__file__), 'gemini_qa', 'prepared_documents.json')
texts, filenames = load_data(data_path)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('message', '')
    if not question:
        return jsonify({'error': 'No message provided'}), 400
    context = texts[0] if texts else ""
    answer = gemini_answer(question, context)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)