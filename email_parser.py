"""Email parsing utilities for extracting codes, links, and cleaning HTML content."""

import re


def extract_verification_codes(text: str) -> list[str]:
    """Extract 4 to 6 digit verification codes from text."""
    pattern = r'\b\d{4,6}\b'
    matches = re.findall(pattern, text)
    seen = set()
    unique_codes = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            unique_codes.append(m)
    return unique_codes

def extract_links(html_content: str, text_content: str) -> list[str]:
    """Extract valid http/https links from message body, ignoring common trackers."""
    combined = f"{html_content} {text_content}"
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    found = re.findall(url_pattern, combined)
    
    cleaned_links = []
    ignored_domains = [
        "w3.org", "schema.org", "gravatar.com", "facebook.com", 
        "twitter.com", "instagram.com", "apple.com", "google.com"
    ]
    
    for link in found:
        link = link.rstrip(".,;:)'\"]")
        if not any(dom in link for dom in ignored_domains) and link not in cleaned_links:
            cleaned_links.append(link)
                
    return cleaned_links

def clean_html_to_text(html_list: list[str] | str) -> str:
    """Convert HTML email body to clean readable plain text."""
    if isinstance(html_list, list):
        html_str = "".join(html_list)
    else:
        html_str = html_list or ""
        
    clean = re.sub('<.*?>', ' ', html_str)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean
