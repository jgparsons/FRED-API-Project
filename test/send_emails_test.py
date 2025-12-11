from unittest.mock import patch
from app.send_emails import send_email, unsubscribe_email


@patch("app.send_emails.requests.post")
def test_send_email_success(mock_post):
    # Arrange — mock what Mailgun would return
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status.return_value = None

    fake_svg = b"12345"

    # Act — call the function
    send_email(
        recipient_address="test@example.com",
        onrrp_today=5.0,
        effr_today=5.1,
        iorb_today=5.2,
        sofr_today=5.3,
        srf_today=5.4,
        svg_bytes=fake_svg,
        subject="Test Email",
    )

    # Assert — Mailgun POST called exactly once
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args

    assert "https://api.mailgun.net/v3/" in args[0]
    assert "auth" in kwargs
    assert "data" in kwargs
    assert "files" in kwargs

    # Assert inline SVG attachment
    assert "inline" in kwargs["files"]
    filename, content = kwargs["files"]["inline"]
    assert filename.endswith(".svg")
    assert content == fake_svg


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
