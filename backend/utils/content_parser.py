import re
from typing import List, Dict, Tuple
from pathlib import Path

class ContentParser:
    """
    Parser to extract meaningful chunks from plain text content.
    Designed to process EJARI documentation and similar structured content.
    """
    
    def __init__(self, min_chunk_size: int = 100, max_chunk_size: int = 400):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        
    def parse_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        Parse a text file and extract meaningful content chunks.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of dictionaries containing parsed content chunks
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return self.parse_content(content)
            
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
    
    def parse_content(self, content: str) -> List[Dict[str, str]]:
        """
        Parse raw content and extract structured chunks.
        
        Args:
            content: Raw text content
            
        Returns:
            List of content chunks with metadata
        """
        chunks = []
        
        # Clean and normalize content
        content = self._clean_content(content)
        
        # Extract sections based on structure
        sections = self._extract_sections(content)
        
        for section_title, section_content in sections:
            # Break each section into smaller chunks if needed
            section_chunks = self._create_chunks(section_content, section_title)
            chunks.extend(section_chunks)
        
        return chunks
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize the raw content."""
        # Remove line numbers at the start of lines
        content = re.sub(r'^\s*\d+→', '', content, flags=re.MULTILINE)
        
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove excessive spaces
        content = re.sub(r' +', ' ', content)
        
        return content.strip()
    
    def _extract_sections(self, content: str) -> List[Tuple[str, str]]:
        """Extract sections from the content based on structure."""
        sections = []
        
        # Define section patterns
        chapter_pattern = r'Chapter\s+[IVX]+\s+([^.]+)'
        heading_pattern = r'([A-Z][^.!?]*(?:Program|Guide|Mechanisms|Training|Registration|Documents|Obligations|Provisions|Index))\s*\n'
        
        # Find chapters
        chapters = re.finditer(chapter_pattern, content, re.IGNORECASE)
        chapter_positions = [(m.start(), m.group(1).strip(), m.group(0)) for m in chapters]
        
        # Process content by chapters or major sections
        if chapter_positions:
            for i, (start_pos, title, full_match) in enumerate(chapter_positions):
                end_pos = chapter_positions[i + 1][0] if i + 1 < len(chapter_positions) else len(content)
                section_content = content[start_pos:end_pos]
                sections.append((title, section_content))
        else:
            # Fallback: split by major headings or paragraphs
            sections = self._extract_by_paragraphs(content)
        
        return sections
    
    def _extract_by_paragraphs(self, content: str) -> List[Tuple[str, str]]:
        """Extract sections by splitting into logical paragraphs."""
        sections = []
        
        # Split by double newlines or major breaks
        paragraphs = re.split(r'\n\s*\n|\. \s*(?=[A-Z])', content)
        
        current_section = ""
        section_title = "General Information"
        
        for para in paragraphs:
            para = para.strip()
            if len(para) < 20:  # Skip very short paragraphs
                continue
                
            # Check if this looks like a new section title
            if self._is_section_title(para):
                # Save previous section if it has content
                if current_section.strip():
                    sections.append((section_title, current_section))
                
                # Start new section
                section_title = para[:50] + "..." if len(para) > 50 else para
                current_section = para
            else:
                current_section += " " + para
        
        # Add the last section
        if current_section.strip():
            sections.append((section_title, current_section))
        
        return sections
    
    def _is_section_title(self, text: str) -> bool:
        """Determine if text looks like a section title."""
        # Check for common title patterns
        title_indicators = [
            'About', 'What is', 'How to', 'Documents', 'Required', 
            'Registration', 'Process', 'Obligations', 'Vision', 'Mission',
            'EJARI', 'Mechanisms', 'Training', 'Users', 'Companies'
        ]
        
        return (len(text) < 100 and 
                any(indicator in text for indicator in title_indicators) and
                not text.endswith('.'))
    
    def _create_chunks(self, content: str, section_title: str) -> List[Dict[str, str]]:
        """Create appropriately sized chunks from section content."""
        chunks = []
        
        # If content is small enough, return as single chunk
        if len(content) <= self.max_chunk_size:
            if len(content) >= self.min_chunk_size:
                chunks.append({
                    'content': content.strip(),
                    'context': section_title,
                    'type': self._determine_content_type(content)
                })
            return chunks
        
        # Split longer content into smaller chunks
        sentences = re.split(r'(?<=[.!?])\s+', content)
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed max size, save current chunk
            if len(current_chunk + sentence) > self.max_chunk_size and len(current_chunk) >= self.min_chunk_size:
                chunks.append({
                    'content': current_chunk.strip(),
                    'context': section_title,
                    'type': self._determine_content_type(current_chunk)
                })
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add remaining content as final chunk
        if len(current_chunk.strip()) >= self.min_chunk_size:
            chunks.append({
                'content': current_chunk.strip(),
                'context': section_title,
                'type': self._determine_content_type(current_chunk)
            })
        
        return chunks
    
    def _determine_content_type(self, content: str) -> str:
        """Determine the type of content for better categorization."""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['required documents', 'copy of', 'passport', 'license']):
            return 'requirements'
        elif any(word in content_lower for word in ['step', 'process', 'procedure', 'how to']):
            return 'procedure'
        elif any(word in content_lower for word in ['definition', 'means', 'refers to', 'is defined as']):
            return 'definition'
        elif any(word in content_lower for word in ['percentage', 'rate', 'fee', 'amount', 'aed']):
            return 'pricing'
        elif any(word in content_lower for word in ['law', 'article', 'decree', 'regulation']):
            return 'legal'
        else:
            return 'general'

    def get_stats(self, chunks: List[Dict[str, str]]) -> Dict[str, int]:
        """Get statistics about the parsed chunks."""
        if not chunks:
            return {}
        
        stats = {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(len(chunk['content']) for chunk in chunks) // len(chunks),
            'types': {}
        }
        
        for chunk in chunks:
            chunk_type = chunk['type']
            stats['types'][chunk_type] = stats['types'].get(chunk_type, 0) + 1
        
        return stats