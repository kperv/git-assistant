from tqdm import tqdm
import pandas as pd
from elasticsearch import Elasticsearch

class DocumentsRetriver:
    elastic_url: str = 'http://localhost:9200'
    index_name: str = "pro-git-book"

    def __init__(self, num_docs: int = 2):
        self.num_docs = num_docs
        self.es_client = Elasticsearch(self.elastic_url)
        book = pd.read_csv('book.csv')
        self.documents = book.to_dict(orient='records')
        self.index_documents()

    def index_documents(self):
        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "chapter": {"type": "keyword"} 
                }
            }
        }
        self.es_client.indices.delete(index=self.index_name, ignore_unavailable=True)
        self.es_client.indices.create(index=self.index_name, body=index_settings)
        for doc in tqdm(self.documents):
            self.es_client.index(index=self.index_name, document=doc)

    def find_documents(self, query: str):
        relevant_documents = []
        if not self.is_valid_query(query):
            return relevant_documents
        else:
            search_query = {
                "size": self.num_docs,
                "query": {
                    "bool": {
                        "must": {
                            "multi_match": {
                                "query": query,
                                "fields": ["text", "chapter"],
                                "type": "best_fields"
                            }
                        },
                    }
                }
            }
            response = self.es_client.search(index=self.index_name, body=search_query)
            relevant_documents = [item['_source']['text'] for item in response['hits']['hits']]
            return relevant_documents

    def is_valid_query(self, query: str):
        return True if (query and query.isalpha()) else False


def main():
    retriever = DocumentsRetriver()
    # retriever.index_documenets()
    query = "How to commit a file?"
    relevant_texts = retriever.find_documents(query)
    for text in relevant_texts:
        print(text)


if __name__ == '__main__':
    main()