from app.collect_FRED_data import collect_FRED_data
from app.send_emails import send_emails

def main():
    (
        onrrp_today,
        effr_today,
        iorb_today,
        sofr_today,
        srf_today,
        png_bytes
    ) = collect_FRED_data()

    send_emails(
        recipient_address="jgp67@georgetown.edu",
        onrrp_today=onrrp_today,
        effr_today=effr_today,
        iorb_today=iorb_today,
        sofr_today=sofr_today,
        srf_today=srf_today,
        png_bytes=png_bytes
    )

if __name__ == "__main__":
    main()

