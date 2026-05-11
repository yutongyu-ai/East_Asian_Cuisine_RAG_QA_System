import os
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
os.environ["CHROMA_TELEMETRY_IMPLEMENTATION"] = "noop"
os.environ["POSTHOG_DISABLED"] = "1"
import yaml
import shutil

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from .data_loader import load_documents


current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.dirname(current_dir), "config", "chroma.yaml")
project_root = os.path.dirname(os.path.dirname(current_dir))

with open(config_path, "r", encoding="utf-8") as f:
    chroma_config = yaml.safe_load(f)


class EmbeddingService:
    def __init__(self,):
        self.persist_dir = os.path.join(project_root, chroma_config['persist_directory'])
        os.makedirs(self.persist_dir, exist_ok=True)
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

    def upload_data(self, file, batch_size=500):

        documents, ids = load_documents(file)

        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]

            self.chroma.add_documents(
                documents=batch_docs,
                ids=batch_ids
            )

        print("saved to chroma database")

if __name__ == "__main__":
    data_path = os.path.join(project_root, "data", "chunked_data.json")
    persist_dir = os.path.join(project_root, chroma_config["persist_directory"])
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    service = EmbeddingService()
    service.upload_data(data_path)

