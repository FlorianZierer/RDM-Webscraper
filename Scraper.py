import os
import time

import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
import numpy as np
import pandas as pd

filepath = "/Users/florianzierer/Downloads/Testing_images_urls"
articles_filepath = filepath + "/articles.xlsx"

# Arrays für die gewünschten Daten
low_data = []
high_data = []

low_labels = []
high_labels = []


# Function to load data from an Excel file
def load_data(filepath):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(filepath)

    # Regex patterns for "high" and "low" labels
    high_pattern = re.compile(r"h\d+")
    low_pattern = re.compile(r"l\d+")

    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        try:
            # Extract required data
            newsguard_score = f"{row['newsguard']}"
            url = row['url']
            screenshot = str(row['screenshot'])
            label = row['label']

            # Check for missing data
            if not newsguard_score or not url or not screenshot:
                continue

            if ("./screenshots/low/" in screenshot):
                screenshot = screenshot.replace("./screenshots/low/", "")

            # Match label and append to the correct array
            if high_pattern.match(label):
                # Build the screenshot path
                screenshot_path = os.path.join(os.path.dirname(filepath) + "/high_cropped", screenshot)
                high_data.append([url, screenshot_path, float(newsguard_score.replace(",", ".")), label])
                low_labels.append(label)
            elif low_pattern.match(label):
                # Build the screenshot path
                screenshot_path = os.path.join(os.path.dirname(filepath) + "/low_cropped", screenshot)
                low_data.append([url, screenshot_path, float(newsguard_score.replace(",", ".")), label])
                high_labels.append(label)

        except ValueError as e:
            print(f"ValueError at row {index}: {e}")
            continue
        except KeyError as e:
            print(f"KeyError: Missing column '{e.args[0]}' in the DataFrame.")
            break


# Call the function
load_data(articles_filepath)

# Optional: Print results for debugging
print("Low Data:", low_data)
print("High Data:", high_data)


def get_bold_terms(soup):
    """
    Findet alle fettgedruckten Begriffe auf der Seite
    """
    bold_terms = soup.find_all(['b', 'strong'])
    return [term.get_text(strip=True) for term in bold_terms if term.get_text(strip=True)]


def count_img_tags(soup):
    """
    Zählt alle <img>-Tags auf der Seite
    """
    img_tags = soup.find_all("img")
    return len(img_tags)


def count_donate_occurrences(soup):
    """
    Zählt die Vorkommen von 'donate' oder 'donat...' auf der Seite.
    """
    text = soup.get_text().lower()
    matches = re.findall(r'\bdonat\w*', text)  # 'donat...' findet Wörter, die mit 'donat' beginnen
    return len(matches)


# Funktion zur Berechnung der Farbvorkommen
from PIL import Image
import numpy as np


def count_unique_colors(image_path):
    try:
        image = Image.open(image_path).convert('RGB')  # Bild öffnen und in RGB konvertieren
        image_data = np.array(image)  # Bilddaten in ein Numpy-Array umwandeln
        unique_colors = np.unique(image_data.reshape(-1, 3), axis=0)  # Einzigartige Farben finden
        return len(unique_colors)  # Anzahl der einzigartigen Farben zurückgeben
    except FileNotFoundError:
        print(f"File not found: {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Listen zur Speicherung der analysierten Daten
newsguard_scores_low, newsguard_scores_high = [], []
color_entropy_low, color_entropy_high = [], []
donate_count_low, donate_count_high = [], []
bold_terms_count_low, bold_terms_count_high = [], []
img_count_low, img_count_high = [], []


def analyze_webpage(data, score_list, entropy_list, donate_list, bold_list, img_list):
    """Main function to analyze the webpage"""
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/70.0.3538.77 Safari/537.36')
        }
        response = requests.get(data[0], headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract bold terms
        bold_text = get_bold_terms(soup)
        bold_list.append(len(bold_text))

        # Count image tags
        img_count = count_img_tags(soup)
        img_list.append(img_count)

        # Count 'donate' occurrences
        donate_count = count_donate_occurrences(soup)
        donate_list.append(donate_count)

        # Compute colour Vorkommen
        color_vorkommen = count_unique_colors(data[1])
        entropy_list.append(color_vorkommen)

        # Append Newsguard score
        score_list.append(data[2])

        # Rate limiting
        time.sleep(1)  # Sleep for 1 second

    except requests.HTTPError as e:
        print(f"HTTP Error {e.response.status_code} for URL: {data[0]}")
    except requests.RequestException as e:
        print(f"Error fetching {data[0]}: {e}")


# Webseiten in low_data und high_data analysieren und Listen befüllen
print("Analysiere Webseiten in low_data...")
for data in low_data:
    analyze_webpage(data, newsguard_scores_low, color_entropy_low, donate_count_low, bold_terms_count_low,
                    img_count_low)

print("\nAnalysiere Webseiten in high_data...")
for data in high_data:
    analyze_webpage(data, newsguard_scores_high, color_entropy_high, donate_count_high, bold_terms_count_high,
                    img_count_high)

# Ausgabe der Ergebnisse
print("\nNewsguard Scores (low):", newsguard_scores_low)
print("Newsguard Scores (high):", newsguard_scores_high)
print("\nUnique colours (low):", color_entropy_low)
print("Unique colours (high):", color_entropy_high)
print("\nDonate Count (low):", donate_count_low)
print("Donate Count (high):", donate_count_high)
print("\nBold Terms Count (low):", bold_terms_count_low)
print("Bold Terms Count (high):", bold_terms_count_high)
print("\nImage Count (low):", img_count_low)
print("Image Count (high):", img_count_high)
