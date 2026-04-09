from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# ─── ROUTES ─────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


# Example API (kasnije proširi)
@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "PERUN API"
    })


# ─── RUN ────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
