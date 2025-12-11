# app/collect_FRED_data.py

import os
import requests
import datetime
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")

onrrp_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=RRPONTSYAWARD&api_key={FRED_API_KEY}&file_type=json"
effr_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=EFFR&api_key={FRED_API_KEY}&file_type=json"
iorb_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=IORB&api_key={FRED_API_KEY}&file_type=json"
sofr_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=SOFR&api_key={FRED_API_KEY}&file_type=json"
srf_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=SRFTSYD&api_key={FRED_API_KEY}&file_type=json"


def collect_FRED_data():

    print("DEBUG_FRED_KEY:", repr(os.getenv("FRED_API_KEY")))

    today = datetime.date.today()

    # ------------------------
    # Fetch all 5 rate series
    # ------------------------
    onrrp_data = requests.get(onrrp_url).json()
    effr_data = requests.get(effr_url).json()
    iorb_data = requests.get(iorb_url).json()
    sofr_data = requests.get(sofr_url).json()
    srf_data = requests.get(srf_url).json()

    # --------------------------------
    # Extract most recent non-missing
    # --------------------------------
    def extract_latest(json_data):
        latest_value = None
        latest_date = None

        for obs in json_data["observations"]:
            if obs["value"] == ".":
                continue
            date_obj = datetime.datetime.strptime(obs["date"], "%Y-%m-%d").date()
            value = float(obs["value"])
            latest_value = value
            latest_date = date_obj

        if latest_value is None:
            return None, None, None

        label = "Today's value" if latest_date == today else "Latest value"
        return latest_value, latest_date, label

    onrrp_val, _, _ = extract_latest(onrrp_data)
    effr_val, effr_date, effr_label = extract_latest(effr_data)
    iorb_val, _, _ = extract_latest(iorb_data)
    sofr_val, _, _ = extract_latest(sofr_data)
    srf_val, _, _ = extract_latest(srf_data)

    # --------------------------------
    # Last 30-day history (excluding today)
    # --------------------------------
    def extract_last_30_days(json_data, col_name):
        rows = []
        thirty_days_ago = today - datetime.timedelta(days=30)

        for obs in json_data["observations"]:
            date = datetime.datetime.strptime(obs["date"], "%Y-%m-%d").date()
            if thirty_days_ago <= date < today:
                value = float(obs["value"]) if obs["value"] != "." else None
                rows.append({"date": date, col_name: value})

        df = pd.DataFrame(rows)
        return df.set_index("date")

    df_all = pd.concat(
        [
            extract_last_30_days(onrrp_data, "ON_RRP"),
            extract_last_30_days(effr_data, "EFFR"),
            extract_last_30_days(iorb_data, "IORB"),
            extract_last_30_days(sofr_data, "SOFR"),
            extract_last_30_days(srf_data, "SRF"),
        ],
        axis=1,
    )

    df_all = df_all.sort_index().dropna(thresh=len(df_all.columns) - 1)

    # ------------------------
    # Plot and convert to SVG
    # ------------------------
    fig = px.line(df_all)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        legend_title="Series",
    )

    svg_bytes = fig.to_image(format="svg")
    svg_bytes = svg_text.encode("utf-8") # bytes for email attachment

    return (
        onrrp_val,
        effr_val,
        iorb_val,
        sofr_val,
        srf_val,
        svg_bytes,
        effr_date,
        effr_label,
    )
