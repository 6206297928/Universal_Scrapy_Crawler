"""
Universal Content Chunker
Production-grade chunking for AI retrieval systems

Features:
- Smart paragraph splitting
- Token-safe chunk sizes
- Overlap support
- Metadata preservation
- Clean output for vector DB
"""

import re
from typing import List, Dict


class ContentChunker:

    def __init__(
        self,
        chunk_size: int = 800,
        overlap: int = 100,
        min_chunk_size: int = 100
    ):
        """
        chunk_size: max characters per chunk
        overlap: characters overlapping between chunks
        min_chunk_size: minimum useful chunk
        """

        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size


    # -----------------------------
    # Clean text before chunking
    # -----------------------------
    def clean_text(self, text: str) -> str:

        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove weird symbols
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)

        return text.strip()


    # -----------------------------
    # Split into paragraphs first
    # -----------------------------
    def split_paragraphs(self, text: str) -> List[str]:

        paragraphs = re.split(r'\.\s+', text)

        clean_paragraphs = []

        for p in paragraphs:
            p = p.strip()

            if len(p) >= self.min_chunk_size:
                clean_paragraphs.append(p + ".")

        return clean_paragraphs


    # -----------------------------
    # Create chunks with overlap
    # -----------------------------
    def chunk_text(self, text: str) -> List[str]:

        text = self.clean_text(text)

        if len(text) <= self.chunk_size:
            return [text]

        paragraphs = self.split_paragraphs(text)

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:

            if len(current_chunk) + len(paragraph) <= self.chunk_size:

                current_chunk += " " + paragraph

            else:

                chunks.append(current_chunk.strip())

                # overlap
                overlap_text = current_chunk[-self.overlap:]

                current_chunk = overlap_text + " " + paragraph

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks


    # -----------------------------
    # Create structured output
    # -----------------------------
    def chunk_document(
        self,
        url: str,
        title: str,
        content: str,
        domain: str = None
    ) -> List[Dict]:

        chunks = self.chunk_text(content)

        structured_chunks = []

        for i, chunk in enumerate(chunks):

            structured_chunks.append({

                "url": url,

                "domain": domain,

                "title": title,

                "chunk_id": i,

                "text": chunk,

                "length": len(chunk)

            })

        return structured_chunks
