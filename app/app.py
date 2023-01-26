"""Main components."""
# from pprint import pformat
from shiny import App, render, ui
from shiny.ui import TagList, div, h3, head_content, tags
from pathlib import Path
import requests
import json
import pandas as pd

app_ui = ui.page_fluid(
    head_content(
        # tags.meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        tags.style((Path(__file__).parent / "style.css").read_text()),
    ),
    div(
        h3("NYC Tax Lien Sales"),
        class_="title",
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(
            div(
                ui.input_numeric("limit", "Number of Results", value=25, min=1, max=50000),
                ui.input_numeric("offset", "Page Number", value=1),
                class_="filters",
            ),
        ),
        ui.panel_main(
            ui.output_table("info"),
        ),
    ),
)


def server(input, output, session):
    """Server function."""
    def lien_data(limit=1500, offset=0):
        payload = {'$limit': limit, '$offset': offset}
        url = "https://data.cityofnewyork.us/resource/9rz4-mjek.json"
        response = requests.get(url, params=payload)
        data = json.loads(response.text)
        return data

    @output
    @render.table
    def info():
        limit = input.limit()
        offset = (input.offset() - 1) * input.limit()
        data = lien_data(limit, offset)
        df = pd.DataFrame(data)
        df['month'] = pd.to_datetime(df['month'], format="%Y-%m-%dT%H:%M:%S")
        # print(df['month'])
        return df


app = App(app_ui, server)
