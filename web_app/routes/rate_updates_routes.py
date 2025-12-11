# web_app/routes/rate_updates_routes.py

import base64
from flask import Blueprint, render_template
from app.collect_FRED_data import collect_FRED_data

rate_updates_routes = Blueprint("rate_updates_routes", __name__)

@rate_updates_routes.route("/rate_updates")
def rate_updates():

    try:
        (
            onrrp_val,
            effr_val,
            iorb_val,
            sofr_val,
            srf_val,
            svg_bytes,
            _effr_date,
            _effr_label,
        ) = collect_FRED_data()

        chart_base64 = base64.b64encode(svg_bytes).decode("utf-8")

    except Exception as e:
        print("Error collecting FRED data:", e)
        chart_base64 = None
        onrrp_val = effr_val = iorb_val = sofr_val = srf_val = None

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
