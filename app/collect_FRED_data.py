# app/collect_FRED_data.py

import os
import requests
import datetime
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")

# Build URLs for series
onrrp_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=RRPONTSYAWARD&api_key={FRED_API_KEY}&file_type=json"
effr_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=EFFR&api_key={FRED_API_KEY}&file_type=json"
iorb_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=IORB&api_key={FRED_API_KEY}&file_type=json"
sofr_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=SOFR&api_key={FRED_API_KEY}&file_type=json"
srf_url = f"https://api.stlouisfed.org/fred/series/observations?series_id=SRFTSYD&api_key={FRED_API_KEY}&file_type=json"


def collect_FRED_data():
    """Return latest values plus 30-day history for charting (no images)."""

    print("DEBUG_FRED_KEY:", repr(os.getenv("FRED_API_KEY")))

    today = datetime.date.today()

    # Fetch JSON from FRED
    onrrp_data = requests.get(onrrp_url).json()
    effr_data = requests.get(effr_url).json()
    iorb_data = requests.get(iorb_url).json()
    sofr_data = requests.get(sofr_url).json()
    srf_data = requests.get(srf_url).json()

    def extract_latest(json_data):
        latest_value = None
        latest_date = None

        for obs in json_data["observations"]:
            if obs["value"] == ".":
                continue

            date_obj = datetime.datetime.strptime(
                obs["date"], "%Y-%m-%d"
            ).date()
            value = float(obs["value"])

            latest_value = value
            latest_date = date_obj

        if latest_value is None:
            return None, None, None

        label = "Today's value" if latest_date == today else "Latest value"
        return latest_value, latest_date, label

    # Extract each series' latest value
    onrrp_val, _, _ = extract_latest(onrrp_data)
    effr_val, effr_date, effr_label = extract_latest(effr_data)
    iorb_val, _, _ = extract_latest(iorb_data)
    sofr_val, _, _ = extract_latest(sofr_data)
    srf_val, _, _ = extract_latest(srf_data)

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

    # Build dataframe for chart
    df_onrrp = extract_last_30_days(onrrp_data, "ON_RRP")
    df_effr = extract_last_30_days(effr_data, "EFFR")
    df_iorb = extract_last_30_days(iorb_data, "IORB")
    df_sofr = extract_last_30_days(sofr_data, "SOFR")
    df_srf = extract_last_30_days(srf_data, "SRF")

    df_all = pd.concat([df_onrrp, df_effr, df_iorb, df_sofr, df_srf], axis=1)
    df_all.index = pd.to_datetime(df_all.index)
    df_all = df_all.sort_index()
    df_all = df_all.dropna(thresh=len(df_all.columns) - 1)

    # Turn into JSON-serializable dict for frontend Plotly
    df_for_chart = df_all.reset_index()
    df_for_chart["date"] = df_for_chart["date"].dt.strftime("%Y-%m-%d")
    chart_data = df_for_chart.to_dict(orient="list")
    # chart_data keys: ["date", "ON_RRP", "EFFR", "IORB", "SOFR", "SRF"]

    return (
        onrrp_val,
        effr_val,
        iorb_val,
        sofr_val,
        srf_val,
        chart_data,
        effr_date,
        effr_label,
    )
