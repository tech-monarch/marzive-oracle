# Marzive Oracle

Marzive Oracle is a question-answering system powered by Google's Gemini AI. It provides concise, focused answers to questions about Marzive DAO and related documents.

## Project Structure

```
├── api/                    # Serverless backend functions (e.g., for Vercel)
│   └── chat.py             # /api/chat endpoint implementation
├── extract_and_prepare_data.py  # Data preparation script
├── documents/               # Source documents
├── frontend/               # Web interface
│   ├── index.html          # Frontend HTML
│   └── style.css           # Frontend styling
└── gemini_qa/              # Gemini QA module
    ├── gemini_qa_infer.py  # Inference module
    └── prepared_documents.json  # Processed document data
```

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Web browser

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tech-monarch/marzive-oracle.git
   cd marzive-oracle
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install packages individually:
   ```bash
   pip install flask flask-cors google-generativeai python-docx
   ```

3. Set up your Gemini API key as an environment variable:
   ```bash
   # On Windows
   set GEMINI_API_KEY=AIzaSyDkRIq5E7EJOVQ_g_uWzn5aP7-KUeAYI-o
   
   # On macOS/Linux
   export GEMINI_API_KEY=AIzaSyDkRIq5E7EJOVQ_g_uWzn5aP7-KUeAYI-o
   ```

   Alternatively, you can provide the API key directly when calling the `gemini_answer` function.

## Usage

### Data Preparation

If you have new documents to process:

1. Place your .docx files in the `documents` folder
2. Run the extraction script:
   ```bash
   python extract_and_prepare_data.py
   ```
   This will extract text from all .docx files and save it to `prepared_documents.json`

### Backend API (Serverless Function)
The backend is designed to run as a serverless function under the `api` directory (e.g., for Vercel deployment). There is no need to run a Flask server locally.

**To test the backend locally, you must use the Vercel development server:**

1. Install Vercel CLI if you haven't:
   ```bash
   npm install -g vercel
   ```
2. Run the local development server from the project root:
   ```bash
   vercel dev
   ```
3. The API will be available at `/api/chat`.

- For production, deploy the project to Vercel and the backend will be served as a serverless function automatically.

### Running the Frontend

1. Start a simple HTTP server in the frontend directory:
   ```bash
   cd frontend
   python -m http.server 8000
   ```

2. Open your browser and navigate to `http://localhost:8000`.

3. You can now ask questions through the web interface.

### Using the Gemini QA Module Directly

You can also use the Gemini QA module directly in your Python code:
 
```python
from gemini_qa.gemini_qa_infer import gemini_answer

question = "What is the Marzive DAO?"
context = "Your context text here..."
api_key = "AIzaSyDkRIq5E7EJOVQ_g_uWzn5aP7-KUeAYI-o"  # Optional if set as environment variable

answer = gemini_answer(question, context, api_key)
print(answer)
```

## Security Notes

- **Never commit API keys to your repository**. Always use environment variables or secure configuration methods.
- If you accidentally commit sensitive information, follow GitHub's guide on [removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

## Troubleshooting

- If you encounter a "Gemini API key not found" error, ensure you've set the `GEMINI_API_KEY` environment variable correctly.
- If the frontend cannot connect to the API, ensure the serverless function is deployed and accessible at `/api/chat`.
- If using Vercel locally, make sure `vercel dev` is running from the project root and you are accessing the correct local URL.

## License

MIT
=======
# marzive-oracle
>>>>>>> origin/main
=======
>>>>>>> origin/main
