import numpy as np
import pandas as pd
from Scraper import newsguard_scores_high, newsguard_scores_low, color_entropy_low, color_entropy_high, \
    donate_count_high, bold_terms_count_high, donate_count_low, bold_terms_count_low, img_count_low, img_count_high

# Lists of data to analyze
data_lists = [
    newsguard_scores_low, newsguard_scores_high,
    color_entropy_low, color_entropy_high,
    donate_count_low, donate_count_high,
    bold_terms_count_low, bold_terms_count_high,
    img_count_low, img_count_high
]
name_list = ["Newsguard_Scores_low", "Newsguard_Scores_high", "Unique_colors_low", "Unique_colors_high",
             "Donate_Count_low", "Donate_Count_high", "Bold_Terms_Count_low", "Bold_Terms_Count_high",
             "Image_Count_low", "Image_Count_high"]

# Step 1: Determine the maximum number of articles (based on the shortest list to avoid index errors)
num_articles = min(len(lst) for lst in data_lists)


# Function to calculate the distance matrix
def calculate_distance_matrix(data_list):
    distance_matrix = np.zeros((num_articles, num_articles))

    # Filling the distance matrix
    for i in range(num_articles):
        for j in range(i + 1, num_articles):
            distance = abs(data_list[i] - data_list[j]) if data_list[i] is not None and data_list[j] is not None else 0
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance  # symmetric matrix

    return distance_matrix


# Step 2: Calculate and save each distance matrix to a CSV file
for idx, data_list in enumerate(data_lists):
    # Calculate distance matrix
    distance_matrix = calculate_distance_matrix(data_list)

    # Save the full distance matrix to CSV
    matrix_df = pd.DataFrame(distance_matrix)
    matrix_df.to_csv(f"{name_list[idx]}_distance_matrix.csv", index=False)

    # Extract and save upper triangle
    upper_triangle = distance_matrix[np.triu_indices(num_articles, 1)]
    upper_triangle_df = pd.DataFrame(upper_triangle)
    upper_triangle_df.to_csv(f"{name_list[idx]}_upper_triangle.csv", index=False)

    # Extract and save lower triangle
    lower_triangle = distance_matrix[np.tril_indices(num_articles, -1)]
    lower_triangle_df = pd.DataFrame(lower_triangle)
    lower_triangle_df.to_csv(f"{name_list[idx]}_lower_triangle.csv", index=False)

    print(f"CSV files for {name_list[idx]} created successfully.")
