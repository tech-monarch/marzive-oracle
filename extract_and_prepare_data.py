import os
import docx
import glob
import json

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_all_documents(documents_folder):
    data = []
    for file_path in glob.glob(os.path.join(documents_folder, '*.docx')):
        text = extract_text_from_docx(file_path)
        data.append({
            'filename': os.path.basename(file_path),
            'content': text
        })
    return data

def save_to_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    documents_folder = os.path.join(os.path.dirname(__file__), 'documents')
    output_path = os.path.join(os.path.dirname(__file__), 'prepared_documents.json')
    data = extract_all_documents(documents_folder)
    save_to_json(data, output_path)
    print(f"Extracted and saved {len(data)} documents to {output_path}")