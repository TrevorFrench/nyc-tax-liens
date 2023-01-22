"""Main components."""
# from pprint import pformat
from shiny import App, render, ui
import requests
import json
import pandas as pd

app_ui = ui.page_fluid(
    ui.panel_title("NYC Tax Lien Sales"),
    ui.input_numeric("limit", "Number of Results", value=25, max=50000),
    ui.input_numeric("offset", "Page Number", value=1),
    ui.output_table("info"),
)


def server(input, output, session):
    """Server function."""
    # @reactive.Calc
    # def offset():
    #     return (input.offset() - 1) * input.limit()

    # @reactive.Calc
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
        # print(data)
        df = pd.DataFrame(data)
        print(df)
        return df


app = App(app_ui, server)
