# app/send_emails.py

import os
import requests

MAILGUN_SENDER_ADDRESS = os.getenv("MAILGUN_SENDER_ADDRESS")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILING_LIST = os.getenv("MAILING_LIST")


# -------------------------
# SEND EMAIL TO ONE USER
# -------------------------
def send_email(
    *,
    recipient_address,
    onrrp_today,
    effr_today,
    iorb_today,
    sofr_today,
    srf_today,
    svg_bytes,
    subject="Fed Email",
):
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
        <img src="cid:chart.svg" alt="Fed Chart" />
        <p>Thank you!</p>
    """

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    message_data = {
        "from": MAILGUN_SENDER_ADDRESS,
        "to": recipient_address,
        "subject": subject,
        "html": html_content,
    }

    response = requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data=message_data,
        files={"inline": ("chart.svg", svg_bytes)},
    )

    response.raise_for_status()
    print("Email sent successfully!")


# -------------------------
# SUBSCRIBE TO MAILING LIST
# -------------------------
def subscribe_email(email_address):
    url = f"https://api.mailgun.net/v3/lists/{MAILING_LIST}/members"

    payload = {
        "address": email_address,
        "subscribed": True,
        "upsert": True,
    }

    response = requests.post(url, auth=("api", MAILGUN_API_KEY), data=payload)
    response.raise_for_status()
    return True


# -------------------------
# UNSUBSCRIBE FROM MAILING LIST
# -------------------------
def unsubscribe_email(recipient_address):

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/unsubscribes"

    try:
        response = requests.post(
            url,
            auth=("api", MAILGUN_API_KEY),
            data={"address": recipient_address},
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print("Error unsubscribing:", e)
        return False


# -------------------------
# SEND TO MAILING LIST
# -------------------------
def send_email_to_list(
    *,
    mailing_list_address,
    onrrp_today,
    effr_today,
    iorb_today,
    sofr_today,
    srf_today,
    svg_bytes,
    subject="Fed Email",
):

    html_content = f"""
        <p>Here are yesterday's rates:</p>
        <ul>
            <li>ON_RRP: {onrrp_today}</li>
            <li>EFFR: {effr_today}</li>
            <li>IORB: {iorb_today}</li>
            <li>SOFR: {sofr_today}</li>
            <li>SRF: {srf_today}</li>
        </ul>
        <img src="cid:chart.svg" alt="Fed Chart" />
    """

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    response = requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_SENDER_ADDRESS,
            "to": mailing_list_address,
            "subject": subject,
            "html": html_content,
        },
        files={"inline": ("chart.svg", svg_bytes)},
    )

    response.raise_for_status()
    print("Sent email to mailing list.")
