import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy import stats

"""
Rollover rating vs weight
"""

df = pd.read_csv('data/Safercar_data.csv')

def prepare_weight_safety_data():
    df_clean = df.copy()
    df_clean['MODEL_YR'] = pd.to_numeric(df_clean['MODEL_YR'], errors='coerce')
    df_clean['ROLLOVER_STARS'] = pd.to_numeric(df_clean['ROLLOVER_STARS'], errors='coerce')
    df_clean['OVERALL_STARS'] = pd.to_numeric(df_clean['OVERALL_STARS'], errors='coerce')
    df_clean['CURB_WEIGHT'] = pd.to_numeric(df_clean['CURB_WEIGHT'], errors='coerce')
    df_clean['MIN_GROSS_WEIGHT'] = pd.to_numeric(df_clean['MIN_GROSS_WEIGHT'], errors='coerce')
    df_clean['WEIGHT_LBS'] = df_clean['CURB_WEIGHT'].combine_first(df_clean['MIN_GROSS_WEIGHT'])
    df_clean['WEIGHT_TONS'] = df_clean['WEIGHT_LBS'] / 2000
    df_clean = df_clean.dropna(subset=['WEIGHT_TONS', 'ROLLOVER_STARS', 'MAKE', 'MODEL'])
    df_clean = df_clean[(df_clean['WEIGHT_TONS'] > 0.5) & (df_clean['WEIGHT_TONS'] < 10)]
    df_clean = df_clean[(df_clean['ROLLOVER_STARS'] >= 0) & (df_clean['ROLLOVER_STARS'] <= 5)]
    return df_clean

def create_weight_safety_visualization():
    df_clean = prepare_weight_safety_data()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_clean['WEIGHT_TONS'],
        y=df_clean['ROLLOVER_STARS'],
        mode='markers',
        name='Vehicles',
        marker=dict(
            size=15,
            color=df_clean['OVERALL_STARS'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Overall<br>Stars", x=1.02),
            opacity=0.2,
            line=dict(width=1, color='white')
        ),
        text=df_clean['MAKE'] + ' ' + df_clean['MODEL'] + ' (' + df_clean['MODEL_YR'].astype(str) + ')',
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Weight: %{x:.1f} tons<br>"
            "Rollover Rating: %{y:.1f}<br>"
            "Overall Rating: %{marker.color:.1f}<br>"
            "<extra></extra>"
        )
    ))
    
    x = df_clean['WEIGHT_TONS'].values
    y = df_clean['ROLLOVER_STARS'].values
    
    if len(x) > 1:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        trend_x = np.linspace(x.min(), x.max(), 100)
        trend_y = slope * trend_x + intercept
        
        fig.add_trace(go.Scatter(
            x=trend_x,
            y=trend_y,
            mode='lines',
            name=f'Trend (r={r_value:.3f})',
            line=dict(color='red', width=3, dash='dash'),
            hovertemplate="Weight: %{x:.1f} tons<br>Predicted Rating: %{y:.2f}<br><extra></extra>"
        ))
    
    weight_bins = pd.cut(df_clean['WEIGHT_TONS'], bins=5)
    bin_means = df_clean.groupby(weight_bins)['ROLLOVER_STARS'].mean()
    bin_counts = df_clean.groupby(weight_bins).size()
    
    bin_centers = []
    for bin_range in bin_means.index:
        left = bin_range.left
        right = bin_range.right
        bin_centers.append((left + right) / 2)
    
    fig.add_trace(go.Scatter(
        x=bin_centers,
        y=bin_means.values,
        mode='markers+lines',
        name='Average by Weight Group',
        marker=dict(size=12, color='orange', symbol='diamond'),
        line=dict(color='orange', width=2),
        text=[f"{count} vehicles" for count in bin_counts.values],
        hovertemplate=(
            "Weight Group: %{x:.1f} tons<br>"
            "Average Rating: %{y:.2f}<br>"
            "Count: %{text}<br>"
            "<extra></extra>"
        )
    ))
    
    fig.update_layout(
        title=dict(
            text='Vehicle Weight vs Rollover Safety Rating',
            x=0.5,
            font=dict(size=24)
        ),
        xaxis_title="Vehicle Weight (tons)",
        yaxis_title="Rollover Star Rating",
        yaxis_range=[0, 5.5],
        height=700,
        hovermode='closest',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(t=80)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    if len(x) > 1:
        fig.add_annotation(
            # text=f"Correlation: r = {r_value:.3f}<br>p-value: {p_value:.4f}<br>N = {len(df_clean)} vehicles",
            text=f"Correlation: r = {r_value:.3f}<br>N = {len(df_clean)} vehicles",
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            font=dict(size=12),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        )
    
    fig.show()

if __name__ == "__main__":
    create_weight_safety_visualization()