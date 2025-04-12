import pandas as pd
from langdetect import detect
from transformers import pipeline
from tqdm import tqdm

sentiment = pipeline("sentiment-analysis", device='cuda')


list_words = ['suicide prevention', 'stay safe', 'please call', 'covid']
pattern = '|'.join(list_words)

chunk_size = 5000000
processed_data = []

reader = pd.read_csv("x_data.csv", chunksize=chunk_size)

for i, chunk in enumerate(reader):
    print(f"Processing chunk {i+1}")

    chunk = chunk.dropna(subset=['tweet', 'date_time']).drop_duplicates(subset=['tweet'])

    #short tweets will get filterd
    chunk = chunk[chunk['tweet'].str.len() >= 45]

    #language detection
    chunk['lang'] = chunk['tweet'].apply(lambda x: detect(x) if pd.notnull(x) else 'unknown')
    chunk = chunk[chunk['lang'] == 'en']

    chunk = chunk[~chunk['tweet'].str.contains(pattern, case=False, na=False)]

    sentiments = []

    for tweet in tqdm(chunk['tweet'], desc=f"Sentiment analysis for chunk {i+1}"):

        sent = sentiment(tweet)[0]['score']
        if sent > 0.997:
            sentiments.append("high")
        elif sent > 0.994:
            sentiments.append("moderate")
        else:
            sentiments.append("low")
    
    chunk['sentiment'] = sentiments
    chunk = chunk.drop('lang', axis=1)

    processed_data.append(chunk)

    chunk.to_csv(f"data/preprocessed_chunk_{i+1}.csv", index=False)


final_df = pd.concat(processed_data)
final_df.to_csv("preprocessed_full.csv", index=False)
