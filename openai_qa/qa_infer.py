import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texts = [item['content'] for item in data]
    filenames = [item['filename'] for item in data]
    return texts, filenames

def build_tokenizer(texts, num_words=10000):
    tokenizer = Tokenizer(num_words=num_words, oov_token='<OOV>')
    tokenizer.fit_on_texts(texts)
    return tokenizer

def vectorize_texts(tokenizer, texts, maxlen=256):
    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(sequences, maxlen=maxlen, padding='post', truncating='post')
    return padded

def load_model(model_path):
    return tf.keras.models.load_model(model_path)

def retrieve_answer(model, tokenizer, texts, question, top_k=3):
    # Vectorize the question
    question_seq = tokenizer.texts_to_sequences([question])
    question_pad = pad_sequences(question_seq, maxlen=256, padding='post', truncating='post')
    # Get relevance scores for all texts
    doc_seqs = vectorize_texts(tokenizer, texts)
    preds = model.predict(doc_seqs, verbose=0)
    # Get top_k most relevant documents
    top_indices = np.argsort(preds.flatten())[::-1][:top_k]
    return [(texts[i], float(preds[i])) for i in top_indices]

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), 'prepared_documents.json')
    model_path = os.path.join(os.path.dirname(__file__), 'qa_retriever_model.h5')
    texts, filenames = load_data(data_path)
    tokenizer = build_tokenizer(texts)
    model = load_model(model_path)
    print("Model and data loaded. Enter your question (or 'exit' to quit):")
    while True:
        question = input("Q: ")
        if question.lower() in ['exit', 'quit']:
            break
        results = retrieve_answer(model, tokenizer, texts, question)
        print("Top relevant contexts:")
        for idx, (context, score) in enumerate(results):
            print(f"[{idx+1}] Score: {score:.4f}\nContext: {context[:300]}\n---")