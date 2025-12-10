from unittest.mock import patch

from app.send_emails import send_email, unsubscribe_email


@patch("app.send_emails.requests.post")
def test_send_email_success(mock_post):
    # Arrange — mock what Mailgun would return
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status.return_value = None

    # Fake values to pass into send_email()
    fake_png = b"12345"

    # Act — call the function
    send_email(
        recipient_address="test@example.com",
        onrrp_today=5.0,
        effr_today=5.1,
        iorb_today=5.2,
        sofr_today=5.3,
        srf_today=5.4,
        png_bytes=fake_png,
        subject="Test Email",
    )

    # Assert — ensure a POST request was made exactly once
    assert mock_post.called
    mock_post.assert_called_once()

    # Get the arguments actually sent to Mailgun
    args, kwargs = mock_post.call_args

    # Assert correct endpoint was used
    assert "https://api.mailgun.net/v3/" in args[0]

    # Assert auth, data, and file payload existence
    assert "auth" in kwargs
    assert "data" in kwargs
    assert "files" in kwargs

    # Assert inline image is passed correctly
    assert "inline" in kwargs["files"]


@patch("app.send_emails.requests.post")
def test_unsubscribe_email_success(mock_post):
    """
    unsubscribe_email should return True when Mailgun responds successfully.
    """
    mock_post.return_value.status_code = 200
    mock_post.return_value.raise_for_status.return_value = None

    result = unsubscribe_email("test@example.com")

    assert result is True
    mock_post.assert_called_once()


@patch("app.send_emails.requests.post")
def test_unsubscribe_email_failure(mock_post):
    """
    unsubscribe_email should return False when Mailgun raises an error.
    """
    mock_post.return_value.status_code = 400
    mock_post.return_value.raise_for_status.side_effect = Exception("API error")

    result = unsubscribe_email("test@example.com")

    assert result is False
    mock_post.assert_called_once()
