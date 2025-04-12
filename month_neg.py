import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px

# Load the dataset
df = pd.read_csv("preprocessed_full.csv")

# Convert date column
df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
df = df.dropna(subset=['date_time'])

# Initialize VADER analyzer
analyzer = SentimentIntensityAnalyzer()

# Compute negativity scores
df['negativity'] = df['tweet'].apply(lambda x: analyzer.polarity_scores(str(x))['neg'])

# Extract full month name (e.g., January, February)
df['Month'] = df['date_time'].dt.month_name()

# Define custom month order for plot
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

# Group by month and calculate average negativity
monthly_negativity = df.groupby('Month')['negativity'].mean().reindex(month_order).reset_index()
monthly_negativity.columns = ['Month', 'Avg_Negativity']

# Save to CSV
monthly_negativity.to_csv("monthwise_avg_negativity.csv", index=False)

# Plot using Plotly
fig = px.bar(monthly_negativity, x='Month', y='Avg_Negativity',
             title='Average Negative Sentiment by Month (All Years Combined from 2014-2024)',
             labels={'Avg_Negativity': 'Average Negativity Score'},
             color='Avg_Negativity',
             color_continuous_scale='Blues')

fig.update_layout(xaxis_title='Month',
                  yaxis_title='Average Negative Sentiment',
                  xaxis_tickangle=45,
                  bargap=0.25)

fig.show()
