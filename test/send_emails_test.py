from app.send_emails import MAILGUN_API_KEY

def test_mailgun_api_key_exists():
    assert isinstance(MAILGUN_API_KEY, str)
    assert MAILGUN_API_KEY.strip() != ""
