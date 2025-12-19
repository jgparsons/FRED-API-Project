# app/main.py

import os
import datetime
from app.collect_FRED_data import collect_FRED_data
from app.send_emails import send_email_to_list

MAILING_LIST = os.getenv("MAILING_LIST")

# used for running daily email
# this is prompted by a Render cron job
def main():
    print("Running daily email job...")

    try:
        (
            onrrp,
            effr,
            iorb,
            sofr,
            srf,
            _svg_bytes,   # unused now
            _effr_date,
            _effr_label,
        ) = collect_FRED_data()

        send_email_to_list(
            mailing_list_address=MAILING_LIST,
            onrrp_today=onrrp,
            effr_today=effr,
            iorb_today=iorb,
            sofr_today=sofr,
            srf_today=srf,
            subject="Daily Fed Rate Update",
        )

        print("Daily rate email sent successfully!")
    except Exception as e:
        print("ERROR running daily email job:", e)


if __name__ == "__main__":
    main()
