import numpy as np
import os
import pandas as pd
from Scraper import (
    newsguard_scores_high, newsguard_scores_low,
    color_entropy_high, color_entropy_low,
    donate_count_high, donate_count_low,
    bold_terms_count_high, bold_terms_count_low,
    img_count_high, img_count_low,
    high_labels, low_labels
)

# Liste von Tupeln mit High- und Low-Daten sowie dem Parametername
data_tuples = [
    (newsguard_scores_high, newsguard_scores_low, 'Newsguard_Scores'),
    (color_entropy_high, color_entropy_low, 'Unique_colors'),
    (donate_count_high, donate_count_low, 'Donate_Count'),
    (bold_terms_count_high, bold_terms_count_low, 'Bold_Terms_Count'),
    (img_count_high, img_count_low, 'Image_Count')
]

# Erstelle den 'rdms' Ordner im Projektverzeichnis
current_dir = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(current_dir, 'rdms')
os.makedirs(output_directory, exist_ok=True)

# Für jeden Parameter die High- und Low-Daten kombinieren und die Abstandsmatrix berechnen
for high_data, low_data, param_name in data_tuples:
    # Kombiniere die High- und Low-Daten sowie die Labels
    data_combined = high_data + low_data
    labels_combined = low_labels + high_labels

    # Überprüfe, ob die Längen übereinstimmen
    if len(data_combined) != len(labels_combined):
        min_length = min(len(data_combined), len(labels_combined))
        data_combined = data_combined[:min_length]
        labels_combined = labels_combined[:min_length]

    total_articles = len(data_combined)

    # Abstandsmatrix berechnen
    distance_matrix = np.zeros((total_articles, total_articles))
    for i in range(total_articles):
        for j in range(i + 1, total_articles):
            if data_combined[i] is not None and data_combined[j] is not None:
                distance = abs(data_combined[i] - data_combined[j])
            else:
                distance = 0
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    # DataFrame erstellen und Labels hinzufügen
    matrix_df = pd.DataFrame(distance_matrix)
    matrix_df.columns = labels_combined
    matrix_df.index = labels_combined
    matrix_df.index.name = "articles"

    # CSV-Datei speichern
    output_path = os.path.join(output_directory, f"{param_name}_distance_matrix.csv")
    matrix_df.to_csv(output_path, index=True)
    print(f"CSV-Datei für {param_name} erfolgreich erstellt unter {output_path}.")