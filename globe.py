import pandas as pd
import plotly.graph_objects as go
import random

# Criando dados fictícios para o globo interativo
countries = ['USA', 'China', 'Russia', 'Germany', 'Brazil', 'India', 'UK', 'France', 'Japan', 'Australia']
latitudes = [38, 35, 61, 51, -10, 20, 55, 46, 36, -25]
longitudes = [-97, 103, 100, 10, -55, 77, -3, 2, 138, 133]

data = []
for i, country in enumerate(countries):
    attacks = random.randint(50, 500)
    financial_loss = random.randint(10, 500)
    affected_users = random.randint(1000, 1000000)
    data.append({
        'Country': country,
        'Latitude': latitudes[i],
        'Longitude': longitudes[i],
        'Attack Count': attacks,
        'Financial Loss (in Million $)': financial_loss,
        'Affected Users': affected_users
    })

df = pd.DataFrame(data)

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    lon=df['Longitude'],
    lat=df['Latitude'],
    text=df.apply(lambda row: f"{row['Country']}<br>Attacks: {row['Attack Count']}<br>"
                              f"Loss: ${row['Financial Loss (in Million $)']}M<br>"
                              f"Affected Users: {row['Affected Users']}", axis=1),
    marker=dict(
        size=df['Attack Count']/10,
        color=df['Financial Loss (in Million $)'],
        colorscale='YlOrBr',
        cmin=df['Financial Loss (in Million $)'].min(),
        cmax=df['Financial Loss (in Million $)'].max(),
        colorbar_title="Loss (M$)",
        line=dict(width=0.5, color='darkred')
    ),
    hoverinfo="text"
))

fig.update_layout(
    title='Globo Interativo de Ataques Cibernéticos',
    width=1000,
    height=1000,
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
        lataxis=dict(range=[-90,90]),
        lonaxis=dict(range=[-180,180])
    )
)

# Salva HTML interativo para personalização posterior
fig.write_html("globo_cyber_beauty.html")
