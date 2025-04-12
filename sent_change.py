import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px


df = pd.read_csv("preprocessed_full.csv")

#parse date
df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
df = df.dropna(subset=['date_time'])

#Run VADER sentiment analysis
analyzer = SentimentIntensityAnalyzer()
df['negativity'] = df['tweet'].apply(lambda x: analyzer.polarity_scores(str(x))['neg'])

#Extract year
df['Year'] = df['date_time'].dt.year


yearly_negativity = df.groupby('Year')['negativity'].mean().reset_index()
yearly_negativity.columns = ['Year', 'Avg_Negativity']


yearly_negativity.to_csv("yearwise_avg_negativity.csv", index=False)



fig = px.line(yearly_negativity, x='Year', y='Avg_Negativity',
              title='Year-wise Average Negativity in Tweets',
              labels={'Avg_Negativity': 'Average Negativity Score'},
              markers=True)

fig.update_traces(line=dict(color='darkred'))
fig.update_layout(xaxis_title='Year', yaxis_title='Average Negativity Score')
fig.show()
