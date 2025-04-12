import pandas as pd
import plotly.express as px
import pycountry


df = pd.read_csv("preprocessed_full.csv")

df = df[df['sentiment'] == "high"]

df_grouped = df.groupby('country').size().reset_index(name='count')


def alpha2_to_alpha3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

df_grouped['country_list'] = df_grouped['country'].apply(alpha2_to_alpha3)

print(df_grouped)

df_grouped = df_grouped.dropna(subset=['country_list'])

# Plot using Alpha-3 codes
fig = px.choropleth(
    df_grouped,
    locations="country_list",
    color="count",
    hover_name="country",
    color_continuous_scale="Reds",
    title="Location-wise Heatmap of Activity"
)
fig.write_image("countries_with_high_risk.jpeg", scale=2)
fig.update_geos(showcountries=True)
fig.show()
