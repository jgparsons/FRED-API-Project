# app/send_emails.py

import os
import requests

MAILGUN_SENDER_ADDRESS = os.getenv("MAILGUN_SENDER_ADDRESS")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILING_LIST = os.getenv("MAILING_LIST")


# -------------------------
# SEND EMAIL TO ONE USER (NO IMAGE)
# -------------------------
def send_email(
    *,
    recipient_address,
    onrrp_today,
    effr_today,
    iorb_today,
    sofr_today,
    srf_today,
    subject="Fed Email",
):
    """
    Send a Fed rate email with yesterday's values to a single recipient.
    No chart image is attached.
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
def unsubscribe_email(email_address):
    try:
        # -------- STEP 1: Remove from mailing list --------
        list_url = f"https://api.mailgun.net/v3/lists/{MAILING_LIST}/members/{email_address}"

        delete_resp = requests.delete(
            list_url,
            auth=("api", MAILGUN_API_KEY)
        )

        # If the user didn't exist in the list, Mailgun returns 404.
        # That is okay. They are effectively unsubscribed.
        if delete_resp.status_code not in (200, 204, 404):
            delete_resp.raise_for_status()

        # -------- STEP 2 (optional but recommended): add to unsubscribes --------
        unsub_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/unsubscribes"

        requests.post(
            unsub_url,
            auth=("api", MAILGUN_API_KEY),
            data={"address": email_address},
        )

        return True

    except Exception as e:
        print("Error unsubscribing:", e)
        return False



# -------------------------
# SEND EMAIL TO ENTIRE MAILING LIST (NO IMAGE)
# -------------------------
def send_email_to_list(
    *,
    mailing_list_address,
    onrrp_today,
    effr_today,
    iorb_today,
    sofr_today,
    srf_today,
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
    )
    response.raise_for_status()
    print("Sent email to mailing list.")
