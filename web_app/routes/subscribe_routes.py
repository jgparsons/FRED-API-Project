
from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from app.collect_FRED_data import collect_FRED_data
from app.send_emails import send_email, subscribe_email

subscribe_routes = Blueprint("subscribe_routes", __name__)

@subscribe_routes.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            flash("Please enter a valid email address.", "warning")
            return redirect(url_for("subscribe_routes.subscribe"))

        try:

            subscribe_email(email)

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

            flash("You’ve been subscribed! Check your inbox for today’s update.",
                  "success")
        except Exception as e:
            print("Error subscribing user / sending email:", e)
            flash(
                "Something went wrong while sending your email. Please try again.",
                "danger",
            )

        return redirect(url_for("subscribe_routes.subscribe"))

    return render_template("subscribe.html", active_page="subscribe")