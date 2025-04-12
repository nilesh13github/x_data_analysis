# x_data_analysis

> The main raw dataset of 42M publicly available tweets is uploaded on → [[https://huggingface.co/Nilesh213/x_data.csv/tree/main/https%3A/huggingface.co/datasets/Nilesh213/X-dataset/tree/main]]

---

### 1 → `Scrapper.py`
- Scrapes 42 million raw tweets from publicly available sources.

---

### 2 → `preprocessing2.py`

- **Drops** rows with missing `tweet` or `date_time` values.  
- **Removes** duplicate tweets.  
- **Filters out** short tweets (less than 45 characters).  
- **Detects language** of each tweet and keeps only English tweets.  
- **Removes tweets** containing any of the unwanted phrases from `list_words`  
  (e.g., `"suicide prevention"`, `"stay safe"`, `"please call"`, `"covid"`).

---

#### → **Sentiment Analysis**
- Analyzes sentiment using the Hugging Face sentiment pipeline.
- Sentiment is categorized based on confidence score:
  - `"high"` → score > 0.997  
  - `"moderate"` → score > 0.994  
  - `"low"` → score ≤ 0.994
- Adds the `sentiment` label as a new column.

- Removes the temporary `lang` column.

---

#### → **Saving and Merging Results**
- Saves each processed chunk as a separate CSV in the `data/` folder  
  *(note: removed from this repository to save space)*.
- Appends each chunk to a master list (`processed_data`).

---

#### → **Final Output data for Analysis**
- Concatenates all processed chunks into a single dataframe.
- Saves the final preprocessed dataset as `preprocessed_full.csv`.

---

### 3 → `data_plotter_1.py`

- Loads the final preprocessed dataset from `preprocessed_full.csv`.
- Computes the distribution of tweets across three sentiment levels:
  - `low`
  - `moderate`
  - `high`
- Uses Plotly to create a **bar chart** showing the number of tweets in each sentiment category.
- Colors are mapped as:
  - `low` → skyblue  
  - `moderate` → blue  
  - `high` → purple
- Customizes the chart layout with axis labels, title, font sizes, and legend.
- Saves the generated chart as `sentiment_level.jpeg`.
- Displays the chart using `fig.show()`.

> This visualization helps in understanding the overall sentiment distribution in the dataset.

![sentiment_level](https://github.com/user-attachments/assets/1db905da-7724-457a-8544-a36fe040441b)

### 4 → `data_plotter_2.py` and `data_analyzer_1.py`
-`data_analyzer_1.py`
- Loads the final preprocessed dataset from `preprocessed_full.csv`.
- Filters the dataset to include only tweets with **`high`** sentiment (potential high-risk posts).
- Applies **TF-IDF vectorization** to extract the most relevant terms from high-risk tweets:
  - Uses `TfidfVectorizer` with English stop words and `max_features=50` (you can increase `max_features` for more terms).
  - Computes the TF-IDF score for each term across all high-risk tweets.
- Sorts the terms based on their TF-IDF scores in descending order and prints the top 10 terms with the highest scores.
- 
-`data_plotter_2.py`
- Loads the final preprocessed dataset from `preprocessed_full.csv`.
- Filters the dataset to include only tweets with **`high`** sentiment (potential high-risk posts).
- Applies **TF-IDF vectorization** to extract the most relevant terms from high-risk tweets:
  - Uses `TfidfVectorizer` with English stop words and `max_features=50` (you can increase `max_features` for more terms).
  - Computes the TF-IDF score for each term across all high-risk tweets.
- Sorts the terms based on their TF-IDF scores in descending order and prints the top 10 terms with the highest scores.

> This analysis identifies the most significant words associated with high-risk tweets, providing insights into language patterns indicative of a mental health crisis.
'

- Loads the final preprocessed dataset from `preprocessed_full.csv`.
- Filters the dataset to include only tweets labeled with **`high`** sentiment (potential high-risk posts).
- Applies **TF-IDF vectorization** to extract the most relevant terms from high-risk tweets:
  - Uses `TfidfVectorizer` with English stop words and `max_features=50`.
  - Computes the top 10 terms based on TF-IDF scores.
- Creates a **bar chart** using Plotly Express:
  - X-axis: top terms
  - Y-axis: TF-IDF score
  - Color scale: `Reds` to highlight intensity of risk-related terms
- Saves the chart as `words_vs_risk.jpeg`.
- Displays the visualization using `fig.show()`.

> This plot highlights the most significant words associated with high-risk tweets, offering insights into language patterns that may indicate a mental health crisis.

![words_vs_risk](https://github.com/user-attachments/assets/4f9d7889-1086-4185-b8e8-6630384a6860)

### 5 → `plotter_3.py`

- Loads the final preprocessed dataset from `preprocessed_full.csv`.
- **Groups** the data by country and counts the number of tweets from each country.
- **Converts** the two-letter country codes (`alpha-2`) to three-letter country codes (`alpha-3`) using the `pycountry` library.
- **Drops** any rows where the country code could not be mapped to a valid three-letter code.
- Creates a **choropleth map** using Plotly Express:
  - Locations: three-letter country codes
  - Color scale: `Reds` to show tweet activity intensity by country
  - Hover information: country name
- Saves the generated map as `countries_with_risk.jpeg`.
- Displays the map using `fig.show()`.

> This visualization provides a location-based view of tweet activity, highlighting the global distribution of high-risk tweets based on sentiment and activity levels.

![countries_vs_risk](https://github.com/user-attachments/assets/e73dd07a-922b-4461-b0df-104982c2b664)

(Refer to the code (data_plotter_3.py) directly for an interactive webpage of the heatmap).

### 6 → `plotter_4.py`

- Loads the final preprocessed dataset from `preprocessed_full.csv`.
- Filters the dataset to include only tweets with a **`high`** sentiment (potential high-risk posts).
- **Groups** the filtered data by country and counts the number of high-risk tweets from each country.
- **Converts** two-letter country codes (`alpha-2`) to three-letter country codes (`alpha-3`) using the `pycountry` library.
- **Drops** rows where the country code could not be mapped to a valid three-letter code.
- Creates a **choropleth map** using Plotly Express:
  - Locations: three-letter country codes
  - Color scale: `Reds` to show intensity of high-risk tweet activity by country
  - Hover information: country name
- Saves the generated map as `countries_with_high_risk.jpeg`.
- Displays the map using `fig.show()`.

> This visualization helps to identify the global distribution of high-risk tweets, indicating where there might be an increased need for mental health support based on tweet activity.

![countries_with_high_risk](https://github.com/user-attachments/assets/26bc3e7c-9c27-4bdb-aba1-4794ecceb768)

### 7 → `month_neg.py.py`

- Loads the final preprocessed dataset from `preprocessed_full.csv`.
- Converts the `date_time` column to a **datetime** format and drops rows with invalid or missing date values.
- Initializes the **VADER sentiment analyzer** to compute the negativity score of each tweet.
  - **Negativity** is measured using VADER's sentiment polarity score, focusing on negative sentiment.
- Extracts the **month name** from the `date_time` column (e.g., January, February).
- Groups the data by **month** and calculates the **average negativity score** for each month.
- Saves the **average negativity by month** to `monthwise_avg_negativity.csv`.
- Creates a **bar chart** using Plotly Express:
  - X-axis: Month
  - Y-axis: Average negative sentiment score
  - Color scale: `Blues` to represent sentiment intensity
- Configures the layout for better readability, including angle for month labels and bar gap.
- Displays the plot using `fig.show()`.

> This visualization provides insights into how negative sentiment in tweets fluctuates month-by-month, helping to identify trends in sentiment over time.

![Screenshot from 2025-04-09 01-07-57](https://github.com/user-attachments/assets/1cd792a8-3379-426f-93fd-909353f69a57)

### 8 → `table_plot.py`

- **Creates a PDF report** with a table displaying the top countries based on tweet counts from the dataset.
- The data includes:
  - S.No.
  - Country Code
  - Count of high-risk tweets
  - Country Name
- Uses the **ReportLab** library to generate the PDF:
  - Sets the page size to **letter**.
  - Creates a **table** and applies styles (background color, text color, alignment, font, padding).
  - Includes **gridlines** around the table for better readability.
- Saves the generated PDF as `Top_Countries_Report.pdf`.

> This script generates a clean, formatted PDF report listing the top countries with the highest counts of high-risk tweets, which can be used for reporting or analysis.


![Screenshot from 2025-04-12 13-31-28](https://github.com/user-attachments/assets/88a9f669-dbff-4441-a5bc-f576af7eb6c5)
