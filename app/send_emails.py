import os
import requests

MAILGUN_SENDER_ADDRESS = os.getenv("MAILGUN_SENDER_ADDRESS")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILING_LIST = os.getenv("MAILING_LIST")


# ---------------------------------------------------------
#  SEND EMAIL TO A SINGLE RECIPIENT
# ---------------------------------------------------------
def send_email(
    *,
    recipient_address,
    onrrp_today,
    effr_today,
    iorb_today,
    sofr_today,
    srf_today,
    png_bytes,
    subject="Fed Email"
):
    """
    Send a Fed rate email with yesterday's values to a single recipient.
    Keyword-only arguments ensure pytest calls succeed.
    """

    html_content = f"""
        <p>Thank you for signing up to receive these fun and interesting emails.</p>
        <p>Here are yesterday's rates:</p>
        <ul>
            <li>ON_RRP: {onrrp_today}</li>
            <li>EFFR: {effr_today}</li>
            <li>IORB: {iorb_today}</li>
            <li>SOFR: {sofr_today}</li>
            <li>SRF: {srf_today}</li>
        </ul>
        <img src="cid:chart.png" alt="Fed Chart" />
        <p>Thank you!</p>
    """

    request_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    message_data = {
        "from": MAILGUN_SENDER_ADDRESS,
        "to": recipient_address,
        "subject": subject,
        "html": html_content,
    }

    try:
        response = requests.post(
            request_url,
            auth=("api", MAILGUN_API_KEY),
            data=message_data,
            files={"inline": ("chart.png", png_bytes)},
        )

        print("RESULT:", response.status_code)
        response.raise_for_status()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

# ---------------------------------------------------------
#  SUBSCRIBE A USER TO THE MAILGUN MAILING LIST
# ---------------------------------------------------------
def subscribe_email(email_address):
    """
    Add a user to the configured Mailgun mailing list.

    Returns:
        True   -> subscription successful
        False  -> any error occurred
    """
    try:
        url = f"https://api.mailgun.net/v3/lists/{MAILING_LIST}/members"

        payload = {
            "address": email_address,
            "subscribed": True,
            "upsert": True,      # avoids duplicates; updates if already exists
        }

        response = requests.post(
            url,
            auth=("api", MAILGUN_API_KEY),
            data=payload,
        )

        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Error subscribing email '{email_address}': {e}")
        return False

# ---------------------------------------------------------
#  UNSUBSCRIBE A USER
# ---------------------------------------------------------
def unsubscribe_email(recipient_address):
    """
    Remove an email from Mailgun unsubscribes.
    """
    try:
        request_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/unsubscribes"

        response = requests.post(
            request_url,
            auth=("api", MAILGUN_API_KEY),
            data={"address": recipient_address},
        )

        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Error unsubscribing: {e}")
        return False


# ---------------------------------------------------------
#  SEND EMAIL TO ENTIRE MAILING LIST
# ---------------------------------------------------------
def send_email_to_list(
    *,
    mailing_list_address,
    onrrp_today,
    effr_today,
    iorb_today,
    sofr_today,
    srf_today,
    png_bytes,
    subject="Fed Email"
):
    """
    Send yesterday's Fed rates to an entire Mailgun mailing list.
    """

    html_content = f"""
        <p>Thank you for signing up to receive these fun and interesting emails.</p>
        <p>Here are yesterday's rates:</p>
        <ul>
            <li>ON_RRP: {onrrp_today}</li>
            <li>EFFR: {effr_today}</li>
            <li>IORB: {iorb_today}</li>
            <li>SOFR: {sofr_today}</li>
            <li>SRF: {srf_today}</li>
        </ul>
        <img src="cid:chart.png" alt="Fed Chart" />
        <p>Thank you!</p>
    """

    request_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    message_data = {
        "from": MAILGUN_SENDER_ADDRESS,
        "to": mailing_list_address,
        "subject": subject,
        "html": html_content,
    }

    try:
        response = requests.post(
            request_url,
            auth=("api", MAILGUN_API_KEY),
            data=message_data,
            files={"inline": ("chart.png", png_bytes)},
        )

        print("RESULT:", response.status_code)
        response.raise_for_status()
        print("Emails sent to entire list successfully!")

    except Exception as e:
        print(f"Error sending list email: {e}")
