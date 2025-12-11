from flask import Blueprint, render_template, request, redirect, url_for, flash

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
            # Add to mailing list
            subscribe_email(email)

            # Collect rates (8 values returned now)
            (
                onrrp_today,
                effr_today,
                iorb_today,
                sofr_today,
                srf_today,
                _svg_bytes,   # ignored
                _effr_date,
                _effr_label,
            ) = collect_FRED_data()

            # Send simple text email (no chart)
            send_email(
                recipient_address=email,
                onrrp_today=onrrp_today,
                effr_today=effr_today,
                iorb_today=iorb_today,
                sofr_today=sofr_today,
                srf_today=srf_today,
                subject="Your Fed Rate Update",
            )

            flash("You’ve been subscribed! Check your inbox for today’s update.", "success")

        except Exception as e:
            print("Error subscribing user / sending email:", e)
            flash(
                "Something went wrong while sending your email. Please try again.",
                "danger",
            )

        return redirect(url_for("subscribe_routes.subscribe"))

    return render_template("subscribe.html", active_page="subscribe")
