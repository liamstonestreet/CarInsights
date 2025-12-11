import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data/Safercar_data.csv')

def prepare_data():
    df_clean = df.copy()
    df_clean['MODEL_YR'] = pd.to_numeric(df_clean['MODEL_YR'], errors='coerce')
    df_clean['ROLLOVER_STARS'] = pd.to_numeric(df_clean['ROLLOVER_STARS'], errors='coerce')
    df_clean = df_clean.dropna(subset=['MODEL_YR', 'ROLLOVER_STARS', 'MAKE'])
    current_year = pd.Timestamp.now().year
    df_clean = df_clean[(df_clean['MODEL_YR'] >= 2000) & (df_clean['MODEL_YR'] <= current_year)]
    return df_clean

def create_rollover_dashboard():
    df_clean = prepare_data()
    makes = sorted(df_clean['MAKE'].unique())
    pivot_avg = df_clean.pivot_table(values='ROLLOVER_STARS', index='MODEL_YR', columns='MAKE', aggfunc='mean')
    pivot_count = df_clean.pivot_table(values='ROLLOVER_STARS', index='MODEL_YR', columns='MAKE', aggfunc='count')
    fig = go.Figure()
    colors = ['#1f77b4', '#ff7f0e']
    default_make1 = 'ACURA'
    default_make2 = 'ACURA'
    
    for make, color in [(default_make1, colors[0]), (default_make2, colors[1])]:
        if make in pivot_avg.columns:
            fig.add_trace(go.Scatter(
                x=pivot_avg.index,
                y=pivot_avg[make],
                mode='lines+markers',
                name=make,
                showlegend=False,
                line=dict(color=color, width=3),
                marker=dict(size=8),
                hovertemplate=(
                    f"<b>{make}</b><br>"
                    "Year: %{x}<br>"
                    "Avg Rating: %{y:.2f}<br>"
                    "Models: %{customdata[0]}<br>"
                    "<extra></extra>"
                ),
                customdata=pivot_count[make].fillna(0).astype(int).values.reshape(-1, 1)
            ))
    
    fig.update_layout(
        xaxis_title="Model Year",
        yaxis_title="Average Rollover Star Rating",
        yaxis_range=[0, 5.5],
        hovermode='closest',
        height=600,
        showlegend=False,
        margin=dict(t=50)
    )
    
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[dict(
                    method="update",
                    label=make,
                    args=[{
                        "y": [
                            pivot_avg[make].tolist() if make in pivot_avg.columns else [],
                            pivot_avg[default_make2].tolist() if default_make2 in pivot_avg.columns else []
                        ],
                        "name": [make, default_make2],
                        "showlegend": [False, False]
                    }]
                ) for make in makes],
                direction="down",
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
                bgcolor="lightblue"
            ),
            dict(
                buttons=[dict(
                    method="update",
                    label=make,
                    args=[{
                        "y": [
                            pivot_avg[default_make1].tolist() if default_make1 in pivot_avg.columns else [],
                            pivot_avg[make].tolist() if make in pivot_avg.columns else []
                        ],
                        "name": [default_make1, make],
                        "showlegend": [False, False]
                    }]
                ) for make in makes],
                direction="down",
                showactive=True,
                x=0.4,
                xanchor="left",
                y=1.1,
                yanchor="top",
                bgcolor="orange"
            )
        ]
    )
    
    fig.show()

if __name__ == "__main__":
    create_rollover_dashboard()