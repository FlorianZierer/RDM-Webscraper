import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
import numpy as np
from scipy.stats import entropy
import csv

filepath = "/Users/florianzierer/Downloads/"

# Dateipfade für "low" und "high" Dateien
high_filepath = filepath + "score_h_95_domains.csv"
low_filepath = filepath + "score_l_75_full.csv"

# Arrays für die gewünschten Daten
low_data = []
high_data = []


# Funktion zum Laden der Daten aus einer CSV-Datei
def load_data(filepath, data_array, cropped_folder):
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            # Ersetze 'url', 'screenshot', und 'newsguard_score' durch die tatsächlichen Spaltennamen in deiner Datei
            url = row.get('url')
            screenshot = row.get('screenshot')
            newsguard_score = row.get('newsguard_score')

            # Füge nur gültige Einträge hinzu und baue den vollen Pfad zum Screenshot
            if url and screenshot and newsguard_score:
                screenshot_path = filepath + cropped_folder + "/" + screenshot
                data_array.append([url, screenshot_path, newsguard_score])


# Daten aus "low" und "high" CSV-Dateien laden, mit entsprechendem Ordnernamen für die Screenshots
load_data(low_filepath, low_data, "low_cropped")
load_data(high_filepath, high_data, "high_cropped")

# Ausgabe der Arrays
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


# Funktion zur Berechnung der Farbentropie eines vorhandenen Bildes
def calculate_color_entropy(image_path):
    image = Image.open(image_path).convert('RGB')
    image_data = np.array(image)
    unique_colors, counts = np.unique(image_data.reshape(-1, 3), axis=0, return_counts=True)
    image.close()
    return entropy(counts)


def analyze_webpage(data):
    """Hauptfunktion zur Analyse der Webseite"""
    try:
        response = requests.get(data.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Fettgedruckte Begriffe analysieren
        bold_text = get_bold_terms(soup)
        print(f"\nAnzahl der fettgedruckten Begriffe: {len(bold_text)}")
        print("Fettgedruckte Begriffe:", bold_text)

        # Bild-Tags zählen
        img_count = count_img_tags(soup)
        print(f"\nAnzahl der Bilder auf der Seite: {img_count}")

        # Vorkommen von 'donate' zählen
        donate_count = count_donate_occurrences(soup)
        print(f"\nAnzahl der Vorkommen von 'donate': {donate_count}")

        color_entropy = calculate_color_entropy(data.screenshot_path)
        print(f"\nFarbentropie des Screenshots: {color_entropy}")


    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
        return None


for data in low_data:
    analyze_webpage(data)

for data in high_data:
    analyze_webpage(data)
