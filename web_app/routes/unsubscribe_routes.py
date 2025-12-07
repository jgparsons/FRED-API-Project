@home_routes.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    if request.method == "POST":
        email = request.form["email"]

        # TODO: actually remove this email from your subscriber store or Mailgun list
        # For now, just pretend and flash a message:
        flash(f"If {email} was on our list, it will be removed from future mailings.", "info")

        return redirect(url_for("home_routes.unsubscribe"))

    return render_template("unsubscribe.html", active_page="unsubscribe")
