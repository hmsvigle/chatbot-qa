import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from models.qa_model import QAPair, SearchResult
from utils.config import QA_CSV_PATH, EMBEDDINGS_PATH, DEFAULT_MODEL, DEFAULT_THRESHOLD

class SemanticSearch:
    def __init__(self, csv_path=None, model_name=None, threshold=None):
        self.csv_path = csv_path or str(QA_CSV_PATH)
        self.model_name = model_name or DEFAULT_MODEL
        self.threshold = threshold or DEFAULT_THRESHOLD
        self.model = None
        self.df = None
        self.embeddings = None
        self.embeddings_path = str(EMBEDDINGS_PATH)
        
    def load_data(self):
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"Loaded {len(self.df)} Q&A pairs from {self.csv_path}")
            return True
        except FileNotFoundError:
            print(f"Error: Could not find {self.csv_path}")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def load_model(self):
        try:
            print("Loading sentence transformer model...")
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def generate_embeddings(self):
        if self.df is None or self.model is None:
            print("Data or model not loaded")
            return False
            
        try:
            print("Generating embeddings for questions...")
            questions = self.df['Question'].tolist()
            self.embeddings = self.model.encode(questions)
            
            # Save embeddings to disk
            with open(self.embeddings_path, 'wb') as f:
                pickle.dump(self.embeddings, f)
            print(f"Embeddings generated and saved to {self.embeddings_path}")
            return True
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return False
    
    def load_embeddings(self):
        if os.path.exists(self.embeddings_path):
            try:
                with open(self.embeddings_path, 'rb') as f:
                    self.embeddings = pickle.load(f)
                print("Loaded pre-computed embeddings")
                return True
            except Exception as e:
                print(f"Error loading embeddings: {e}")
        return False
    
    def initialize(self):
        if not self.load_data():
            return False
        
        if not self.load_model():
            return False
        
        # Try to load existing embeddings, otherwise generate new ones
        if not self.load_embeddings():
            if not self.generate_embeddings():
                return False
        
        print("Semantic search initialized successfully!")
        return True
    
    def search(self, query, top_k=1):
        if self.model is None or self.embeddings is None or self.df is None:
            return "System not initialized properly"
        
        try:
            # Encode the query
            query_embedding = self.model.encode([query])
            
            # Calculate cosine similarities
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # Find the best match
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            if best_score >= self.threshold:
                answer = self.df.iloc[best_idx]['Answer']
                confidence = f"(Confidence: {best_score:.2f})"
                return f"{answer} {confidence}"
            else:
                return f"I'm sorry, I don't have enough information to answer that question. (Best match confidence: {best_score:.2f})"
                
        except Exception as e:
            return f"Error processing query: {e}"
    
    def get_stats(self):
        if self.df is not None:
            return f"Knowledge base contains {len(self.df)} Q&A pairs"
        return "No data loaded"