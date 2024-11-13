import numpy as np
from Scraper import newsguard_scores_high, newsguard_scores_low, color_entropy_low, color_entropy_high, \
    donate_count_high, bold_terms_count_high, donate_count_low, bold_terms_count_low, img_count_low, img_count_high

# Listen der zu analysierenden Daten
data_lists = [
    newsguard_scores_low, newsguard_scores_high,
    color_entropy_low, color_entropy_high,
    donate_count_low, donate_count_high,
    bold_terms_count_low, bold_terms_count_high,
    img_count_low, img_count_high
]
name_list = ["Newsguard Scores (low)","Newsguard Scores (high)", "Unique colors (low)", "Unique colors (high)", "Donate Count (low)", "Donate Count (high)","Bold Terms Count (low)", "Bold Terms Count (high)","Image Count (low)", "Image Count (high)"]

# Schritt 1: Bestimmen der maximalen Anzahl der Artikel (Artikelanzahl in der längsten Liste)
num_articles = min(len(lst) for lst in data_lists)  # Minimale Länge der Listen, um Indexfehler zu vermeiden


# Funktion zum Berechnen der Distanzmatrix
def calculate_distance_matrix(data_list):
    distance_matrix = np.zeros((num_articles, num_articles))

    # Füllen der Distanzmatrix
    for i in range(num_articles):
        for j in range(i + 1, num_articles):
            distance = abs(data_list[i] - data_list[j]) if data_list[i] is not None and data_list[j] is not None else 0
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance  # symmetrische Matrix

    return distance_matrix


# Schritt 2: Berechnung und Ausgabe der Distanzmatrix für jede Liste
for idx, data_list in enumerate(data_lists):
    print(f"\nDistanzmatrix für " + name_list[idx]+":")
    distance_matrix = calculate_distance_matrix(data_list)
    print(distance_matrix)

    # Extrahieren der oberen Dreiecksmatrix
    upper_triangle = distance_matrix[np.triu_indices(num_articles, 1)]
    print("\nObere Dreiecksmatrix: " + name_list[idx]+":")
    print(upper_triangle)

    # Extrahieren der unteren Dreiecksmatrix
    lower_triangle = distance_matrix[np.tril_indices(num_articles, -1)]
    print("\nUntere Dreiecksmatrix: " + name_list[idx]+":")
    print(lower_triangle)

    print("=" * 50)
