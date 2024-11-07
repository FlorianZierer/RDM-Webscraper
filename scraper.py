import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from selenium import webdriver
from PIL import Image
import numpy as np
from scipy.stats import entropy
import io

url = "https://www.foxnews.com/live-news/donald-trump-kamala-harris-election-news-11-3-24"


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


def take_screenshot(url):
    """
    Öffnet die Seite mit Selenium und macht einen Screenshot
    """
    driver = webdriver.Chrome()
    driver.get(url)

    # Screenshot in Bytes speichern
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    return Image.open(io.BytesIO(screenshot))


def calculate_color_entropy(image):
    """
    Berechnet die Farbentropie eines Bildes
    """
    image_data = np.array(image.convert('RGB'))
    unique_colors, counts = np.unique(image_data.reshape(-1, 3), axis=0, return_counts=True)
    return entropy(counts)


def analyze_webpage(url):
    """Hauptfunktion zur Analyse der Webseite"""
    try:
        response = requests.get(url)
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

        # Screenshot machen, Farbentropie berechnen und Screenshot löschen
        screenshot = take_screenshot(url)
        color_entropy = calculate_color_entropy(screenshot)
        print(f"\nFarbentropie des Screenshots: {color_entropy}")

        # Speicher freigeben, indem das Bild gelöscht wird
        screenshot.close()

    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
        return None

# Funktion aufrufen
analyze_webpage(url)
