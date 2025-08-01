#!/usr/bin/env python3
"""
Comprehensive demo script to compare different system phases.
Showcases improvements between Phase 1 and Phase 2.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

from services.semantic_search import SemanticSearch
from utils.version_manager import SystemPhase, version_manager

def demo_phase_comparison():
    """Compare Phase 1 and Phase 2 side by side."""
    print("🚀 EJARI CHATBOT - PHASE COMPARISON DEMO")
    print("=" * 60)
    
    # Test queries for demonstration
    demo_queries = [
        "What is EJARI?",
        "How do I register a tenancy contract?", 
        "What documents are required for registration?",
        "What are the rent increase percentages?",
        "What are landlord obligations?",
        "Training requirements for EJARI"
    ]
    
    phases_to_test = [SystemPhase.PHASE_1, SystemPhase.PHASE_2]
    results = {}
    
    for phase in phases_to_test:
        print(f"\n{'='*20} {phase.value.upper().replace('_', ' ')} {'='*20}")
        
        # Initialize system for this phase
        search_system = SemanticSearch(force_phase=phase)
        
        if not search_system.initialize():
            print(f"❌ Failed to initialize {phase.value}")
            continue
            
        print(f"✅ System initialized")
        print(f"📊 {search_system.get_stats()}")
        print(f"🔧 Version: {search_system.get_version_info()['phase_name']}")
        print()
        
        # Test queries
        phase_results = []
        successful_responses = 0
        
        for i, query in enumerate(demo_queries, 1):
            print(f"{i}. Query: '{query}'")
            response = search_system.search(query)
            
            if "I'm sorry, I don't have enough information" not in response:
                successful_responses += 1
                status = "✅ SUCCESS"
                # Show first 100 chars of response
                preview = response[:100] + "..." if len(response) > 100 else response
                print(f"   {status}: {preview}")
            else:
                status = "❌ FAILED"
                print(f"   {status}: Limited knowledge base")
            
            phase_results.append({
                'query': query,
                'response': response,
                'success': "SUCCESS" in status
            })
            print()
        
        success_rate = (successful_responses / len(demo_queries)) * 100
        print(f"📈 Phase Results: {successful_responses}/{len(demo_queries)} queries answered ({success_rate:.1f}%)")
        
        results[phase] = {
            'success_rate': success_rate,
            'successful_responses': successful_responses,
            'total_queries': len(demo_queries),
            'results': phase_results,
            'stats': search_system.get_stats()
        }
    
    # Final comparison
    print(f"\n{'='*60}")
    print("📊 FINAL COMPARISON SUMMARY")
    print(f"{'='*60}")
    
    for phase, data in results.items():
        phase_name = phase.value.replace('_', ' ').title()
        print(f"{phase_name}:")
        print(f"  Success Rate: {data['success_rate']:.1f}%")
        print(f"  Queries Answered: {data['successful_responses']}/{data['total_queries']}")
        print()
    
    if len(results) >= 2:
        phase1_rate = results[SystemPhase.PHASE_1]['success_rate']
        phase2_rate = results[SystemPhase.PHASE_2]['success_rate']
        improvement = phase2_rate - phase1_rate
        
        print(f"🎯 IMPROVEMENT: {improvement:.1f} percentage points")
        if improvement > 0:
            print(f"🎉 Phase 2 shows significant improvement over Phase 1!")
        print()
    
    return results

def demo_individual_phase(phase: SystemPhase):
    """Demo a specific phase in detail."""
    print(f"🔍 DETAILED DEMO - {phase.value.upper().replace('_', ' ')}")
    print("=" * 50)
    
    # Get phase-specific demo queries
    demo_env = version_manager.create_demo_environment(phase)
    queries = demo_env['demo_queries']
    
    # Initialize system
    search_system = SemanticSearch(force_phase=phase)
    
    if not search_system.initialize():
        print(f"❌ Failed to initialize {phase.value}")
        return
    
    # Show system info
    version_info = search_system.get_version_info()
    print(f"📋 Phase: {version_info['phase_name']}")
    print(f"📝 Description: {version_info['description']}")
    print(f"📊 Stats: {search_system.get_stats()}")
    print()
    
    # Test queries
    print("🧪 Testing queries:")
    print("-" * 30)
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: '{query}'")
        response = search_system.search(query)
        print(f"Response: {response}")

def main():
    """Main demo function."""
    print("Welcome to the EJARI Chatbot Phase Comparison Demo!")
    print("Choose an option:")
    print("1. Compare Phase 1 vs Phase 2")
    print("2. Demo Phase 1 only")
    print("3. Demo Phase 2 only")
    print("4. Show available phases")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            demo_phase_comparison()
        elif choice == "2":
            demo_individual_phase(SystemPhase.PHASE_1)
        elif choice == "3":
            demo_individual_phase(SystemPhase.PHASE_2)
        elif choice == "4":
            available_phases = version_manager.get_available_phases()
            print("\n📋 Available Phases:")
            for phase, config in available_phases.items():
                print(f"- {config.name}: {config.description}")
        else:
            print("Invalid choice. Running comparison demo...")
            demo_phase_comparison()
            
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"Error during demo: {e}")
        # Fallback to comparison demo
        demo_phase_comparison()

if __name__ == "__main__":
    main()