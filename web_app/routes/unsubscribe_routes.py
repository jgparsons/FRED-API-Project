from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.send_emails import unsubscribe_email

unsubscribe_routes = Blueprint("unsubscribe_routes", __name__)


@unsubscribe_routes.route("/unsubscribe", methods=["GET", "POST"])
def unsubscribe():
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            flash("Please enter the email address you subscribed with.", "warning")
            return redirect(url_for("unsubscribe_routes.unsubscribe"))

        success = unsubscribe_email(email)

        if success:
            flash(
                f"{email} has been unsubscribed and will no longer receive mailings.",
                "info",
            )
        else:
            flash(
                "Something went wrong contacting the email service. Please try again later.",
                "danger",
            )

        return redirect(url_for("unsubscribe_routes.unsubscribe"))

    return render_template("unsubscribe.html", active_page="unsubscribe")
