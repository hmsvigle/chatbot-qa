#!/usr/bin/env python3
"""
Test script for the enhanced semantic search system with content chunks.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

from services.semantic_search import SemanticSearch

def test_content_parsing():
    """Test the content parsing functionality."""
    print("=" * 60)
    print("TESTING CONTENT PARSING")
    print("=" * 60)
    
    # Initialize the semantic search system
    search_system = SemanticSearch()
    
    # Load and parse content
    if search_system.load_data():
        print("✓ Content loading successful")
        
        # Print statistics
        stats = search_system.get_stats()
        print(f"Stats: {stats}")
        
        if search_system.content_chunks:
            print(f"\nFirst few content chunks:")
            for i, chunk in enumerate(search_system.content_chunks[:3]):
                print(f"\nChunk {i+1}:")
                print(f"  Context: {chunk['context']}")
                print(f"  Type: {chunk['type']}")
                print(f"  Content: {chunk['content'][:200]}...")
        
        return True
    else:
        print("✗ Content loading failed")
        return False

def test_model_loading():
    """Test model loading."""
    print("\n" + "=" * 60)
    print("TESTING MODEL LOADING")
    print("=" * 60)
    
    search_system = SemanticSearch()
    
    if search_system.load_model():
        print("✓ Model loading successful")
        return search_system
    else:
        print("✗ Model loading failed")
        return None

def test_embedding_generation(search_system):
    """Test embedding generation."""
    print("\n" + "=" * 60)
    print("TESTING EMBEDDING GENERATION")
    print("=" * 60)
    
    # Load data first
    if not search_system.load_data():
        print("✗ Could not load data for embedding generation")
        return False
    
    # Generate embeddings
    if search_system.generate_embeddings():
        print("✓ Embedding generation successful")
        print(f"Generated embeddings shape: {search_system.embeddings.shape}")
        return True
    else:
        print("✗ Embedding generation failed")
        return False

def test_search_functionality(search_system):
    """Test search functionality with sample queries."""
    print("\n" + "=" * 60)
    print("TESTING SEARCH FUNCTIONALITY")
    print("=" * 60)
    
    # Initialize the system
    if not search_system.initialize():
        print("✗ System initialization failed")
        return False
    
    # Test queries
    test_queries = [
        "What is EJARI?",
        "How do I register a tenancy contract?",
        "What documents are required for registration?",
        "What are the rent increase percentages?",
        "Who can use EJARI system?",
        "What is the vision of RERA?",
    ]
    
    print("Testing search queries:")
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 50)
        
        response = search_system.search(query)
        print(f"Response: {response}")
    
    return True

def test_backward_compatibility():
    """Test backward compatibility with CSV mode."""
    print("\n" + "=" * 60)
    print("TESTING BACKWARD COMPATIBILITY (CSV MODE)")
    print("=" * 60)
    
    # Create system with content mode disabled
    search_system = SemanticSearch()
    search_system.use_content_mode = False
    
    if search_system.initialize():
        print("✓ CSV mode initialization successful")
        
        # Test a simple query
        response = search_system.search("What is EJARI?")
        print(f"CSV mode response: {response}")
        return True
    else:
        print("✗ CSV mode initialization failed")
        return False

def main():
    """Run all tests."""
    print("Enhanced Semantic Search System - Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Content parsing
        if not test_content_parsing():
            print("\n❌ Content parsing test failed")
            return
        
        # Test 2: Model loading
        search_system = test_model_loading()
        if not search_system:
            print("\n❌ Model loading test failed")
            return
        
        # Test 3: Embedding generation
        if not test_embedding_generation(search_system):
            print("\n❌ Embedding generation test failed")
            return
        
        # Test 4: Search functionality
        if not test_search_functionality(search_system):
            print("\n❌ Search functionality test failed")
            return
        
        # Test 5: Backward compatibility
        if not test_backward_compatibility():
            print("\n⚠️  Backward compatibility test failed (CSV mode)")
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        # Final system stats
        final_stats = search_system.get_stats()
        print(f"\nFinal System Stats: {final_stats}")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()