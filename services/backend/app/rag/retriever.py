import os
import yaml
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

from .data_loader import load_documents

#BASE_DIR = Path(__file__).resolve().parents[4]
BASE_DIR = Path(__file__).resolve().parents[2]
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(current_dir), "config", "chroma.yaml")
project_root = os.path.dirname(os.path.dirname(current_dir))

with open(config_path, "r", encoding="utf-8") as f:
    chroma_config = yaml.safe_load(f)

class RetrieveService():
    def __init__(self):
        self.persist_dir = os.path.join(project_root, chroma_config['persist_directory'])
        data_path = BASE_DIR / "data" / "chunked_data.json"
        self.documents, _ = load_documents(data_path)

        embed_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en",
            encode_kwargs={'normalize_embeddings': True}
        )

        self.chroma = Chroma(
            collection_name=chroma_config['collection_name'],
            embedding_function=embed_model,
            persist_directory=self.persist_dir,
            collection_metadata={"hnsw:space": "cosine"},
        )

    def get_retriever(self):
        # vector retriever
        vector_retriever = self.chroma.as_retriever(search_kwargs={"k": 5})

        # BM25 retriever
        bm25_retriever = BM25Retriever.from_documents(self.documents)
        bm25_retriever.k = 5

        # Hybrid
        hybrid = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[0.5, 0.5]
        )

        return hybrid

if __name__=='__main__':
    retriever = RetrieveService().get_retriever()
    res = retriever.invoke("What is east asian cuisine?")
    for d in res:
        print(d.page_content)
        print(d.metadata)
        print("-" * 70)