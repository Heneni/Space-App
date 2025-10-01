import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import os

DATA_URL = "https://storage.googleapis.com/workthisfucker/THEHISTORYORACLE.csv"
df = pd.read_csv(DATA_URL, parse_dates=["ts"])

MOOD_COLORS = {
    "happy": "#00FF7F", "sad": "#001A33", "energetic": "#FFD700",
    "chill": "#00CED1", "nostalgic": "#7B68EE", "angry": "#FF4500",
    "romantic": "#FF69B4", "eclectic": "#39FF14"
}
GENRE_ACCENTS = {
    "rock": "#FF1493", "hip-hop": "#1DB954", "electronic": "#00BFFF",
    "pop": "#FFD700", "classical": "#8A2BE2"
}

app = dash.Dash(__name__, requests_pathname_prefix="/api/app/")
server = app.server

app.layout = html.Div(
    style={"backgroundColor": "#0F1D13", "fontFamily": "Montserrat, Arial, sans-serif", "color": "#E0FFE0", "borderRadius": "20px", "padding": "2rem"},
    children=[
        html.H1("🎶 The History Oracle", style={"color": "#39FF14", "textAlign": "center", "fontWeight": "700"}),
        html.P("A timeline-driven narrative of my musical journey, painted by moods, places, and genres.", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="filter-mood",
            options=[{"label": mood.title(), "value": mood} for mood in sorted(df["mood"].unique())],
            value=None,
            placeholder="Filter by Mood",
            style={"borderRadius": "15px", "backgroundColor": "#002d09", "color": "#39FF14"}
        ),
        dcc.Dropdown(
            id="filter-genre",
            options=[{"label": genre.title(), "value": genre} for genre in sorted(df["genre"].unique())],
            value=None,
            placeholder="Filter by Genre",
            style={"marginTop": "10px", "borderRadius": "15px", "backgroundColor": "#002d09", "color": "#FFD700"}
        ),
        dcc.Graph(id="timeline-graph", config={"displayModeBar": False}, style={"borderRadius": "25px", "marginTop": "2rem"}),
        html.Div(id="track-details", style={"marginTop": "2rem", "backgroundColor": "#142e19", "borderRadius": "20px", "padding": "1rem"}),
    ]
)

@app.callback(
    Output("timeline-graph", "figure"),
    [Input("filter-mood", "value"), Input("filter-genre", "value")]
)
def update_timeline(selected_mood, selected_genre):
    filtered_df = df.copy()
    if selected_mood:
        filtered_df = filtered_df[filtered_df["mood"] == selected_mood]
    if selected_genre:
        filtered_df = filtered_df[filtered_df["genre"] == selected_genre]
    color_map = filtered_df["mood"].map(MOOD_COLORS).fillna("#39FF14")
    accent_map = filtered_df["genre"].map(GENRE_ACCENTS).fillna("#FFD700")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df["ts"],
        y=[1]*len(filtered_df),
        mode="markers+text",
        marker=dict(
            size=18,
            color=color_map,
            line=dict(width=2, color=accent_map)
        ),
        text=filtered_df["track"] + " - " + filtered_df["artist"],
        hovertext=filtered_df.apply(lambda row: f"{row['ts'].strftime('%Y-%m-%d')}: {row['track']} by {row['artist']}<br>Genre: {row['genre']} | Mood: {row['mood']}<br>Place: {row.get('place','')}", axis=1),
        hoverinfo="text",
        textposition="bottom center"
    ))
    fig.update_layout(
        plot_bgcolor="#0F1D13",
        paper_bgcolor="#0F1D13",
        xaxis_title="Date",
        yaxis_visible=False,
        font=dict(family="Montserrat, Arial", color="#E0FFE0"),
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        hoverlabel=dict(bgcolor="#002d09", font_size=14, font_family="Montserrat")
    )
    return fig

@app.callback(
    Output("track-details", "children"),
    [Input("timeline-graph", "clickData")]
)
def show_track_details(clickData):
    if clickData is None or "points" not in clickData:
        return "Click a point on the timeline to see track details, moods, and more."
    point = clickData["points"][0]
    idx = point["pointIndex"]
    row = df.iloc[idx]
    elements = [
        html.H2(f"{row['track']} – {row['artist']}", style={"color": GENRE_ACCENTS.get(row['genre'], "#39FF14")}),
        html.P(f"Date: {row['ts'].strftime('%Y-%m-%d')} | Genre: {row['genre']} | Mood: {row['mood']} | Place: {row.get('place','')}"),
        html.Div(f"Feeling: {row['mood']}", style={"color": MOOD_COLORS.get(row['mood'], "#39FF14"), "fontWeight": "bold"}),
    ]
    if "audio_url" in row and pd.notna(row["audio_url"]):
        elements.append(html.Audio(src=row["audio_url"], controls=True, style={"width": "100%", "marginTop": "10px"}))
    return html.Div(elements, style={"backgroundColor": "#142e19", "borderRadius": "20px", "padding": "1rem"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run_server(debug=False, host="0.0.0.0", port=port)
