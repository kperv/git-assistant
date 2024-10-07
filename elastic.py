import pandas as pd
from tqdm import tqdm
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer


class DocumentsRetriver:
    elastic_url: str = "http://localhost:9200"
    index_name: str = "pro-git-book"
    model_name: str = 'multi-qa-MiniLM-L6-cos-v1'
    model = SentenceTransformer(model_name)

    def __init__(self, book: pd.DataFrame, num_docs: int = 10):
        self.num_docs = num_docs
        self.es_client = Elasticsearch(self.elastic_url)
        self.documents = book.to_dict(orient="records")
        self.add_vectors()
        self.index_documents()

    def add_vectors(self):
        for doc in self.documents:
            doc['text_vector'] = self.model.encode(doc['text'])

    def index_documents(self):
        index_settings = {
            "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            "mappings": {
                "properties": {"text": {"type": "text"}, "chapter": {"type": "keyword"}, "section": {"type": "keyword"}, "text_vector": {"type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"}}
            },
        }
        self.es_client.indices.delete(index=self.index_name, ignore_unavailable=True)
        self.es_client.indices.create(index=self.index_name, body=index_settings)
        for doc in tqdm(self.documents):
            self.es_client.index(index=self.index_name, document=doc)

    def find_documents(self, query: str):
        relevant_documents = []
        if not self.is_valid_query(query):
            print("query is not valid")
            return relevant_documents
        else:   
            # vector
            v_q = self.model.encode(query)
            knn_query = {
                "field": "text_vector",
                "query_vector": v_q,
                "k": 5,
                "num_candidates": 10000,
                "boost": 0.5,
            }
            # text
            keyword_query = {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": ["text", "chapter", "section^3"],
                            "type": "best_fields",
                            "boost": 0.5,
                        }
                    },
                }
            }

            response = self.es_client.search(index=self.index_name, query=keyword_query, knn=knn_query, size=self.num_docs)
            print("*"*20)
            print(response)
            relevant_documents = [
                item["_source"] for item in response["hits"]["hits"]
            ]
            return relevant_documents

    def is_valid_query(self, query: str):
        return True if len(query) > 0 else False


def main():
    book_df = pd.read_csv('/ssd/ksu/projects/git-assistant/book.csv')
    retriever = DocumentsRetriver(book_df)
    # retriever.index_documenets()
    query = "How to commit a file?"
    relevant_texts = retriever.find_documents(query)
    for text in relevant_texts:
        print(text)


if __name__ == "__main__":
    main()
