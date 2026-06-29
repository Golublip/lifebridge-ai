import os
import json
from typing import List, Dict, Any, Optional

class VectorMemory:
    """
    Manages vector memory using ChromaDB for semantic documents, reports, and conversation logs.
    Includes a lightweight, robust fallback implementation if ChromaDB fails to load on the local environment.
    """
    def __init__(self, collection_name: str = "lifebridge_records"):
        self.collection_name = collection_name
        self.chroma_client = None
        self.collection = None
        self.fallback_db = []  # Simple in-memory fallback: List[Dict[str, Any]]
        self.use_fallback = False
        
        # Determine path
        self.persist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db"))
        
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
            print("Successfully initialized ChromaDB collection.")
        except Exception as e:
            print(f"ChromaDB initialization failed: {e}. Falling back to in-memory semantic memory.")
            self.use_fallback = True
            self._load_fallback_db()

    def _load_fallback_db(self):
        fallback_file = os.path.join(self.persist_dir, "fallback_db.json")
        if os.path.exists(fallback_file):
            try:
                with open(fallback_file, "r") as f:
                    self.fallback_db = json.load(f)
            except Exception:
                self.fallback_db = []

    def _save_fallback_db(self):
        os.makedirs(self.persist_dir, exist_ok=True)
        fallback_file = os.path.join(self.persist_dir, "fallback_db.json")
        try:
            with open(fallback_file, "w") as f:
                json.dump(self.fallback_db, f, indent=2)
        except Exception as e:
            print(f"Failed to save fallback vector memory: {e}")

    def add_document(self, doc_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Adds a document/report to the vector store
        """
        if metadata is None:
            metadata = {}
            
        if not self.use_fallback and self.collection:
            try:
                self.collection.add(
                    documents=[content],
                    ids=[doc_id],
                    metadatas=[metadata]
                )
                return
            except Exception as e:
                print(f"Error writing to ChromaDB: {e}. Writing to fallback db.")
                
        # Fallback approach
        # Check if already exists, update it
        for doc in self.fallback_db:
            if doc['id'] == doc_id:
                doc['content'] = content
                doc['metadata'] = metadata
                self._save_fallback_db()
                return
        
        self.fallback_db.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata
        })
        self._save_fallback_db()

    def search(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Searches matching health records or conversations.
        If using fallback, performs a basic word-overlap/keyword search.
        """
        if not self.use_fallback and self.collection:
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=limit
                )
                output = []
                if results and 'documents' in results and results['documents']:
                    docs = results['documents'][0]
                    ids = results['ids'][0]
                    metadatas = results['metadatas'][0] if 'metadatas' in results else [{}]*len(docs)
                    for i in range(len(docs)):
                        output.append({
                            "id": ids[i],
                            "content": docs[i],
                            "metadata": metadatas[i] or {}
                        })
                return output
            except Exception as e:
                print(f"Error querying ChromaDB: {e}. Querying fallback db.")

        # Fallback keyword overlap search
        query_words = set(query.lower().split())
        scored_docs = []
        for doc in self.fallback_db:
            content_words = set(doc['content'].lower().split())
            overlap = len(query_words.intersection(content_words))
            # Basic score
            score = overlap / max(len(query_words), 1)
            scored_docs.append((score, doc))
            
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:limit]]
