import os
import requests
from urllib.parse import quote
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

HEADERS = {
    "Accept": "*/*",
    "Origin": "https://lordflix.org",
    "Referer": "https://lordflix.org/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
API = "https://enc-dec.app/api"


def validate(data, path):
    if data.get("status") != 200:
        raise ValueError(
            f"API Error at {path} | Status: {data.get('status')} | {data.get('error', 'Unknown error')}"
        )
    return data["result"]


def get_servers():
    try:
        resp = requests.get("https://snowhouse.lordflix.club/servers", headers=HEADERS, timeout=10)
        return resp.json().get("servers", [])
    except Exception as e:
        return []


def fetch_media(title, media_type, year, imdb_id, tmdb_id, server, season=None, episode=None):
    if media_type == "series":
        url = (
            f"https://snowhouse.lordflix.club/?title={quote(title)}&type=series"
            f"&year={year}&imdb={imdb_id}&tmdb={tmdb_id}&server={server}"
            f"&season={season}&episode={episode}"
        )
    else:
        url = (
            f"https://snowhouse.lordflix.club/?title={quote(title)}&type=movie"
            f"&year={year}&imdb={imdb_id}&tmdb={tmdb_id}&server={server}"
        )

    # Step 1: Encrypt + sign
    enc_lordflix = f"{API}/enc-lordflix?url={quote(url)}"
    response = requests.get(enc_lordflix, timeout=10).json()
    data = validate(response, enc_lordflix)
    enc_url = data["url"]
    sign = data["sign"]

    # Step 2: Get encrypted media data
    encrypted = requests.get(enc_url, headers=HEADERS, timeout=10).text

    # Step 3: Decrypt
    dec_lordflix = f"{API}/dec-lordflix"
    response = requests.post(dec_lordflix, json={"text": encrypted, "sign": sign}, timeout=10).json()
    decrypted = validate(response, dec_lordflix)

    return decrypted


@app.route("/")
def index():
    servers = get_servers()
    return render_template("index.html", servers=servers)


@app.route("/fetch", methods=["POST"])
def fetch():
    body = request.get_json()
    try:
        result = fetch_media(
            title=body["title"],
            media_type=body["type"],
            year=body["year"],
            imdb_id=body["imdb_id"],
            tmdb_id=body["tmdb_id"],
            server=body["server"],
            season=body.get("season"),
            episode=body.get("episode"),
        )
        return jsonify({"ok": True, "result": result, "referer": HEADERS["Referer"]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/servers")
def servers():
    return jsonify(get_servers())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
