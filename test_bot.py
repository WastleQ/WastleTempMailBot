from email_parser import clean_html_to_text, extract_links, extract_verification_codes
from locales import get_text


def test_locales():
    ru_welcome = get_text("ru", "welcome")
    en_welcome = get_text("en", "welcome")
    assert "WastleTempMailBot" in ru_welcome
    assert "WastleTempMailBot" in en_welcome

def test_locales_fallback():
    text = get_text("unknown_lang", "welcome")
    assert "WastleTempMailBot" in text

def test_email_parser():
    html = "<p>Your verification code is <b>849201</b>. Click <a href='https://aniliberty.top/verify?token=abc'>here</a> to verify.</p>"
    text = "Plain text fallback 849201"
    
    codes = extract_verification_codes(text)
    assert "849201" in codes
    
    links = extract_links(html, text)
    assert "https://aniliberty.top/verify?token=abc" in links
    
    cleaned = clean_html_to_text(html)
    assert "Your verification code is 849201" in cleaned

