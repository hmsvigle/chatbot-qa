"""
Release Management System
Handles version control, backward compatibility, and demonstration capabilities.
Follows development guidelines for consistent release management.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import json
from pathlib import Path

class ReleaseVersion(Enum):
    """Available system releases."""
    PHASE_1 = "phase_1"
    PHASE_2 = "phase_2" 
    PHASE_3 = "phase_3"  # Future release
    LATEST = "latest"    # Auto-detect latest

@dataclass
class ReleaseConfig:
    """Configuration for a specific release."""
    version: str
    name: str
    description: str
    features: List[str]
    technical_doc: str
    test_commands: List[str]
    demo_queries: List[str]
    performance_metrics: Dict[str, Any]
    backward_compatible: bool

class ReleaseManager:
    """
    Manages different system releases according to development guidelines.
    
    Core Principles:
    - UV environment consistency
    - Backward compatibility preservation
    - Local testing per release
    - Documentation per phase
    - Demonstration capabilities
    """
    
    def __init__(self):
        self.current_release = ReleaseVersion.LATEST
        self.release_configs = self._initialize_release_configs()
        
    def _initialize_release_configs(self) -> Dict[ReleaseVersion, ReleaseConfig]:
        """Initialize configuration for each release following guidelines."""
        return {
            ReleaseVersion.PHASE_1: ReleaseConfig(
                version="1.0.0",
                name="Phase 1: CSV-based Q&A System",
                description="Basic semantic search with predefined Q&A pairs",
                features=[
                    "CSV-based knowledge storage",
                    "Basic semantic search",
                    "Confidence scoring",
                    "Simple Q&A matching"
                ],
                technical_doc="PHASE1_TECHNICAL.md",
                test_commands=[
                    "uv run python -c \"from backend.services.semantic_search import SemanticSearch; from backend.utils.version_manager import SystemPhase; s=SemanticSearch(force_phase=SystemPhase.PHASE_1); s.initialize(); print(s.get_stats())\"",
                    "uv run python test_backend.py"
                ],
                demo_queries=[
                    "What is EJARI?",
                    "How do I register my tenancy contract?",
                    "What documents are required?"
                ],
                performance_metrics={
                    "knowledge_base_size": 8,
                    "success_rate": 0.4,
                    "response_type": "basic",
                    "threshold": 0.7
                },
                backward_compatible=True
            ),
            
            ReleaseVersion.PHASE_2: ReleaseConfig(
                version="2.0.0", 
                name="Phase 2: Content-based Knowledge System",
                description="Intelligent document processing with content chunking",
                features=[
                    "Intelligent content parsing",
                    "Automatic document chunking", 
                    "Content categorization",
                    "Contextual responses",
                    "Source attribution",
                    "Enhanced similarity matching",
                    "Direct embedding storage"
                ],
                technical_doc="PHASE2_TECHNICAL.md",
                test_commands=[
                    "uv run python test_final_system.py",
                    "uv run python test_enhanced_system.py",
                    "uv run python demo_comparison.py"
                ],
                demo_queries=[
                    "What is EJARI?",
                    "How do I register a tenancy contract with EJARI?",
                    "What are the rent increase percentages in Dubai?", 
                    "What documents are required for EJARI registration?",
                    "What are landlord obligations?",
                    "Training requirements for EJARI",
                    "Property management companies requirements"
                ],
                performance_metrics={
                    "knowledge_base_size": 178,
                    "success_rate": 0.9,
                    "response_type": "contextual",
                    "threshold": 0.5,
                    "content_types": 6,
                    "improvement_factor": 22
                },
                backward_compatible=True
            )
        }
    
    def get_release_info(self, release: Optional[ReleaseVersion] = None) -> ReleaseConfig:
        """Get configuration for a specific release."""
        target_release = release or self._detect_latest_release()
        return self.release_configs.get(target_release, self.release_configs[ReleaseVersion.PHASE_1])
    
    def _detect_latest_release(self) -> ReleaseVersion:
        """Detect the latest available release based on implementation."""
        # Check for Phase 2 capabilities
        content_file = Path("data/content.txt")
        if content_file.exists() and content_file.stat().st_size > 1000:
            return ReleaseVersion.PHASE_2
        
        # Default to Phase 1
        return ReleaseVersion.PHASE_1
    
    def get_execution_steps(self, release: ReleaseVersion) -> Dict[str, List[str]]:
        """Get execution steps for demonstrating a specific release."""
        config = self.get_release_info(release)
        
        return {
            "environment_setup": [
                "cd /Users/himansu.panigrahy/Documents/Personal_Projects/Chatbots/chatbot-QA",
                "# UV environment (consistent across releases)",
                "uv --version  # Verify UV installation"
            ],
            "testing": config.test_commands,
            "demonstration": [
                f"# Demo {config.name}",
                "uv run streamlit run main.py",
                "# Test with demo queries:",
                *[f"# - {query}" for query in config.demo_queries[:3]]
            ],
            "validation": [
                f"# Expected: {config.performance_metrics.get('success_rate', 'N/A')} success rate",
                f"# Knowledge base: {config.performance_metrics.get('knowledge_base_size', 'N/A')} items"
            ]
        }
    
    def generate_local_test_script(self, release: ReleaseVersion) -> str:
        """Generate local test script for a release (not committed to git)."""
        config = self.get_release_info(release)
        
        script_content = f'''#!/usr/bin/env python3
"""
Local test script for {config.name}
Generated by ReleaseManager - Not committed to git
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

