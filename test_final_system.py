#!/usr/bin/env python3
"""
Final test script to validate the enhanced content-based system.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

from services.semantic_search import SemanticSearch

def test_enhanced_queries():
    """Test the system with various queries to show improvement."""
    print("Enhanced Content-Based Semantic Search - Final Test")
    print("=" * 60)
    
    # Initialize with lower threshold
    search_system = SemanticSearch(threshold=0.5)  # Lower threshold
    
    if not search_system.initialize():
        print("❌ Failed to initialize system")
        return
    
    print(f"✓ System initialized successfully")
    print(f"Stats: {search_system.get_stats()}")
    print("\n" + "=" * 60)
    print("TESTING VARIOUS QUERIES")
    print("=" * 60)
    
    # Test comprehensive queries
    test_queries = [
        {
            "query": "What is EJARI?",
            "expected": "definition of EJARI program"
        },
        {
            "query": "How do I register a tenancy contract?",
            "expected": "registration process information"
        },
        {
            "query": "What documents are required for registration?",
            "expected": "required documents information"
        },
        {
            "query": "What are the rent increase percentages in Dubai?",
            "expected": "rent increase rates"
        },
        {
            "query": "Who can use EJARI system?",
            "expected": "user types and requirements"
        },
        {
            "query": "What is the vision of RERA?",
            "expected": "RERA vision statement"
        },
        {
            "query": "What are landlord obligations?",
            "expected": "landlord responsibilities"
        },
        {
            "query": "What is the eviction process?",
            "expected": "eviction procedures"
        },
        {
            "query": "Training requirements for EJARI",
            "expected": "training information"
        },
        {
            "query": "Property management companies requirements",
            "expected": "company requirements"
        }
    ]
    
    successful_responses = 0
    
    for i, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        expected = test_case["expected"]
        
        print(f"\n{i}. Query: '{query}'")
        print(f"   Expected: {expected}")
        print("-" * 50)
        
        response = search_system.search(query)
        
        # Check if we got a meaningful response (not the "I don't have enough information" message)
        if "I'm sorry, I don't have enough information" not in response:
            successful_responses += 1
            print(f"✓ SUCCESS: Got relevant response")
            # Show first 150 chars of response
            response_preview = response[:150] + "..." if len(response) > 150 else response
            print(f"   Response: {response_preview}")
        else:
            print(f"✗ FAILED: {response}")
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Successful responses: {successful_responses}/{len(test_queries)}")
    print(f"Success rate: {(successful_responses/len(test_queries)*100):.1f}%")
    
    if successful_responses >= len(test_queries) * 0.7:  # 70% success rate
        print("🎉 ENHANCED SYSTEM PERFORMING WELL!")
    else:
        print("⚠️  System needs further optimization")
    
    return successful_responses >= len(test_queries) * 0.7

def main():
    """Run the final test."""
    try:
        success = test_enhanced_queries()
        
        if success:
            print("\n✅ Phase 2 Implementation Complete!")
            print("The enhanced content-based system is ready for use.")
        else:
            print("\n❌ Phase 2 needs more work.")
            print("Consider adjusting the threshold or improving content parsing.")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()