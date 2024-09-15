from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from view_stats import AdStats
from ads import AdsBank
import plotly.graph_objects as go

from datetime import datetime, timedelta
from pathlib import Path
import os

df = AdStats.read()
ad_bank = AdsBank()


dirname = Path(os.path.dirname(__file__))
static_image_dir = dirname.parent / "public/"

app = Dash()

app.layout = [
    html.H1(children="Ad Statistics", style={"textAlign": "center"}),
    dcc.Dropdown(df.ad_id.unique(), "", id="dropdown-selection"),
    html.Img(id="img", src=None, width=600),
    html.H2(id="caption", children="", style={"textAlign": "left"}),
    dcc.Graph(id="map"),
    dcc.Graph(id="time"),
]


def create_state_map(df: pd.DataFrame, filter_by_id: str | None = None):
    if filter_by_id is not None:
        df = df[df["ad_id"] == filter_by_id]

    count_per_state = df["region_code"].value_counts().to_dict()

    fig = px.choropleth(
        title="Ad Views per state",
        locations=list(count_per_state.keys()),
        locationmode="USA-states",
        color=list(count_per_state.values()),
        scope="usa",
    )
    return fig


def create_time_graph(df: pd.DataFrame, filter_by_id: str | None = None):
    if filter_by_id is not None:
        df = df[df["ad_id"] == filter_by_id]

    df["datetime"] = pd.to_datetime(df["time"], unit="s")
    df["day"] = df["datetime"].dt.strftime("%Y-%m-%d")

    a_week_ago = (datetime.today() - timedelta(weeks=1)).strftime("%Y-%m-%d")
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    hist = go.Histogram(
        x=df["day"],
        y=df["ad_duration"] / 1000,  # convert ms -> seconds
        autobinx=False,
        histfunc="sum",
        xbins=dict(start=a_week_ago, end=tomorrow, size="D"),
    )
    fig = go.Figure(data=[hist])
    fig.for_each_xaxis(lambda x: x.update({"range": [a_week_ago, tomorrow]}))
    fig.update_layout(title="Total Ad time this week (seconds)")
    return fig


@callback(Output("caption", "children"), Input("dropdown-selection", "value"))
def update_caption(value):
    if value == "" or value not in ad_bank.ads:
        return ""
    return ad_bank.ads[value]["message"]


@callback(Output("img", "src"), Input("dropdown-selection", "value"))
def update_img(value):
    if value == "" or value not in ad_bank.ads:
        return ""

    img_url = ad_bank.ads[value]["img_url"]
    if img_url.startswith("http"):
        return img_url
    return f"http://localhost:3000/{img_url}"


@callback(Output("map", "figure"), Input("dropdown-selection", "value"))
def update_map(value):
    return create_state_map(df, filter_by_id=value)


@callback(Output("time", "figure"), Input("dropdown-selection", "value"))
def update_time_graph(value):
    global df
    df = AdStats.read()
    return create_time_graph(df, filter_by_id=value)


if __name__ == "__main__":
    app.run(debug=True)
