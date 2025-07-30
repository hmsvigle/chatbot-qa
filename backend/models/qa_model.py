from dataclasses import dataclass
from typing import List, Optional

@dataclass
class QAPair:
    question: str
    answer: str
    confidence: Optional[float] = None

@dataclass
class SearchResult:
    answer: str
    confidence: float
    question_matched: str
    
@dataclass
class ChatMessage:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None