# LordFlix Extractor

A Flask web app that fetches and decrypts stream data from LordFlix via the enc-dec API.

## Deploy to Render (from GitHub)

### Option A — One-click via render.yaml
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New → Blueprint**
3. Connect your GitHub repo — Render auto-reads `render.yaml` and deploys

### Option B — Manual
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo
4. Set:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60`
5. Click **Deploy**

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000`

## Project Structure

```
lordflix-app/
├── app.py              # Flask backend + API logic
├── templates/
│   └── index.html      # Web UI
├── requirements.txt
├── render.yaml         # Render deployment config
└── README.md
```

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Web UI |
| `/fetch` | POST | Fetch & decrypt stream data |
| `/servers` | GET | List available servers |

### POST `/fetch` body
```json
{
  "title": "Game of Thrones",
  "type": "series",
  "year": "2011",
  "imdb_id": "tt0944947",
  "tmdb_id": "1399",
  "server": "ServerName",
  "season": "1",
  "episode": "2"
}
```
