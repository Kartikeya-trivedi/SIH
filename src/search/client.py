from opensearchpy import OpenSearch, RequestsHttpConnection
from typing import Dict, List, Any, Optional
import json
import os

from src.core.config import settings
from src.core.logging import LoggerMixin


class OpenSearchClient(LoggerMixin):
    """OpenSearch client for text and vector search operations."""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenSearch client."""
        try:
            # Configure authentication if credentials are provided
            auth = None
            if settings.opensearch_username and settings.opensearch_password:
                auth = (settings.opensearch_username, settings.opensearch_password)
            
            # Create client
            self.client = OpenSearch(
                hosts=[settings.opensearch_url],
                http_auth=auth,
                use_ssl=False,  # Set to True in production
                verify_certs=False,  # Set to True in production
                connection_class=RequestsHttpConnection,
                timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
            
            # Test connection
            self.client.ping()
            self.logger.info("OpenSearch client initialized successfully")
            
        except Exception as e:
            self.logger.error("Failed to initialize OpenSearch client", error=str(e))
            self.client = None
    
    def create_index(self, index_name: str, mapping: Dict[str, Any]) -> bool:
        """Create an index with the specified mapping."""
        try:
            if not self.client:
                return False
            
            # Check if index exists
            if self.client.indices.exists(index=index_name):
                self.logger.info("Index already exists", index_name=index_name)
                return True
            
            # Create index
            self.client.indices.create(
                index=index_name,
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "analysis": {
                            "analyzer": {
                                "custom_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "standard",
                                    "filter": ["lowercase", "stop", "snowball"]
                                }
                            }
                        }
                    },
                    "mappings": mapping
                }
            )
            
            self.logger.info("Index created successfully", index_name=index_name)
            return True
            
        except Exception as e:
            self.logger.error("Failed to create index", error=str(e), index_name=index_name)
            return False
    
    def index_document(self, index_name: str, document: Dict[str, Any], doc_id: Optional[str] = None) -> bool:
        """Index a document."""
        try:
            if not self.client:
                return False
            
            self.client.index(
                index=index_name,
                body=document,
                id=doc_id
            )
            
            self.logger.info("Document indexed successfully", index_name=index_name, doc_id=doc_id)
            return True
            
        except Exception as e:
            self.logger.error("Failed to index document", error=str(e), index_name=index_name, doc_id=doc_id)
            return False
    
    def search_documents(
        self, 
        index_name: str, 
        query: Dict[str, Any], 
        size: int = 10,
        from_: int = 0
    ) -> Dict[str, Any]:
        """Search documents in an index."""
        try:
            if not self.client:
                return {"hits": {"hits": [], "total": {"value": 0}}}
            
            response = self.client.search(
                index=index_name,
                body=query,
                size=size,
                from_=from_
            )
            
            self.logger.info("Search completed", index_name=index_name, total_hits=response["hits"]["total"]["value"])
            return response
            
        except Exception as e:
            self.logger.error("Search failed", error=str(e), index_name=index_name)
            return {"hits": {"hits": [], "total": {"value": 0}}}
    
    def delete_document(self, index_name: str, doc_id: str) -> bool:
        """Delete a document from an index."""
        try:
            if not self.client:
                return False
            
            self.client.delete(index=index_name, id=doc_id)
            
            self.logger.info("Document deleted successfully", index_name=index_name, doc_id=doc_id)
            return True
            
        except Exception as e:
            self.logger.error("Failed to delete document", error=str(e), index_name=index_name, doc_id=doc_id)
            return False
    
    def bulk_index(self, index_name: str, documents: List[Dict[str, Any]]) -> bool:
        """Bulk index multiple documents."""
        try:
            if not self.client:
                return False
            
            # Prepare bulk data
            bulk_data = []
            for doc in documents:
                bulk_data.append({
                    "index": {
                        "_index": index_name,
                        "_id": doc.get("id")
                    }
                })
                bulk_data.append(doc)
            
            # Execute bulk operation
            response = self.client.bulk(body=bulk_data)
            
            # Check for errors
            if response.get("errors"):
                self.logger.error("Bulk indexing had errors", errors=response["errors"])
                return False
            
            self.logger.info("Bulk indexing completed", index_name=index_name, count=len(documents))
            return True
            
        except Exception as e:
            self.logger.error("Bulk indexing failed", error=str(e), index_name=index_name)
            return False


class SearchService(LoggerMixin):
    """Service for search operations using OpenSearch."""
    
    def __init__(self):
        self.client = OpenSearchClient()
        self._initialize_indices()
    
    def _initialize_indices(self):
        """Initialize required indices."""
        # Kolam images index
        kolam_mapping = {
            "properties": {
                "title": {"type": "text", "analyzer": "custom_analyzer"},
                "description": {"type": "text", "analyzer": "custom_analyzer"},
                "tags": {"type": "keyword"},
                "detected_patterns": {"type": "keyword"},
                "symmetry_type": {"type": "keyword"},
                "complexity_score": {"type": "float"},
                "user_id": {"type": "integer"},
                "is_public": {"type": "boolean"},
                "created_at": {"type": "date"},
                "image_vector": {"type": "dense_vector", "dims": 512}  # For vector search
            }
        }
        self.client.create_index("kolam_images", kolam_mapping)
        
        # Trivia questions index
        questions_mapping = {
            "properties": {
                "question_text": {"type": "text", "analyzer": "custom_analyzer"},
                "question_type": {"type": "keyword"},
                "difficulty_level": {"type": "integer"},
                "category": {"type": "keyword"},
                "tags": {"type": "keyword"},
                "correct_answer": {"type": "text"},
                "explanation": {"type": "text", "analyzer": "custom_analyzer"},
                "is_active": {"type": "boolean"},
                "created_at": {"type": "date"}
            }
        }
        self.client.create_index("trivia_questions", questions_mapping)
    
    def search_similar_kolams(
        self,
        query_text: Optional[str] = None,
        tags: Optional[List[str]] = None,
        pattern_types: Optional[List[str]] = None,
        complexity_range: Optional[tuple] = None,
        user_id: Optional[int] = None,
        size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for similar Kolam images."""
        query = {"query": {"bool": {"must": []}}}
        
        # Text search
        if query_text:
            query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query_text,
                    "fields": ["title^2", "description", "tags"],
                    "type": "best_fields"
                }
            })
        
        # Filter by tags
        if tags:
            query["query"]["bool"]["must"].append({
                "terms": {"tags": tags}
            })
        
        # Filter by pattern types
        if pattern_types:
            query["query"]["bool"]["must"].append({
                "terms": {"detected_patterns": pattern_types}
            })
        
        # Filter by complexity range
        if complexity_range:
            query["query"]["bool"]["must"].append({
                "range": {
                    "complexity_score": {
                        "gte": complexity_range[0],
                        "lte": complexity_range[1]
                    }
                }
            })
        
        # Filter by user or public images
        if user_id:
            query["query"]["bool"]["must"].append({
                "bool": {
                    "should": [
                        {"term": {"user_id": user_id}},
                        {"term": {"is_public": True}}
                    ]
                }
            })
        else:
            query["query"]["bool"]["must"].append({
                "term": {"is_public": True}
            })
        
        response = self.client.search_documents("kolam_images", query, size=size)
        return [hit["_source"] for hit in response["hits"]["hits"]]
    
    def search_trivia_questions(
        self,
        query_text: Optional[str] = None,
        category: Optional[str] = None,
        difficulty_level: Optional[int] = None,
        tags: Optional[List[str]] = None,
        size: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for trivia questions."""
        query = {"query": {"bool": {"must": []}}}
        
        # Text search
        if query_text:
            query["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query_text,
                    "fields": ["question_text^2", "explanation"],
                    "type": "best_fields"
                }
            })
        
        # Filter by category
        if category:
            query["query"]["bool"]["must"].append({
                "term": {"category": category}
            })
        
        # Filter by difficulty level
        if difficulty_level:
            query["query"]["bool"]["must"].append({
                "term": {"difficulty_level": difficulty_level}
            })
        
        # Filter by tags
        if tags:
            query["query"]["bool"]["must"].append({
                "terms": {"tags": tags}
            })
        
        # Only active questions
        query["query"]["bool"]["must"].append({
            "term": {"is_active": True}
        })
        
        response = self.client.search_documents("trivia_questions", query, size=size)
        return [hit["_source"] for hit in response["hits"]["hits"]]
    
    def vector_search_similar_kolams(
        self,
        vector: List[float],
        size: int = 10,
        user_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar Kolam images using vector similarity."""
        query = {
            "query": {
                "knn": {
                    "image_vector": {
                        "vector": vector,
                        "k": size
                    }
                }
            }
        }
        
        # Filter by user or public images
        if user_id:
            query["query"]["knn"]["filter"] = {
                "bool": {
                    "should": [
                        {"term": {"user_id": user_id}},
                        {"term": {"is_public": True}}
                    ]
                }
            }
        else:
            query["query"]["knn"]["filter"] = {
                "term": {"is_public": True}
            }
        
        response = self.client.search_documents("kolam_images", query, size=size)
        return [hit["_source"] for hit in response["hits"]["hits"]]
    
    def index_kolam_image(self, kolam_data: Dict[str, Any]) -> bool:
        """Index a Kolam image for search."""
        return self.client.index_document("kolam_images", kolam_data, str(kolam_data["id"]))
    
    def index_trivia_question(self, question_data: Dict[str, Any]) -> bool:
        """Index a trivia question for search."""
        return self.client.index_document("trivia_questions", question_data, str(question_data["id"]))
    
    def delete_kolam_image(self, image_id: int) -> bool:
        """Remove a Kolam image from search index."""
        return self.client.delete_document("kolam_images", str(image_id))
    
    def delete_trivia_question(self, question_id: int) -> bool:
        """Remove a trivia question from search index."""
        return self.client.delete_document("trivia_questions", str(question_id))

