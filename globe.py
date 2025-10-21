import pandas as pd
import plotly.graph_objects as go

# === IMPORTANDO DADOS REAIS ===
df = pd.read_csv('data/globe_data.csv')

def format_money(value):
    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:.0f}"

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lon=df['Longitude'],
    lat=df['Latitude'],
    text=df.apply(lambda row: (
        f"{row['Country']}<br>"
        f"Ataques: {int(row['Attack Count']):,}<br>"
        f"Perdas: {format_money(row['Financial Loss (in Million $)'] * 1_000_000)}<br>"
        f"Usuários afetados: {int(row['Number of Affected Users']):,}"
    ), axis=1),
    marker=dict(
        size=df['Attack Count'] / df['Attack Count'].max() * 40,
        color=df['Financial Loss (in Million $)'],
        colorscale='YlOrBr',
        cmin=df['Financial Loss (in Million $)'].min(),
        cmax=df['Financial Loss (in Million $)'].max(),
        colorbar_title="Perdas (M$)",
        line=dict(width=0.5, color='darkred')
    ),
    hoverinfo="text"
))

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    geo=dict(
        projection_type='orthographic',
        showland=True,
        landcolor="rgb(25,25,25)",
        showcountries=True,
        countrycolor="rgb(60,60,60)",
        showocean=True,
        oceancolor="rgb(5,10,40)",
        showcoastlines=True,
        coastlinecolor="rgb(120,120,120)",
        bgcolor="rgba(0,0,0,0)"
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

fig.write_html("globo_cyber_beauty.html")
print("Arquivo salvo como globo_cyber.html")
