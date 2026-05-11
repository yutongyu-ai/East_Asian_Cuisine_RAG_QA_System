import json
from langchain_core.documents import Document

def load_documents(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    ids = []

    for item in data:
        documents.append(
            Document(
                page_content=item["text"],
                metadata={
                    "chunk_id": item["chunk_id"],
                    "parent_doc_id": item["parent_doc_id"],
                    "source": item["source"],
                }
            )
        )
        ids.append(item["chunk_id"])

    return documents, ids