import pandas as pd

# Load the dataset
movies = pd.read_csv("imdb_top_1000.csv")

# Cleaning the columns
movies["Series_Title"] = movies["Series_Title"].str.strip()
movies["Certificate"] = movies["Certificate"].str.strip()
movies["Genre"] = movies["Genre"].str.strip()
movies["Overview"] = movies["Overview"].str.strip()
movies["Director"] = movies["Director"].str.strip()
movies["Star1"] = movies["Star1"].str.strip()
movies["Star2"] = movies["Star2"].str.strip()
movies["Star3"] = movies["Star3"].str.strip()
movies["Star4"] = movies["Star4"].str.strip()

# Concatenating the columns needed for embedding
movies["clean_text"] = movies["Series_Title"] + " " + movies["Overview"] + " " + movies["Genre"] + " " + movies["Director"] + " " + movies["Star1"] + " " + movies["Star2"] + " " + movies["Star3"] + " " + movies["Star4"]

# Creating a new column - (concateneted) clean text
cleaned_data = movies[["Series_Title", "Overview", "clean_text"]]

# Saving cleaned dataset
cleaned_data.to_csv("cleaned_data.csv", index=False)
