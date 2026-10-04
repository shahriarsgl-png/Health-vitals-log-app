import os
from datetime import datetime, timezone

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Render provides DATABASE_URL; locally we fall back to SQLite.
db_url = os.environ.get("DATABASE_URL", "sqlite:///vitals.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)   # bpm
    temperature = db.Column(db.Float, nullable=False)    # degrees Celsius
    spo2 = db.Column(db.Integer, nullable=False)         # percent
    recorded_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    readings = Reading.query.order_by(Reading.recorded_at.desc()).all()
    return render_template("index.html", readings=readings)


@app.route("/add", methods=["POST"])
def add():
    reading = Reading(
        patient_name=request.form["patient_name"],
        heart_rate=int(request.form["heart_rate"]),
        temperature=float(request.form["temperature"]),
        spo2=int(request.form["spo2"]),
    )
    db.session.add(reading)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    reading = db.get_or_404(Reading, id)
    if request.method == "POST":
        reading.patient_name = request.form["patient_name"]
        reading.heart_rate = int(request.form["heart_rate"])
        reading.temperature = float(request.form["temperature"])
        reading.spo2 = int(request.form["spo2"])
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", r=reading)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    reading = db.get_or_404(Reading, id)
    db.session.delete(reading)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
