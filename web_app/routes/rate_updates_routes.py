# web_app/routes/rate_updates_routes.py

from flask import Blueprint, render_template
from app.collect_FRED_data import collect_FRED_data

rate_updates_routes = Blueprint("rate_updates_routes", __name__)


@rate_updates_routes.route("/rate_updates")
def rate_updates():
    """
    Rates page:
    - Calls collect_FRED_data()
    - Shows today's/latest values for each rate
    - Passes 30-day chart_data to frontend which uses Plotly.js
    """

    try:
        (
            onrrp_val,
            effr_val,
            iorb_val,
            sofr_val,
            srf_val,
            chart_data,
            _effr_date,   # unused here, but available
            _effr_label,  # unused here
        ) = collect_FRED_data()

    except Exception as e:
        print("Error collecting FRED data for /rate_updates:", e)
        onrrp_val = effr_val = iorb_val = sofr_val = srf_val = None
        chart_data = None

    return render_template(
        "rate_updates.html",
        active_page="rate_updates",
        onrrp_today=onrrp_val,
        effr_today=effr_val,
        iorb_today=iorb_val,
        sofr_today=sofr_val,
        srf_today=srf_val,
        chart_data=chart_data,
    )
