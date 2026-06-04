from typing import Set

def format_response(text: str, source_urls: Set[str], last_updated: str) -> str:
    """
    Appends a primary citation and a mandatory footer to the LLM response.
    Ensures exactly one primary citation is used, even if multiple chunks came from different URLs.
    """
    if not text.strip():
        return ""
        
    # If the LLM returned the fallback message, do not append source or footer
    if text.strip() == "The requested information is not available in the current knowledge base.":
        return text.strip()

    # We enforce exactly one primary citation link
    primary_citation = ""
    if source_urls:
        # Just grab the first one available
        url = list(source_urls)[0]
        primary_citation = f"\n\nSource: {url}"
        
    # Mandatory footer
    footer = f"\nLast updated from sources: {last_updated}"
    
    return f"{text}{primary_citation}{footer}"
