import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv("preprocessed_full.csv")


sentiment_order = ['low', 'moderate', 'high']

sentiment_counts = df['sentiment'].value_counts().reindex(sentiment_order).reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']
print(sentiment_counts.columns)

color_map = {'low': 'skyblue', 'moderate': 'blue', 'high': 'purple'}


fig = go.Figure()

for sentiment in sentiment_order:
    count = sentiment_counts[sentiment_counts['Sentiment'] == sentiment]['Count'].values[0]
    fig.add_trace(go.Bar(
        x=[sentiment],
        y=[count],
        name=sentiment.capitalize(),
        marker_color=color_map[sentiment]
    ))


fig.update_layout(
    title="Distribution of Posts by Sentiment",
    xaxis_title="Sentiment Category",
    yaxis_title="Number of Posts",
    title_font_size=18,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    showlegend=True
)


fig.write_image("sentiment_level.jpeg", scale=2)
fig.show()
