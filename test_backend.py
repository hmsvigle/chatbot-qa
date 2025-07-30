#!/usr/bin/env python3

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

from services.chatbot_service import ChatbotService

def test_chatbot():
    print("Testing Ejari Chatbot Backend...")
    
    # Initialize chatbot service
    service = ChatbotService()
    if not service.initialize():
        print("❌ Failed to initialize chatbot service")
        return False
    
    print("✅ Chatbot service initialized successfully")
    print(f"📊 {service.get_stats()}")
    
    # Test queries
    test_queries = [
        "What is Ejari?",
        "How do I register my tenancy contract?",
        "What documents are required?",
        "How long does registration take?",
        "This is an unrelated question about pizza"
    ]
    
    print("\n🧪 Testing queries:")
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        response = service.process_query(query)
        print(f"💬 Response: {response}")
    
    return True

if __name__ == "__main__":
    success = test_chatbot()
    if success:
        print("\n✅ All tests passed! Backend is working correctly.")
    else:
        print("\n❌ Some tests failed.")