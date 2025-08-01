"""
Version Manager for Multi-Phase System Demonstration
Enables switching between different system phases/modes for showcasing improvements.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional
import os
from pathlib import Path

class SystemPhase(Enum):
    """Enumeration of available system phases."""
    PHASE_1 = "phase_1"  # CSV-based Q&A system
    PHASE_2 = "phase_2"  # Content-based knowledge system
    PHASE_3 = "phase_3"  # Future: Multi-document processing
    AUTO = "auto"        # Automatic mode detection

@dataclass
class PhaseConfig:
    """Configuration for a specific system phase."""
    name: str
    description: str
    data_source: str
    threshold: float
    features: list
    storage_format: str
    embedding_mode: str

class VersionManager:
    """
    Manages different system phases and enables easy switching between them.
    This allows for demonstration of improvements across different versions.
    """
    
    def __init__(self):
        self.current_phase = SystemPhase.AUTO
        self.phase_configs = self._initialize_phase_configs()
        
    def _initialize_phase_configs(self) -> Dict[SystemPhase, PhaseConfig]:
        """Initialize configuration for each system phase."""
        return {
            SystemPhase.PHASE_1: PhaseConfig(
                name="Phase 1: CSV-based Q&A",
                description="Basic semantic search with predefined Q&A pairs",
                data_source="qa.csv",
                threshold=0.7,
                features=[
                    "Basic semantic search",
                    "CSV-based knowledge base", 
                    "Simple Q&A matching",
                    "Confidence scoring"
                ],
                storage_format="csv_embeddings",
                embedding_mode="questions_only"
            ),
            
            SystemPhase.PHASE_2: PhaseConfig(
                name="Phase 2: Content-based Knowledge System", 
                description="Intelligent document processing with content chunking",
                data_source="content.txt",
                threshold=0.5,
                features=[
                    "Intelligent content parsing",
                    "Automatic document chunking",
                    "Content categorization",
                    "Contextual responses",
                    "Source attribution",
                    "Enhanced similarity matching"
                ],
                storage_format="content_embeddings",
                embedding_mode="content_chunks"
            ),
            
            SystemPhase.PHASE_3: PhaseConfig(
                name="Phase 3: Multi-document Knowledge Fusion",
                description="Advanced multi-source content processing (Future)",
                data_source="multiple_sources",
                threshold=0.4,
                features=[
                    "Multi-document processing",
                    "Knowledge graph integration",
                    "Cross-reference linking",
                    "Advanced NLP features"
                ],
                storage_format="graph_embeddings", 
                embedding_mode="knowledge_graph"
            )
        }
    
    def set_phase(self, phase: SystemPhase) -> bool:
        """
        Set the current system phase.
        
        Args:
            phase: The phase to switch to
            
        Returns:
            bool: True if phase switch was successful
        """
        if phase in self.phase_configs:
            self.current_phase = phase
            return True
        return False
    
    def get_current_phase(self) -> SystemPhase:
        """Get the currently active phase."""
        return self.current_phase
    
    def get_phase_config(self, phase: Optional[SystemPhase] = None) -> PhaseConfig:
        """
        Get configuration for a specific phase.
        
        Args:
            phase: Phase to get config for (current phase if None)
            
        Returns:
            PhaseConfig: Configuration for the specified phase
        """
        target_phase = phase or self.current_phase
        if target_phase == SystemPhase.AUTO:
            target_phase = self._detect_optimal_phase()
            
        return self.phase_configs.get(target_phase, self.phase_configs[SystemPhase.PHASE_1])
    
    def _detect_optimal_phase(self) -> SystemPhase:
        """
        Automatically detect the optimal phase based on available data.
        
        Returns:
            SystemPhase: The detected optimal phase
        """
        # Check for Phase 2 content
        content_file = Path("data/content.txt")
        if content_file.exists() and content_file.stat().st_size > 1000:  # Has substantial content
            return SystemPhase.PHASE_2
        
        # Check for Phase 1 CSV data
        csv_file = Path("data/qa.csv") 
        if csv_file.exists():
            return SystemPhase.PHASE_1
            
        # Default fallback
        return SystemPhase.PHASE_1
    
    def get_available_phases(self) -> Dict[SystemPhase, PhaseConfig]:
        """Get all available phases and their configurations."""
        available = {}
        
        for phase, config in self.phase_configs.items():
            if phase == SystemPhase.PHASE_3:  # Skip future phases
                continue
                
            # Check if phase data is available
            if self._is_phase_available(phase):
                available[phase] = config
                
        return available
    
    def _is_phase_available(self, phase: SystemPhase) -> bool:
        """Check if a phase has the required data available."""
        config = self.phase_configs[phase]
        
        if phase == SystemPhase.PHASE_1:
            return Path("data/qa.csv").exists()
        elif phase == SystemPhase.PHASE_2:
            return Path("data/content.txt").exists()
        elif phase == SystemPhase.PHASE_3:
            return False  # Future phase not implemented
            
        return False
    
    def get_phase_comparison(self) -> Dict[str, Any]:
        """
        Get a comparison of different phases for demonstration purposes.
        
        Returns:
            Dict containing comparison metrics and features
        """
        comparison = {
            "phases": {},
            "metrics": {
                "knowledge_base_size": {},
                "features_count": {},
                "data_sources": {}
            }
        }
        
        for phase, config in self.get_available_phases().items():
            comparison["phases"][phase.value] = {
                "name": config.name,
                "description": config.description,
                "features": config.features,
                "threshold": config.threshold,
                "data_source": config.data_source
            }
            
            # Add metrics
            comparison["metrics"]["features_count"][phase.value] = len(config.features)
            comparison["metrics"]["data_sources"][phase.value] = config.data_source
            
        return comparison
    
    def create_demo_environment(self, phase: SystemPhase) -> Dict[str, Any]:
        """
        Create environment settings for demonstration of a specific phase.
        
        Args:
            phase: Phase to create demo environment for
            
        Returns:
            Dict containing environment configuration
        """
        config = self.get_phase_config(phase)
        
        return {
            "phase": phase.value,
            "config": config,
            "environment_vars": {
                "DEMO_MODE": "true",
                "SYSTEM_PHASE": phase.value,
                "SIMILARITY_THRESHOLD": str(config.threshold),
                "DATA_SOURCE": config.data_source
            },
            "demo_queries": self._get_demo_queries_for_phase(phase)
        }
    
    def _get_demo_queries_for_phase(self, phase: SystemPhase) -> list:
        """Get appropriate demo queries for a specific phase."""
        base_queries = [
            "What is EJARI?",
            "How do I register a tenancy contract?",
            "What documents are required?"
        ]
        
        if phase == SystemPhase.PHASE_1:
            return base_queries[:3]  # Limited queries for Phase 1
        elif phase == SystemPhase.PHASE_2:
            return base_queries + [
                "What are the rent increase percentages?",
                "What are landlord obligations?", 
                "What is the eviction process?",
                "Training requirements for EJARI",
                "Property management companies requirements"
            ]
        else:
            return base_queries
    
    def get_version_info(self) -> Dict[str, str]:
        """Get current version information."""
        config = self.get_phase_config()
        
        return {
            "current_phase": self.current_phase.value,
            "phase_name": config.name,
            "description": config.description,
            "data_source": config.data_source,
            "features": ", ".join(config.features[:3]) + "..." if len(config.features) > 3 else ", ".join(config.features)
        }

# Global version manager instance
version_manager = VersionManager()