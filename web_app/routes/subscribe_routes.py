@home_routes.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    if request.method == "POST":
        email = request.form["email"]
        frequency = request.form.get("frequency", "daily")  # if you have this field

        # get today’s data + chart
        (
            onrrp_today,
            effr_today,
            iorb_today,
            sofr_today,
            srf_today,
            png_bytes,
        ) = collect_FRED_data()

        try:
            # send the email using your helper
            send_email(
                recipient_address=email,
                onrrp_today=onrrp_today,
                effr_today=effr_today,
                iorb_today=iorb_today,
                sofr_today=sofr_today,
                srf_today=srf_today,
                png_bytes=png_bytes,
                subject="Your Fed rate update",
            )
            flash("You’ve been subscribed! Check your inbox for today’s update.", "success")
        except Exception as e:
            print("Error sending email:", e)
            flash("Something went wrong sending your email. Please try again.", "danger")

        # redirect so refresh doesn’t resubmit the form
        return redirect(url_for("home_routes.subscribe"))

    return render_template("subscribe.html", active_page="subscribe")
