from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import select
from database.db import db
import json
import bin.scanning as s
from flask_login import current_user, login_required

from database.models import Scan

scanRoutes = Blueprint("scanRoutes", __name__)

@scanRoutes.route("/scan", methods=["GET", "POST"])
@login_required
def scan():

    if request.method == "POST":

        url = request.form.get('url')

        if not url:
            return render_template("scan.html")
        
        if not url.startswith("https"):
           url = "https://" + url

        cookies = s.scanning(url)
        cookies_a_r = s.scanAfterReject(url)

        # gen AI
        scan_result = {
            "cookies_b_c": cookies[0],
            "cookies_a_c": cookies[1],
            "privacy_policy": cookies[2],
            "security_headers": cookies[3],
            "cookies_a_r": cookies_a_r[0],
            "reject_button": cookies_a_r[1],
        }

        scores = []

        for name, data in cookies[0].items():
            scores.append(data["score"])     

        for name, data in cookies[1].items():
            scores.append(data["score"])
        
        for name, data in cookies_a_r[0].items():
            scores.append(data["score"])

        new_scan = Scan(
            user_id = current_user.id,
            url = url,
            average_score = sum(scores) / scores.__len__() if scores else 1, 
            result = json.dumps(scan_result)  # gen AI
        )

        db.session.add(new_scan)
        db.session.commit()

        return render_template("results.html", 
                               cookies_b_c=cookies[0], 
                               cookies_a_c=cookies[1], 
                               privacy=cookies[2], 
                               security_headers = cookies[3], 
                               cookies_a_r=cookies_a_r[0],
                               reject_button=cookies_a_r[1]
                               )

    return render_template("scan.html")

@scanRoutes.route("/results/<int:scan_id>")
@login_required
def results(scan_id):

    if not scan_id:
        return render_template("results.html")

    scan = db.session.execute(select(Scan).where(Scan.id == scan_id)).scalar_one_or_none()
    scan_results = json.loads(scan.result)

    return render_template("results.html", 
                           cookies_b_c=scan_results["cookies_b_c"], 
                           cookies_a_c=scan_results["cookies_a_c"], 
                           privacy=scan_results["privacy_policy"], 
                           security_headers=scan_results["security_headers"],
                           cookies_a_r=scan_results["cookies_a_r"],
                           reject_button=scan_results["reject_button"])

@scanRoutes.route("/history")
@login_required
def history():

    scans = db.session.execute(select(Scan).where(current_user.id == Scan.user_id)).scalars().all().__reversed__()

    return render_template("history.html", scans=scans)

@scanRoutes.route("/delete/<int:scan_id>")
@login_required
def delete(scan_id):

    scan = db.session.execute(select(Scan).where(Scan.id == scan_id)).scalar_one_or_none()

    db.session.delete(scan)
    db.session.commit()

    return redirect(url_for("scanRoutes.history"))