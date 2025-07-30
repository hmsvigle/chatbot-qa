import sys
from pathlib import Path
from typing import List, Optional

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from services.semantic_search import SemanticSearch
from models.qa_model import ChatMessage, SearchResult

class ChatbotService:
    def __init__(self):
        self.search_engine = None
        self.initialized = False
        
    def initialize(self) -> bool:
        try:
            self.search_engine = SemanticSearch()
            if self.search_engine.initialize():
                self.initialized = True
                return True
            return False
        except Exception as e:
            print(f"Error initializing chatbot service: {e}")
            return False
    
    def process_query(self, query: str) -> str:
        if not self.initialized or not self.search_engine:
            return "Chatbot service is not initialized properly."
        
        try:
            response = self.search_engine.search(query)
            return response
        except Exception as e:
            return f"Error processing query: {e}"
    
    def get_stats(self) -> str:
        if self.search_engine:
            return self.search_engine.get_stats()
        return "Service not initialized"
    
    def update_threshold(self, threshold: float) -> bool:
        if self.search_engine:
            self.search_engine.threshold = threshold
            return True
        return False