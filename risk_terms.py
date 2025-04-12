import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("preprocessed_full.csv")

high_risk_df = df[df['sentiment'] == 'high']


vectorizer = TfidfVectorizer(stop_words='english', max_features=50)  # You can increase max_features
X = vectorizer.fit_transform(high_risk_df['tweet'])

tfidf_scores = zip(vectorizer.get_feature_names_out(), X.sum(axis=0).tolist()[0])
sorted_terms = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)


print("Top High-Risk TF-IDF Terms :")
for term, score in sorted_terms[:10]:
    print(f"{term}: {score:.4f}")