from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-base")

def rerank(query, docs, top_k=3):
    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)

    scored = list(zip(docs, scores))
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked[:top_k]]