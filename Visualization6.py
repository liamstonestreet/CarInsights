import pandas as pd
import numpy as np
from textwrap import dedent
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

"""
Discarded visualization
"""

CSV_PATH = "data/cars.csv"

def load_and_clean(csv_path=CSV_PATH):
    df = pd.read_csv(CSV_PATH, dtype=str, encoding="utf-16")
    df.columns = [c.strip() for c in df.columns]
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    if "Price" in df.columns:
        df["Price"] = df["Price"].str.replace(",", "", regex=False)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    if "Mileage" in df.columns:
        df["Mileage"] = df["Mileage"].str.replace(",", "", regex=False)
        df["Mileage"] = pd.to_numeric(df["Mileage"], errors="coerce")
    text_cols = ["Brand", "Model", "Status", "Dealer"]
    for c in text_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().replace({"nan": None})
    if "Status" in df.columns:
        df["Status"] = df["Status"].replace({
            "Certified Pre-Owned": "Certified",
            "certified pre-owned": "Certified",
            "Certified Pre-owned": "Certified",
            "Certified Pre Owned": "Certified",
        })
    return df

df = load_and_clean(CSV_PATH)
df.replace({"": np.nan, "None": np.nan, "nan": np.nan}, inplace=True)
year_min = int(df["Year"].min()) if df["Year"].notna().any() else 2000
year_max = int(df["Year"].max()) if df["Year"].notna().any() else 2025
available_statuses = list(pd.Categorical(df["Status"].dropna().unique()))
if not available_statuses:
    available_statuses = ["New", "Used", "Certified"]

