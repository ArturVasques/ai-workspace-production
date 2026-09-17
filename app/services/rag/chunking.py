"""
Text chunking for document ingestion.

Documents are divided into overlapping chunks before embeddings are created.
Overlap helps preserve context around chunk boundaries.

Used by:
- document ingestion service before embedding generation.

A production system may later replace this implementation with
token-aware or document-format-aware chunking without affecting repositories
or agents.
"""


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[str]:
    """Split text into bounded overlapping chunks."""

    normalized = " ".join(text.split())

    if not normalized:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0

    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunk = normalized[start:end]

        # Avoid cutting a word when a nearby whitespace boundary exists.
        if end < len(normalized):
            last_space = chunk.rfind(" ")

            if last_space > chunk_size // 2:
                end = start + last_space
                chunk = normalized[start:end]

        chunks.append(chunk.strip())

        if end >= len(normalized):
            break

        start = end - overlap

    return chunks