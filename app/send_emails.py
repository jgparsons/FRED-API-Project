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
    <html>
    <body style="
        margin:0;
        padding:0;
        background-color:#0a102c;
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
        color:#f9fafb;
    ">
      <table width="100%" cellpadding="0" cellspacing="0" style="padding:32px 0;">
        <tr>
          <td align="center">
            <table width="520" cellpadding="0" cellspacing="0" style="
              background-color:#0b1536;
              border:1px solid #1a2642;
              border-radius:10px;
              padding:28px;
            ">
              <tr>
                <td style="padding-bottom:18px;">
                  <h2 style="margin:0;color:#e5e7eb;">📈 Fed Rate Watch</h2>
                  <p style="margin:6px 0 0;color:#c6dcf6;font-size:14px;">
                    Yesterday’s published rates
                  </p>
                </td>
              </tr>

              <tr><td>{rate_row("ON RRP", onrrp_today)}</td></tr>
              <tr><td>{rate_row("EFFR", effr_today)}</td></tr>
              <tr><td>{rate_row("IORB", iorb_today)}</td></tr>
              <tr><td>{rate_row("SOFR", sofr_today)}</td></tr>
              <tr><td>{rate_row("SRF", srf_today)}</td></tr>

              <tr>
                <td style="padding-top:22px;font-size:13px;color:#9ca3af;">
                  You’re receiving this because you subscribed to Fed Rate Watch.
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    response = requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_SENDER_ADDRESS,
            "to": recipient_address,
            "subject": subject,
            "html": html_content,
        },
    )
    response.raise_for_status()
    print("Email sent successfully!")


def rate_row(label, value):
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
      <tr>
        <td style="padding:10px 0;color:#c6dcf6;font-size:14px;">
          {label}
        </td>
        <td align="right" style="padding:10px 0;color:#f9fafb;font-weight:600;">
          {value}
        </td>
      </tr>
      <tr>
        <td colspan="2" style="border-bottom:1px solid #1a2642;"></td>
      </tr>
    </table>
    """


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
        unsub_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/unsubscribes"

        response = requests.post(
            unsub_url,
            auth=("api", MAILGUN_API_KEY),
            data={"address": email_address},
        )

        response.raise_for_status()
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
    <html>
    <body style="
        margin:0;
        padding:0;
        background-color:#0a102c;
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
        color:#f9fafb;
    ">
      <table width="100%" cellpadding="0" cellspacing="0" style="padding:32px 0;">
        <tr>
          <td align="center">
            <table width="520" cellpadding="0" cellspacing="0" style="
              background-color:#0b1536;
              border:1px solid #1a2642;
              border-radius:10px;
              padding:28px;
            ">
              <tr>
                <td style="padding-bottom:18px;">
                  <h2 style="margin:0;color:#e5e7eb;">📈 Fed Rate Watch</h2>
                  <p style="margin:6px 0 0;color:#c6dcf6;font-size:14px;">
                    Yesterday’s published rates
                  </p>
                </td>
              </tr>

              <tr><td>{rate_row("ON RRP", onrrp_today)}</td></tr>
              <tr><td>{rate_row("EFFR", effr_today)}</td></tr>
              <tr><td>{rate_row("IORB", iorb_today)}</td></tr>
              <tr><td>{rate_row("SOFR", sofr_today)}</td></tr>
              <tr><td>{rate_row("SRF", srf_today)}</td></tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
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