def aggregate_for_display(df, groupby_col, selected_statuses, year_range):
    d = df.copy()
    d = d[(d["Year"].notna()) & (d["Year"] >= year_range[0]) & (d["Year"] <= year_range[1])]
    if selected_statuses:
        d = d[d["Status"].isin(selected_statuses)]
    group_cols = [groupby_col, "Status"]
    agg = d.groupby(group_cols).agg(
        avg_price = pd.NamedAgg(column="Price", aggfunc=lambda s: np.nan if s.dropna().empty else s.dropna().mean()),
        avg_mileage = pd.NamedAgg(column="Mileage", aggfunc=lambda s: np.nan if s.dropna().empty else s.dropna().mean()),
        count = pd.NamedAgg(column="Price", aggfunc=lambda s: s.notna().sum() if s.notna().any() else len(s))
    ).reset_index()
    group_overall = agg.groupby(groupby_col).apply(
        lambda g: pd.Series({
            "group_avg_price": np.nan if g["avg_price"].dropna().empty else np.average(g["avg_price"].dropna(), weights=g.loc[g["avg_price"].notna(), "count"])
        })
    ).reset_index()
    agg = agg.merge(group_overall, on=groupby_col, how="left")
    agg.sort_values(["group_avg_price", groupby_col], ascending=[False, True], inplace=True)
    agg["group_order"] = pd.Categorical(agg[groupby_col], categories=agg[groupby_col].unique(), ordered=True)
    mileage = d.copy()
    mileage_group = mileage.groupby(groupby_col).agg(
        avg_mileage = pd.NamedAgg(column="Mileage", aggfunc=lambda s: np.nan if s.dropna().empty else s.dropna().mean()),
        count_with_mileage = pd.NamedAgg(column="Mileage", aggfunc=lambda s: s.notna().sum())
    ).reset_index()
    mileage_group[groupby_col] = pd.Categorical(mileage_group[groupby_col], categories=agg[groupby_col].unique(), ordered=True)
    mileage_group.sort_values(groupby_col, inplace=True)
    return agg, mileage_group

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2("Car market: Avg Price & Avg Mileage by Brand/Model"),
    html.Div([
        html.Div([
            html.Label("Grouping level:"),
            dcc.RadioItems(
                id="grouping",
                options=[{"label": "Brand", "value": "Brand"}, {"label": "Model", "value": "Model"}],
                value="Brand",
                inline=True
            )
        ], style={"display": "inline-block", "margin-right": "30px"}),
        html.Div([
            html.Label("Status filter:"),
            dcc.Checklist(
                id="status_filter",
                options=[{"label": str(s), "value": str(s)} for s in available_statuses],
                value=available_statuses,
                inline=True
            )
        ], style={"display": "inline-block", "margin-right": "30px"}),
        html.Div([
            html.Label("Year range:"),
            dcc.RangeSlider(
                id="year_slider",
                min=year_min,
                max=year_max,
                value=[year_min, year_max],
                marks={y: str(y) for y in range(year_min, year_max+1, max(1,(year_max-year_min)//8))},
                tooltip={"placement": "bottom", "always_visible": False}
            )
        ], style={"width": "60%", "display": "inline-block", "verticalAlign": "top"}),
    ], style={"margin-bottom": "20px"}),
    dcc.Graph(id="price_mileage_graph", config={"displayModeBar": True, "scrollZoom": True}, style={"height": "650px"}),
    html.Div(id="summary_text", style={"margin-top": "10px", "fontStyle": "italic", "color": "#444"}),
    html.Div([
        html.P(dedent("""
            Hover over bars or the line for details. Use the grouping switch to compare Brand vs Model.
            The bars show average price in USD (grouped by status), and the line shows average mileage
            for the group (averaged across selected statuses).
        """))
    ], style={"margin-top": "20px", "max-width": "900px"})
], style={"padding": "20px", "font-family": "Arial, sans-serif"})

@app.callback(
    Output("price_mileage_graph", "figure"),
    Output("summary_text", "children"),
    Input("grouping", "value"),
    Input("status_filter", "value"),
    Input("year_slider", "value"),
)
def update_figure(grouping, selected_statuses, year_slider):
    agg_df, mileage_df = aggregate_for_display(df, grouping, selected_statuses, year_slider)
    if agg_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data for selected filters",
            xaxis={"visible": False},
            yaxis={"visible": False},
        )
        return fig, "No listings match the selected filters."
    groups_order = list(agg_df[grouping].drop_duplicates())
    statuses = agg_df["Status"].unique()
    fig = go.Figure()
    for status in statuses:
        df_status = agg_df[agg_df["Status"] == status]
        df_status = df_status.set_index(grouping).reindex(groups_order).reset_index()
        x = df_status[grouping].astype(str)
        y = df_status["avg_price"]
        counts = df_status["count"]
        avg_mile = df_status["avg_mileage"]
        hover_text = []
        for g, p, m, c in zip(x, y, avg_mile, counts):
            price_text = f"${p:,.0f}" if pd.notna(p) else "N/A"
            mileage_text = f"{m:,.0f} mi" if pd.notna(m) else "N/A"
            hover_text.append(f"{grouping}: {g}<br>Status: {status}<br>Avg price: {price_text}<br>Avg mileage: {mileage_text}<br>Listings: {int(c) if not pd.isna(c) else 0}")
        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                name=str(status),
                customdata=np.stack([counts, df_status["avg_mileage"].fillna(np.nan)], axis=-1),
                hovertext=hover_text,
                hoverinfo="text",
            )
        )
    mileage_df = mileage_df.set_index(grouping).reindex(groups_order).reset_index()
    mileage_y = mileage_df["avg_mileage"]
    fig.add_trace(
        go.Scatter(
            x=mileage_df[grouping].astype(str),
            y=mileage_y,
            mode="lines+markers",
            name="Avg mileage (group)",
            yaxis="y2",
            hovertemplate = "%{x}<br>Avg mileage: %{y:.0f} mi<br>Listings with mileage: %{customdata}",
            customdata = mileage_df["count_with_mileage"].fillna(0).astype(int),
        )
    )
    fig.update_layout(
        barmode="group",
        title=f"Average Price (bars) and Average Mileage (line) by {grouping} — Years {year_slider[0]} to {year_slider[1]}",
        xaxis_title=grouping,
        yaxis=dict(title="Average Price (USD)", tickprefix="$", showgrid=True),
        yaxis2=dict(
            title="Average Mileage (miles)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend_title="Status / Metric",
        margin=dict(l=60, r=60, t=80, b=140),
        hovermode="x unified"
    )
    if len(groups_order) > 30:
        fig.update_layout(xaxis_tickangle=45)
    total_listings = df[
        (df["Year"].notna()) & (df["Year"] >= year_slider[0]) & (df["Year"] <= year_slider[1]) & 
        (df["Status"].isin(selected_statuses))
    ].shape[0]
    summary = f"Showing {total_listings} listings across {len(groups_order)} {grouping.lower() + ('s' if not grouping.endswith('s') else '')}."
    return fig, summary

if __name__ == "__main__":
    app.run(debug=True, port=8056)