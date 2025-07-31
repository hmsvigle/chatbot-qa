import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from models.qa_model import QAPair, SearchResult
from utils.config import QA_CSV_PATH, EMBEDDINGS_PATH, DEFAULT_MODEL, DEFAULT_THRESHOLD, DATA_DIR
from utils.content_parser import ContentParser

class SemanticSearch:
    def __init__(self, content_file=None, csv_path=None, model_name=None, threshold=None):
        self.content_file = content_file or str(DATA_DIR / "content.txt")
        self.csv_path = csv_path or str(QA_CSV_PATH)
        self.model_name = model_name or DEFAULT_MODEL
        self.threshold = threshold or DEFAULT_THRESHOLD
        self.model = None
        self.df = None  # Keep for backward compatibility with existing CSV data
        self.content_chunks = []  # New: store parsed content chunks
        self.embeddings = None
        self.embeddings_path = str(EMBEDDINGS_PATH)
        self.content_parser = ContentParser()
        self.use_content_mode = True  # Flag to use new content-based approach
        
    def load_data(self):
        """Load data from both content file and CSV for backward compatibility."""
        success = False
        
        # Try to load content chunks first
        if self.use_content_mode and os.path.exists(self.content_file):
            try:
                print(f"Loading content from {self.content_file}...")
                self.content_chunks = self.content_parser.parse_file(self.content_file)
                print(f"Loaded {len(self.content_chunks)} content chunks")
                
                # Print statistics
                stats = self.content_parser.get_stats(self.content_chunks)
                if stats:
                    print(f"Content statistics: {stats}")
                
                success = True
            except Exception as e:
                print(f"Error loading content file: {e}")
                print("Falling back to CSV mode...")
                self.use_content_mode = False
        
        # Fallback to CSV or load both
        if not self.use_content_mode or not success:
            try:
                self.df = pd.read_csv(self.csv_path)
                print(f"Loaded {len(self.df)} Q&A pairs from {self.csv_path}")
                success = True
            except FileNotFoundError:
                print(f"Error: Could not find {self.csv_path}")
                return False
            except Exception as e:
                print(f"Error loading CSV data: {e}")
                return False
        
        return success
    
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
        """Generate embeddings for content chunks or CSV questions."""
        if self.model is None:
            print("Model not loaded")
            return False
            
        try:
            if self.use_content_mode and self.content_chunks:
                print("Generating embeddings for content chunks...")
                texts = [chunk['content'] for chunk in self.content_chunks]
                self.embeddings = self.model.encode(texts)
                
                # Save embeddings with content data
                embedding_data = {
                    'embeddings': self.embeddings,
                    'content_chunks': self.content_chunks,
                    'mode': 'content',
                    'model_name': self.model_name
                }
                
            elif self.df is not None:
                print("Generating embeddings for CSV questions...")
                questions = self.df['Question'].tolist()
                self.embeddings = self.model.encode(questions)
                
                # Save embeddings with CSV data for backward compatibility
                embedding_data = {
                    'embeddings': self.embeddings,
                    'df_data': self.df.to_dict('records'),
                    'mode': 'csv',
                    'model_name': self.model_name
                }
            else:
                print("No data available for embedding generation")
                return False
            
            # Save to disk
            with open(self.embeddings_path, 'wb') as f:
                pickle.dump(embedding_data, f)
            print(f"Embeddings generated and saved to {self.embeddings_path}")
            return True
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return False
    
    def load_embeddings(self):
        """Load embeddings and associated data from disk."""
        if os.path.exists(self.embeddings_path):
            try:
                with open(self.embeddings_path, 'rb') as f:
                    data = pickle.load(f)
                
                # Handle new format with embedded content
                if isinstance(data, dict) and 'embeddings' in data:
                    self.embeddings = data['embeddings']
                    
                    if data.get('mode') == 'content' and 'content_chunks' in data:
                        self.content_chunks = data['content_chunks']
                        self.use_content_mode = True
                        print(f"Loaded pre-computed embeddings for {len(self.content_chunks)} content chunks")
                    elif data.get('mode') == 'csv' and 'df_data' in data:
                        self.df = pd.DataFrame(data['df_data'])
                        self.use_content_mode = False
                        print(f"Loaded pre-computed embeddings for {len(self.df)} CSV entries")
                    
                # Handle legacy format (just embeddings array)
                else:
                    self.embeddings = data
                    print("Loaded legacy embeddings format")
                
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
        """Search for the most relevant content based on the query."""
        if self.model is None or self.embeddings is None:
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
                if self.use_content_mode and self.content_chunks:
                    # Return content from chunks
                    best_chunk = self.content_chunks[best_idx]
                    answer = best_chunk['content']
                    context = best_chunk.get('context', '')
                    content_type = best_chunk.get('type', 'general')
                    
                    # Format response with context
                    response = f"{answer}"
                    if context and context != "General Information":
                        response += f"\n\n*Source: {context}*"
                    
                    confidence = f"\n(Confidence: {best_score:.2f}, Type: {content_type})"
                    return f"{response} {confidence}"
                    
                elif self.df is not None:
                    # Fallback to CSV mode
                    answer = self.df.iloc[best_idx]['Answer']
                    confidence = f"(Confidence: {best_score:.2f})"
                    return f"{answer} {confidence}"
                else:
                    return "No content available for response"
            else:
                return f"I'm sorry, I don't have enough information to answer that question. (Best match confidence: {best_score:.2f})"
                
        except Exception as e:
            return f"Error processing query: {e}"
    
    def get_stats(self):
        """Get statistics about the current knowledge base."""
        stats = []
        
        if self.use_content_mode and self.content_chunks:
            chunk_stats = self.content_parser.get_stats(self.content_chunks)
            stats.append(f"Content chunks: {len(self.content_chunks)}")
            if chunk_stats.get('types'):
                type_info = ", ".join([f"{k}: {v}" for k, v in chunk_stats['types'].items()])
                stats.append(f"Types: {type_info}")
        
        if self.df is not None:
            stats.append(f"CSV Q&A pairs: {len(self.df)}")
        
        if self.embeddings is not None:
            stats.append(f"Embeddings: {len(self.embeddings)}")
        
        return "Knowledge base - " + "; ".join(stats) if stats else "No data loaded"