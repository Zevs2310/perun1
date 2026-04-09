from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder="templates")

# ─── DATABASE ─────────────────────────────
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─── MODELS ───────────────────────────────
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(50))

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ip = db.Column(db.String(50))
    status = db.Column(db.String(50))

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    status = db.Column(db.String(50))
    priority = db.Column(db.String(10))

# ─── INIT DB ──────────────────────────────
with app.app_context():
    db.create_all()

# ─── ROUTE (FRONTEND) ─────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─── USERS API ────────────────────────────
@app.route("/api/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        users = User.query.all()
        return jsonify([{
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        } for u in users])

    if request.method == "POST":
        data = request.json
        user = User(
            name=data["name"],
            email=data["email"],
            role=data["role"]
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "created"})

# ─── DEVICES API ──────────────────────────
@app.route("/api/devices", methods=["GET", "POST"])
def devices():
    if request.method == "GET":
        devices = Device.query.all()
        return jsonify([{
            "id": d.id,
            "name": d.name,
            "ip": d.ip,
            "status": d.status
        } for d in devices])

    if request.method == "POST":
        data = request.json
        device = Device(
            name=data["name"],
            ip=data["ip"],
            status=data["status"]
        )
        db.session.add(device)
        db.session.commit()
        return jsonify({"status": "created"})

# ─── INCIDENTS API ────────────────────────
@app.route("/api/incidents", methods=["GET", "POST"])
def incidents():
    if request.method == "GET":
        incidents = Incident.query.all()
        return jsonify([{
            "id": i.id,
            "title": i.title,
            "status": i.status,
            "priority": i.priority
        } for i in incidents])

    if request.method == "POST":
        data = request.json
        incident = Incident(
            title=data["title"],
            status=data["status"],
            priority=data["priority"]
        )
        db.session.add(incident)
        db.session.commit()
        return jsonify({"status": "created"})

# ─── RUN ──────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
