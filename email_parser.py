import re


def extract_verification_codes(text: str) -> list[str]:
    # Look for 4 to 6 digit numbers, potentially near keywords or standalone
    # We can search for standalone 4-6 digit numbers
    pattern = r'\b\d{4,6}\b'
    matches = re.findall(pattern, text)
    # Remove duplicates while preserving order
    seen = set()
    unique_codes = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            unique_codes.append(m)
    return unique_codes

def extract_links(html_content: str, text_content: str) -> list[str]:
    combined = f"{html_content} {text_content}"
    # Find all http/https URLs
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    found = re.findall(url_pattern, combined)
    
    cleaned_links = []
    ignored_domains = ["w3.org", "schema.org", "gravatar.com", "facebook.com", "twitter.com", "instagram.com", "apple.com", "google.com"]
    
    for link in found:
        # Remove trailing punctuation often captured by regex
        link = link.rstrip(".,;:)'\"]")
        if not any(dom in link for dom in ignored_domains) and link not in cleaned_links:
            cleaned_links.append(link)
                
    return cleaned_links

def clean_html_to_text(html_list: list[str] | str) -> str:
    if isinstance(html_list, list):
        html_str = "".join(html_list)
    else:
        html_str = html_list or ""
        
    # Basic HTML tag stripping
    clean = re.sub('<.*?>', ' ', html_str)
    # Collapse multiple spaces/newlines
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean
