"""Main components."""
# from pprint import pformat
from shiny import App, render, ui
from shiny.ui import TagList, div, h3, head_content, tags
from pathlib import Path
import requests
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
                # min/max form controls don't work. I need to submit a ticket for this.
                ui.input_numeric("limit", "Number of Results", value=5, min=1, max=50000),
                ui.input_numeric("offset", "Page Number", value=1),
                ui.input_select(
                    "column_names",
                    "Column Names",
                    {
                        "month": "month",
                        "cycle": "cycle",
                        "borough": "borough",
                        "block": "block",
                        "lot": "lot",
                        "tax_class_code": "tax_class_code",
                        "building_class": "building_class",
                        "community_board": "community_board",
                        "council_district": "council_district",
                        "house_number": "house_number",
                        "street_name": "street_name",
                        "zip_code": "zip_code",
                        "water_debt_only": "water_debt_only",
                    },
                    selected=[
                        "month",
                        "cycle",
                        "tax_class_code",
                        "building_class",
                        "street_name",
                        "zip_code",
                        "water_debt_only",
                    ],
                    multiple=True,
                ),
                ui.input_date_range("date_range", "Date Range", start="2001-01-01", end="2023-12-31"),
                ui.input_select(
                    "cycle",
                    "Cycle",
                    [
                        "90 Day Notice",
                        "60 Day Notice",
                        "30 Day Notice",
                        "10 Day Notice",
                        "90 Days Notice",
                        "60 Days Notice",
                        "30 Days Notice",
                        "10 Days Notice",
                        "Final Sale",
                    ],
                    selected="90 Day Notice",
                ),
                ui.input_select(
                    "borough",
                    "Borough",
                    [1,2,3,4,5,],
                    selected=1,
                ),
                ui.input_select(
                    "tax_class_code",
                    "Tax Class Code",
                    [1,2,4,],
                    selected=1,
                ),
                ui.input_radio_buttons(
                    "water_debt_only",
                    "Water Debt Only",
                    {
                        "YES": "Yes",
                        "NO": "No",
                    },
                ),
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
    def lien_data(limit=1500, offset=0, begin_date="2001-01-01", end_date="2023-12-31", cycle="90 Day Notice", borough=1, tax_class_code=1, water_debt_only="YES"):
        date_query = f"month between '{begin_date}' and '{end_date}'"
        payload = {'$limit': limit, '$offset': offset, '$where': date_query, 'cycle': cycle, 'borough': borough, 'tax_class_code': tax_class_code, 'water_debt_only': water_debt_only}
        url = "https://data.cityofnewyork.us/resource/9rz4-mjek.json"
        response = requests.get(url, params=payload)
        data = response.json()
        return data

    @output
    @render.table
    def info():
        limit = input.limit()
        offset = (input.offset() - 1) * input.limit()
        date_range = input.date_range()
        begin_date = date_range[0]
        end_date = date_range[1]
        cycle = input.cycle()
        borough = input.borough()
        tax_class_code = input.tax_class_code()
        water_debt_only = input.water_debt_only()
        data = lien_data(limit, offset, begin_date, end_date, cycle, borough, tax_class_code, water_debt_only)
        df = pd.DataFrame(data)
        df['month'] = pd.to_datetime(df['month'], format="%Y-%m-%dT%H:%M:%S")
        cols = []
        for name in input.column_names():
            cols.append(name)
        df = df[cols]
        return df


app = App(app_ui, server)
