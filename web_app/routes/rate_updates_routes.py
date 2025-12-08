import base64
import datetime

from flask import Blueprint, render_template

from app.collect_FRED_data import collect_FRED_data

rate_updates_routes = Blueprint("rate_updates_routes", __name__)

@rate_updates_routes.route("/rate_updates")
def rate_updates():
    """
    Rates page:
    - Calls collect_FRED_data()
    - Shows today's/latest values for each rate
    - Embeds the PNG chart returned by collect_FRED_data()
    """
    
    try:
        (
            onrrp_val,
            effr_val,
            iorb_val,
            sofr_val,
            srf_val,
            png_bytes,
            _effr_date,   # unused here, but returned by the function
            _effr_label,  # unused here
        ) = collect_FRED_data()

        chart_base64 = base64.b64encode(png_bytes).decode("utf-8")

    except Exception as e:
        print("Error collecting FRED data for /rate_updates:", e)
        onrrp_val = effr_val = iorb_val = sofr_val = srf_val = None
        chart_base64 = None

    return render_template(
        "rate_updates.html",
        active_page="rate_updates",
        onrrp_today=onrrp_val,
        effr_today=effr_val,
        iorb_today=iorb_val,
        sofr_today=sofr_val,
        srf_today=srf_val,
        chart_base64=chart_base64,
    )
    
   