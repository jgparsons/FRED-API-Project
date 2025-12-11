# test/send_emails_test.py

from unittest.mock import patch
from app.send_emails import send_email, unsubscribe_email


@patch("app.send_emails.requests.post")
def test_send_email_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status.return_value = None

    send_email(
        recipient_address="test@example.com",
        onrrp_today=5.0,
        effr_today=5.1,
        iorb_today=5.2,
        sofr_today=5.3,
        srf_today=5.4,
        subject="Test Email",
    )

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args

    # Correct endpoint
    assert "https://api.mailgun.net/v3/" in args[0]

    # auth and data present
    assert "auth" in kwargs
    assert "data" in kwargs
    # no files key expected anymore
    assert "files" not in kwargs


@patch("app.send_emails.requests.post")
def test_unsubscribe_email_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status.return_value = None

    result = unsubscribe_email("test@example.com")

    assert result is True
    mock_post.assert_called_once()


@patch("app.send_emails.requests.post")
def test_unsubscribe_email_failure(mock_post):
    mock_post.return_value.status_code = 400
    mock_post.return_value.raise_for_status.side_effect = Exception("API error")

    result = unsubscribe_email("test@example.com")

    assert result is False
    mock_post.assert_called_once()
