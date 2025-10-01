# 🎶 The History Oracle

This is a Dash app visualizing your personal music listening history as an interactive timeline narrative, styled with a green and black theme, rounded typography, and vibrant accent colors representing moods and genres. All data is loaded from your Google Cloud Storage CSV.

## Features
- Timeline-driven narrative: music, dates, places, moods.
- Interactive filtering by mood and genre.
- Eclectic dynamic styling that changes with time, mood, and genre.
- Single interactive interface (not separate charts).

## Local Development

```bash
pip install -r requirements.txt
python api/app.py
```

## Vercel Deployment

1. Clone the repo and commit the files above.
2. Push to GitHub and link your repo to Vercel.
3. Vercel will detect `vercel.json` and deploy `api/app.py` as a Python serverless function.
4. Access your Dash app at `https://<your-vercel-deployment>/api/app`.

## Testing

Run basic tests with:
```bash
pytest test_app.py
```

## Data Source

- [THEHISTORYORACLE.csv](https://storage.googleapis.com/workthisfucker/THEHISTORYORACLE.csv) (8+ years of spotty listening data)

## Customization

- Update accent colors and palettes in `api/app.py` as needed.
- Add more tests to `test_app.py` for robust validation.
