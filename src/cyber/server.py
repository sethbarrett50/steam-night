from __future__ import annotations

from dataclasses import dataclass

from flask import Flask, jsonify, render_template_string, request

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>STEAM Night Cyber Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
            background: #f7fbff;
            color: #102a43;
        }
        .card {
            background: white;
            border: 2px solid #d9e2ec;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 8px 24px rgba(16, 42, 67, 0.08);
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            margin-bottom: 16px;
            border-radius: 8px;
            border: 1px solid #bcccdc;
            font-size: 16px;
        }
        button {
            background: #2f80ed;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 18px;
            font-size: 16px;
            cursor: pointer;
        }
        .msg {
            margin-top: 16px;
            font-size: 18px;
            font-weight: bold;
        }
        .hint {
            margin-top: 20px;
            font-size: 15px;
            color: #486581;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔐 KidSafe Login Challenge</h1>
        <p>Can you guess the password before the computer does?</p>
        <form method="post">
            <label for="username">Username</label>
            <input id="username" name="username" value="student" />

            <label for="password">Password</label>
            <input id="password" name="password" type="password" />

            <button type="submit">Try Login</button>
        </form>

        {% if message %}
        <div class="msg">{{ message }}</div>
        {% endif %}

        <div class="hint">
            This is a safe classroom demo showing why weak passwords are easy for computers to guess.
        </div>
    </div>
</body>
</html>
"""


@dataclass(frozen=True)
class DemoConfig:
    password: str


def create_app(config: DemoConfig) -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    @app.get("/api/check")
    def api_check_get() -> tuple[dict[str, str], int]:
        return {"message": "Use POST with a password."}, 405

    @app.post("/api/check")
    def api_check() -> tuple[dict[str, bool | str], int]:
        data = request.get_json(silent=True) or {}
        password = str(data.get("password", ""))
        success = password == config.password
        return jsonify({"success": success, "password": password}), 200

    @app.route("/", methods=["GET", "POST"])
    def login() -> str:
        message = ""
        if request.method == "POST":
            password = request.form.get("password", "")
            if password == config.password:
                message = "✅ Access Granted!"
            else:
                message = "❌ Nope — try again!"
        return render_template_string(HTML_TEMPLATE, message=message)

    return app
