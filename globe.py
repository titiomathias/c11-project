import pandas as pd
import plotly.graph_objects as go

# === IMPORTANDO DADOS REAIS ===
df = pd.read_csv('data/globe_data.csv')

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lon=df['Longitude'],
    lat=df['Latitude'],
    text=df.apply(lambda row: f"{row['Country']}<br>"
                              f"Ataques: {row['Attack Count']}<br>"
                              f"Perdas: ${row['Financial Loss (in Million $)']:.1f}M<br>"
                              f"Usuários afetados: {int(row['Number of Affected Users']):,}",
                  axis=1),
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
    title='🌐 Globo Interativo de Ataques Cibernéticos (2015–2024)',
    margin=dict(l=0, r=0, t=50, b=0),
    geo=dict(
        projection_type='orthographic',
        showland=True,
        landcolor="rgb(204, 230, 179)",
        showcountries=True,
        countrycolor="rgb(80, 80, 80)",
        showocean=True,
        oceancolor="rgb(170, 215, 255)",
        showcoastlines=True,
        coastlinecolor="rgb(50,50,50)",
    )
)

fig.write_html("globo_cyber.html")
print("Arquivo salvo como globo_cyber.html")
