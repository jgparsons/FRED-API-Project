from app.send_emails import MAILGUN_API_KEY

def test_mailgun_api_key_exists_or_none():
    # Local: key is a non-empty string
    # CI: key is None
    assert MAILGUN_API_KEY is None or MAILGUN_API_KEY.strip() != ""

