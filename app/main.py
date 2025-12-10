from app.collect_FRED_data import collect_FRED_data
from app.send_emails import send_email_to_list
import os
import datetime

MAILING_LIST = os.getenv("MAILING_LIST")

def main():
    today = datetime.date.today()
    if today.datetime.weekday < 5:
        (
            onrrp_today,
            effr_today,
            iorb_today,
            sofr_today,
            srf_today,
            png_bytes
        ) = collect_FRED_data()

        send_email_to_list(
            mailing_list_address="MAILING_LIST",
            onrrp_today=onrrp_today,
            effr_today=effr_today,
            iorb_today=iorb_today,
            sofr_today=sofr_today,
            srf_today=srf_today,
            png_bytes=png_bytes,
            subject="Daily Fed Rate Update"
        )

if __name__ == "__main__":
    main()

