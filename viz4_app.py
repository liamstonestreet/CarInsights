import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from preprocess import preprocess_recall_data


# ---------- Load & preprocess recall data ----------

RECALL_PATH = "data/recall"  # adjust if needed
df = preprocess_recall_data(RECALL_PATH)

# Clean MODEL YEAR
df = df.dropna(subset=["MODEL YEAR"])
df["MODEL YEAR"] = df["MODEL YEAR"].astype(int)

ALL_MAKES = sorted(df["MAKE"].dropna().unique())
DEFAULT_MAKE = "SUBARU" if "SUBARU" in ALL_MAKES else ALL_MAKES[0]

# Precompute brand-year and model-year recall counts (distinct campaigns)
BRAND_YEAR_COUNTS = (
    df.groupby(["MAKE", "MODEL YEAR"])["NHTSA ID"]
    .nunique()
    .reset_index()
)

MODEL_YEAR_COUNTS = (
    df.groupby(["MODEL", "MODEL YEAR"])["NHTSA ID"]
    .nunique()
    .reset_index()
)



# def build_figure(make: str, model: str):
#     """Build the Plotly figure for a given make + model (or all models)."""
#     df_brand = df[df["MAKE"] == make]

#     if model != "ALL_MODELS":
#         df_brand = df_brand[df_brand["MODEL"] == model]

#     if df_brand.empty:
#         fig = go.Figure()
#         fig.update_layout(
#             title=f"No data for {make}" + ("" if model == "ALL_MODELS" else f" – {model}"),
#             template="plotly_white",
#         )
#         return fig

#     # Count distinct recall campaigns per model year
#     grouped = df_brand.groupby("MODEL YEAR")["NHTSA ID"].nunique()

#     # Continuous year range
#     min_year = int(df_brand["MODEL YEAR"].min())
#     max_year = int(df_brand["MODEL YEAR"].max())
#     all_years = list(range(min_year, max_year + 1))

#     grouped_full = grouped.reindex(all_years, fill_value=0)

#     years = grouped_full.index.to_list()
#     counts = grouped_full.values

#     # Year formatter (your logic)
#     def format_year(year: int) -> str:
#         first_two = year // 100
#         yy = year % 100
#         if first_two == 19:
#             return f"'{yy:02d}"
#         return f"{yy:02d}"

#     tickvals = years
#     ticktext = [format_year(y) for y in years]

#     title_suffix = "" if model == "ALL_MODELS" else f" – {model}"

#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=years,
#             y=counts,
#             mode="lines+markers",
#             name="Distinct recall campaigns",
#             hovertemplate="Model Year: %{x}<br>Recalls: %{y}<extra></extra>",
#         )
#     )

#     fig.update_layout(
#         title=f"Recall Trends for {make}{title_suffix} (by Model Year)",
#         xaxis=dict(
#             title="Model Year",
#             tickmode="array",
#             tickvals=tickvals,
#             ticktext=ticktext,
#         ),
#         yaxis=dict(
#             title="Number of distinct recalls",
#             dtick=1,  # integer y-ticks
#         ),
#         template="plotly_white",
#         margin=dict(l=60, r=20, t=60, b=60),
#     )
#     return fig

