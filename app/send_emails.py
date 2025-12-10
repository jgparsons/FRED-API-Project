import kaleido
import os
#from os import SPLICE_F_MORE
import requests
import datetime
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dotenv import load_dotenv

MAILGUN_SENDER_ADDRESS = os.getenv("MAILGUN_SENDER_ADDRESS") # "example@georgetown.edu"
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN") # "sandbox-xyz.mailgun.org"
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")

def send_email(
    recipient_address,
    onrrp_today,
    effr_today,
    iorb_today,
    sofr_today,
    srf_today,
    png_bytes,
    subject="Fed Email"
):
    html_content = f"""
        <p>Thank you for signing up to receive these fun and interesting emails.</p>
        <p>Here are today's rates:</p>
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

    try:
        request_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

        message_data = {
            'from': MAILGUN_SENDER_ADDRESS,
            'to': recipient_address,
            'subject': subject,
            'html': html_content,
        }

        response = requests.post(
            request_url,
            auth=("api", MAILGUN_API_KEY),
            data=message_data,
            files={"inline": ("chart.png", png_bytes)}
        )

        print("RESULT:", response.status_code)
        response.raise_for_status()
        print("Email sent successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {str(e)}")

#adding unsubscribe ability?

def unsubscribe_email(recipient_address):
    """
    Remove an email from future mailings via Mailgun's unsubscribe endpoint.

    Returns:
        True  if the API call succeeds,
        False if there is any error.
    """
    try:
        request_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/unsubscribes"

        response = requests.post(
            request_url,
            auth=("api", MAILGUN_API_KEY),
            data={"address": recipient_address},
        )

        print("UNSUBSCRIBE RESULT:", response.status_code)
        response.raise_for_status()
        return True

    except Exception as e:  # catch generic Exception so the test's side_effect works
        print(f"Error unsubscribing: {e}")
        return False