def test_{release.value}():
    """Test {config.name}."""
    print("=" * 60)
    print(f"TESTING {config.name.upper()}")
    print("=" * 60)
    
    from services.semantic_search import SemanticSearch
    from utils.version_manager import SystemPhase
    
    # Initialize system for this release
    search_system = SemanticSearch(force_phase=SystemPhase.{release.name})
    
    if not search_system.initialize():
        print(f"❌ Failed to initialize {release.value}")
        return False
        
    print(f"✅ System initialized")
    print(f"📊 Stats: {{search_system.get_stats()}}")
    print()
    
    # Test demo queries
    demo_queries = {config.demo_queries}
    successful_responses = 0
    
    for i, query in enumerate(demo_queries, 1):
        print(f"{{i}}. Query: '{{query}}'")
        response = search_system.search(query)
        
        if "I'm sorry, I don't have enough information" not in response:
            successful_responses += 1
            print(f"✅ SUCCESS")
        else:
            print(f"❌ FAILED")
        print()
    
    success_rate = (successful_responses / len(demo_queries)) * 100
    expected_rate = {config.performance_metrics.get('success_rate', 0) * 100}
    
    print(f"📈 Results: {{successful_responses}}/{{len(demo_queries)}} queries ({{success_rate:.1f}}%)")
    print(f"📊 Expected: {{expected_rate:.1f}}%")
    
    return success_rate >= expected_rate * 0.8  # Allow 20% variance

if __name__ == "__main__":
    success = test_{release.value}()
    print(f"\\n{'✅ PASS' if success else '❌ FAIL'}: {config.name}")
'''
        
        return script_content
    
    def get_demonstration_plan(self) -> Dict[str, Any]:
        """Get comprehensive demonstration plan for all releases."""
        plan = {
            "overview": "Demonstration plan following development guidelines",
            "environment": {
                "manager": "UV package manager", 
                "venv": ".venv (consistent across releases)",
                "python": "3.13+"
            },
            "releases": {}
        }
        
        for release, config in self.release_configs.items():
            if release in [ReleaseVersion.PHASE_1, ReleaseVersion.PHASE_2]:  # Only implemented releases
                plan["releases"][release.value] = {
                    "name": config.name,
                    "version": config.version,
                    "execution_steps": self.get_execution_steps(release),
                    "technical_doc": config.technical_doc,
                    "performance_metrics": config.performance_metrics,
                    "demo_queries": config.demo_queries
                }
        
        return plan
    
    def create_release_comparison(self, releases: List[ReleaseVersion]) -> Dict[str, Any]:
        """Create comparison between specified releases."""
        comparison = {
            "releases_compared": [r.value for r in releases],
            "metrics": {},
            "features": {},
            "improvements": {}
        }
        
        for release in releases:
            config = self.get_release_info(release)
            comparison["metrics"][release.value] = config.performance_metrics
            comparison["features"][release.value] = config.features
        
        # Calculate improvements if comparing Phase 1 and Phase 2
        if ReleaseVersion.PHASE_1 in releases and ReleaseVersion.PHASE_2 in releases:
            phase1_metrics = self.get_release_info(ReleaseVersion.PHASE_1).performance_metrics
            phase2_metrics = self.get_release_info(ReleaseVersion.PHASE_2).performance_metrics
            
            comparison["improvements"] = {
                "knowledge_base_expansion": f"{phase2_metrics['knowledge_base_size'] / phase1_metrics['knowledge_base_size']:.1f}x",
                "success_rate_improvement": f"{(phase2_metrics['success_rate'] - phase1_metrics['success_rate']) * 100:.1f} percentage points",
                "response_enhancement": f"{phase1_metrics['response_type']} → {phase2_metrics['response_type']}"
            }
        
        return comparison

# Global instance following singleton pattern
release_manager = ReleaseManager()