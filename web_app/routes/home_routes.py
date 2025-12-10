# app/web_app/routes/home_routes.py

import datetime

from flask import Blueprint, render_template

from app.collect_FRED_data import collect_FRED_data

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def home():
    """
    Home page:
    - Shows a quick headline rate (using EFFR as the main one).
    """
    try:
        (
            _onrrp_val,
            effr_val,
            _iorb_val,
            _sofr_val,
            _srf_val,
            _png_bytes,
            effr_date,
            effr_label,
        ) = collect_FRED_data()

        current_rate = effr_val
        last_updated = (
            effr_date.strftime("%Y-%m-%d") if effr_date is not None else None
        )
    except Exception as e:
        print("No FRED data available:", e)
        current_rate = None
        last_updated = None
        effr_label = None

    return render_template(
        "home.html",
        active_page="home",
        current_rate=current_rate,
        last_updated=last_updated,
        effr_label=effr_label,
    )


@home_routes.route("/about")
def about():
    return render_template("about.html", active_page="about")


@home_routes.route("/about-us")
def about_us():
    return render_template("about_us.html", active_page="about_us")
