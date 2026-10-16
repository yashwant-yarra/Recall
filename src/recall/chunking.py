def chunk_pages(pages: list[str], size: int = 1000, overlap: int = 150) -> list[tuple[int, str]]:
    """Split pages into overlapping character windows, never across a page break.

    Args:
        pages: Page texts from extract_text().
        size: Maximum characters per chunk.
        overlap: Characters shared by consecutive chunks on the same page.

    Returns:
        (page_no, text) pairs; page_no starts at 1. Blank chunks are dropped.

    Raises:
        ValueError: If overlap is not smaller than size.
    """
    if not 0 <= overlap < size:
        raise ValueError("overlap must be >= 0 and < size")
    step = size - overlap
    chunks = []
    # Number pages before filtering, so a blank page doesn't shift later page numbers.
    for page_no, text in enumerate(pages, start=1):
        # Stop once a window reaches the end; otherwise the last window is a subset of the previous one.
        for start in range(0, max(len(text) - overlap, 1), step):
            piece = text[start:start + size].strip()
            if piece:
                chunks.append((page_no, piece))
    return chunks
