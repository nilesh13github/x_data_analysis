import pandas as pd

df = pd.read_csv("x_data.csv")

sampled_df = df.sample(n=100000, random_state=42)  # `random_state` for reproducibility

sampled_df.to_csv("random_100000.csv", index=False)

