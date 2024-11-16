import numpy as np
import os
import pandas as pd
from Scraper import (
    newsguard_scores_high, newsguard_scores_low,
    color_entropy_low, color_entropy_high,
    donate_count_high, bold_terms_count_high,
    donate_count_low, bold_terms_count_low,
    img_count_low, img_count_high,
    low_labels, high_labels
)

# Namenslisten für die Ausgabe
data_lists = [
    newsguard_scores_low, newsguard_scores_high,
    color_entropy_low, color_entropy_high,
    donate_count_low, donate_count_high,
    bold_terms_count_low, bold_terms_count_high,
    img_count_low, img_count_high
]
name_list = [
    "Newsguard_Scores_low", "Newsguard_Scores_high",
    "Unique_colors_low", "Unique_colors_high",
    "Donate_Count_low", "Donate_Count_high",
    "Bold_Terms_Count_low", "Bold_Terms_Count_high",
    "Image_Count_low", "Image_Count_high"
]

# Schritt 1: Bestimmen der Mindestanzahl von Artikeln
num_articles = min(len(lst) for lst in data_lists)


# Funktion zur Berechnung der Abstandsmatrix
def calculate_distance_matrix(data_list):
    distance_matrix = np.zeros((num_articles, num_articles))

    for i in range(num_articles):
        for j in range(i + 1, num_articles):
            if data_list[i] is not None and data_list[j] is not None:
                distance = abs(data_list[i] - data_list[j])
            else:
                distance = 0
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance

    return distance_matrix


# Schritt 2: Berechnen und Speichern jeder Abstandsmatrix in CSV

# Erstelle den 'rdms' Ordner im Projektverzeichnis
# current_dir ermittelt das Verzeichnis, in dem sich das aktuelle Skript befindet
current_dir = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(current_dir, 'rdms')
os.makedirs(output_directory, exist_ok=True)

for idx, data_list in enumerate(data_lists):
    # Abstandsmatrix berechnen
    distance_matrix = calculate_distance_matrix(data_list)
    matrix_df = pd.DataFrame(distance_matrix)

    # Labels hinzufügen
    if "high" in name_list[idx]:
        labels = low_labels[:num_articles]
    else:
        labels = high_labels[:num_articles]

    matrix_df.columns = labels
    matrix_df.index = labels
    matrix_df.index.name = "articles"

    # CSV-Datei speichern im 'rdms' Ordner
    output_path = os.path.join(output_directory, f"{name_list[idx]}_distance_matrix.csv")
    matrix_df.to_csv(output_path, index=True)
    print(f"CSV-Datei für {name_list[idx]} erfolgreich erstellt unter {output_path}.")

