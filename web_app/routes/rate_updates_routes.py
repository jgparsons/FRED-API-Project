@home_routes.route("/rates")
def rates():
    # call data function
    (
        onrrp_today,
        effr_today,
        iorb_today,
        sofr_today,
        srf_today,
        png_bytes,
    ) = collect_FRED_data()

    # turn the PNG into base64 so we can embed it in HTML
    chart_base64 = base64.b64encode(png_bytes).decode("utf-8")

    return render_template(
        "rates.html",          # or "rate_updates.html" if you prefer
        active_page="rates",
        onrrp_today=onrrp_today,
        effr_today=effr_today,
        iorb_today=iorb_today,
        sofr_today=sofr_today,
        srf_today=srf_today,
        chart_base64=chart_base64,
    )
