# app/web_app/routes/home_routes.py

import base64
import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.collect_FRED_data import collect_FRED_data
from app.send_emails import send_email

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def home():
    """
    Home page:
    - Shows a quick headline rate (using EFFR as the main one).
    """
    try:
        (
            _onrrp_today,
            effr_today,
            _iorb_today,
            _sofr_today,
            _srf_today,
            _png_bytes,
        ) = collect_FRED_data()

        current_rate = effr_today
        last_updated = datetime.date.today().strftime("%Y-%m-%d")
    except Exception as e:
        print("No FRED data for available today:", e)
        current_rate = None
        last_updated = None

    return render_template(
        "home.html",
        active_page="home",
        current_rate=current_rate,
        last_updated=last_updated,
    )


@home_routes.route("/rate_updates")
def rate_updates():
    """
    Rates page:
    - Calls collect_FRED_data()
    - Shows today's values for each rate
    - Embeds the PNG chart returned by collect_FRED_data()
    """
    try:
        (
            onrrp_today,
            effr_today,
            iorb_today,
            sofr_today,
            srf_today,
            png_bytes,
        ) = collect_FRED_data()

        chart_base64 = base64.b64encode(png_bytes).decode("utf-8")
    except Exception as e:
        print("Error collecting FRED data for rate updates:", e)
        onrrp_today = effr_today = iorb_today = sofr_today = srf_today = None
        chart_base64 = None

    return render_template(
        "rate_updates.html",      # make sure this file exists
        active_page="rate_updates",
        onrrp_today=onrrp_today,
        effr_today=effr_today,
        iorb_today=iorb_today,
        sofr_today=sofr_today,
        srf_today=srf_today,
        chart_base64=chart_base64,
    )


@home_routes.route("/about")
def about():
    return render_template("about.html", active_page="about")


@home_routes.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    """
    Subscribe page:
    - GET: show the form
    - POST: take email + frequency, call collect_FRED_data(), then send_email()
    """
    if request.method == "POST":
        email = request.form.get("email")
        frequency = request.form.get("frequency", "daily")  # you can log/use this later

        if not email:
            flash("Please enter a valid email address.", "warning")
            return redirect(url_for("home_routes.subscribe"))

        try:
            (
                onrrp_today,
                effr_today,
                iorb_today,
                sofr_today,
                srf_today,
                png_bytes,
            ) = collect_FRED_data()

            send_email(
                recipient_address=email,
                onrrp_today=onrrp_today,
                effr_today=effr_today,
                iorb_today=iorb_today,
                sofr_today=sofr_today,
                srf_today=srf_today,
                png_bytes=png_bytes,
                subject="Your Fed Rate Update",
            )

            flash(
                "You’ve been subscribed! Check your inbox for today’s update.",
                "success",
            )
        except Exception as e:
            print("Error subscribing user / sending email:", e)
            flash(
                "Something went wrong while sending your email. Please try again.",
                "danger",
            )

        # PRG pattern: redirect after POST
        return redirect(url_for("home_routes.subscribe"))

    return render_template("subscribe.html", active_page="subscribe")


@home_routes.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    """
    Unsubscribe page:
    - Right now this is a stub (no real storage to remove from).
    - Later you can hook this into Mailgun lists or your own storage.
    """
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            flash("Please enter the email address you subscribed with.", "warning")
            return redirect(url_for("home_routes.unsubscribe"))

        # TODO: actually remove from whatever subscriber store you end up using.
        flash(
            f"If {email} is on our list, it will be removed from future mailings.",
            "info",
        )
        return redirect(url_for("home_routes.unsubscribe"))

    return render_template("unsubscribe.html", active_page="unsubscribe")


@home_routes.route("/about-us")
def about_us():
    return render_template("about_us.html", active_page="about_us")