def build_figure(make: str, model: str):
    """Build the Plotly figure for a given make + model (or all models)."""
    df_brand = df[df["MAKE"] == make]

    if model != "ALL_MODELS":
        df_brand = df_brand[df_brand["MODEL"] == model]

    if df_brand.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"No data for {make}" + ("" if model == "ALL_MODELS" else f" – {model}"),
            template="plotly_white",
        )
        return fig

    # Count distinct recall campaigns per model year for the selected series
    grouped = df_brand.groupby("MODEL YEAR")["NHTSA ID"].nunique()

    # Continuous year range
    min_year = int(df_brand["MODEL YEAR"].min())
    max_year = int(df_brand["MODEL YEAR"].max())
    all_years = list(range(min_year, max_year + 1))

    grouped_full = grouped.reindex(all_years, fill_value=0)

    years = grouped_full.index.to_list()
    counts = grouped_full.values

    # ---- Percentile computation for hover ----
    percentile_strings = []

    if model == "ALL_MODELS":
        # percentile across brands for that year
        for y, c in zip(years, counts):
            dist = BRAND_YEAR_COUNTS.loc[
                BRAND_YEAR_COUNTS["MODEL YEAR"] == y, "NHTSA ID"
            ].values
            if len(dist) == 0:
                percentile_strings.append("N/A")
            else:
                pct = 100.0 * (dist <= c).sum() / len(dist)
                percentile_strings.append(f"{pct:.1f}%")
        percentile_prefix = "Percentile (across brands):"
    else:
        # percentile across models for that year
        for y, c in zip(years, counts):
            dist = MODEL_YEAR_COUNTS.loc[
                MODEL_YEAR_COUNTS["MODEL YEAR"] == y, "NHTSA ID"
            ].values
            if len(dist) <= 4:  # only if more than 4 models
                percentile_strings.append("N/A")
            else:
                pct = 100.0 * (dist <= c).sum() / len(dist)
                percentile_strings.append(f"{pct:.1f}%")
        percentile_prefix = "Percentile (across models):"

    # Year formatter (your logic)
    def format_year(year: int) -> str:
        first_two = year // 100
        yy = year % 100
        if first_two == 19:
            return f"'{yy:02d}"
        return f"{yy:02d}"

    tickvals = years
    ticktext = [format_year(y) for y in years]

    title_suffix = "" if model == "ALL_MODELS" else f" – {model}"

    hover_template = (
        "Model Year: %{x}<br>"
        "Recalls: %{y}<br>"
        f"{percentile_prefix} %{{customdata}}<br>" # Interpolate percentile_prefix here
        "<extra></extra>"
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years,
            y=counts,
            mode="lines+markers",
            name="Distinct recall campaigns",
            customdata=percentile_strings,
            hovertemplate=hover_template,
        )
    )

    fig.update_layout(
        title=f"Recall Trends for {make}{title_suffix} (by Model Year)",
        xaxis=dict(
            title="Model Year",
            tickmode="array",
            tickvals=tickvals,
            ticktext=ticktext,
        ),
        yaxis=dict(
            title="Number of distinct recalls",
            dtick=1,  # integer y-ticks
        ),
        template="plotly_white",
        margin=dict(l=60, r=20, t=60, b=60),
    )
    return fig



# ---------- Dash app (GPT helped me make the html layout) ----------

app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "sans-serif", "maxWidth": "900px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H2("Recall Trends by Model Year"),

        html.Div(
            style={"display": "flex", "gap": "16px", "marginBottom": "16px"},
            children=[
                html.Div(
                    style={"flex": 1},
                    children=[
                        html.Label("Make"),
                        dcc.Dropdown(
                            id="make-dropdown",
                            options=[{"label": m, "value": m} for m in ALL_MAKES],
                            value=DEFAULT_MAKE,
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": 1},
                    children=[
                        html.Label("Model"),
                        dcc.Dropdown(
                            id="model-dropdown",
                            options=[{"label": "All models", "value": "ALL_MODELS"}],
                            value="ALL_MODELS",
                            clearable=False,
                        ),
                    ],
                ),
            ],
        ),

        dcc.Graph(id="recall-graph"),
    ],
)


# ---------- Callbacks ----------

@app.callback(
    Output("model-dropdown", "options"),
    Output("model-dropdown", "value"),
    Input("make-dropdown", "value"),
)
def update_model_options(selected_make):
    df_brand = df[df["MAKE"] == selected_make]

    if df_brand.empty:
        options = [{"label": "All models", "value": "ALL_MODELS"}]
        return options, "ALL_MODELS"

    models = sorted(df_brand["MODEL"].dropna().unique())
    options = [{"label": "All models", "value": "ALL_MODELS"}] + [
        {"label": m, "value": m} for m in models
    ]
    return options, "ALL_MODELS"

@app.callback(
    Output("recall-graph", "figure"),
    Input("make-dropdown", "value"),
    Input("model-dropdown", "value"),
)
def update_graph(selected_make, selected_model):
    return build_figure(selected_make, selected_model)


if __name__ == "__main__":
    app.run(debug=True)
