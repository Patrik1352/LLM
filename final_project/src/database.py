import json
import numpy as np
import faiss
import os
from openai import OpenAI
from typing import List, Dict, Optional


class VectorDatabase:
    def __init__(self, api_key, model: str = "text-embedding-3-small"):
        self.documents: List[Dict] = []
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = model
        self.index: Optional[faiss.Index] = None
        self.dimension = 1536  # Для text-embedding-3-small

    def _get_embedding(self, text: str) -> np.ndarray:
        """Получение эмбеддинга через OpenAI API"""
        response = self.client.embeddings.create(
            input=[text],
            model=self.embedding_model
        )
        return np.array(response.data[0].embedding, dtype='float32')

    def add_document(self, document: Dict):
        """Добавление документа в базу"""
        self.documents.append(document)
        embedding = self._get_embedding(document["summarization"])
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(np.array([embedding]))
        else:
            self.index.add(np.array([embedding]))

    def add_documents_batch(self, documents: List[Dict]):
        """Пакетное добавление документов"""
        summaries = [doc["summarization"] for doc in documents]
        embeddings = [self._get_embedding(text) for text in summaries]
        
        self.documents.extend(documents)
        embeddings_array = np.array(embeddings, dtype='float32')
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings_array)

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Поиск по сумммаризации с возвратом полных документов"""
        query_embed = self._get_embedding(query)
        distances, indices = self.index.search(np.array([query_embed]), k)
        
        return [self.documents[i] for i in indices[0] if i < len(self.documents)]

    def save(self, path: str):
        """Сохранение базы на диск"""
        os.makedirs(path, exist_ok=True)
        
        with open(os.path.join(path, "documents.json"), "w", encoding="utf-8") as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        
        if self.index is not None:
            faiss.write_index(self.index, os.path.join(path, "index.faiss"))

    def load(self, path: str):
        """Загрузка базы с диска"""
        with open(os.path.join(path, "documents.json"), "r", encoding="utf-8") as f:
            self.documents = json.load(f)
        
        index_path = os.path.join(path, "index.faiss")
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)