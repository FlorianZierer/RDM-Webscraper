from selenium import webdriver
import time


def capture_screenshot_safari(url, output_path="screenshot.png"):
    # Starte den Safari WebDriver
    driver = webdriver.Safari()

    try:
        driver.set_window_size(980, 800)  # Fenstergröße auf 980 x 800 Pixel setzen
        driver.get(url)  # Webseite öffnen
        time.sleep(2)  # Warten, bis die Seite vollständig geladen ist
        driver.save_screenshot(output_path)  # Screenshot speichern
        print(f"Screenshot gespeichert unter: {output_path}")
    finally:
        driver.quit()  # Browser schließen


# Beispielaufruf
capture_screenshot_safari("https://gellerreport.com/2024/11/steel-city-terror-national-guard-member-is-hamas-terrorist-mohamad-hamad-bought-explosives-for-fireball-bomb-vandalized-jewish-buildings-donated-to-jihad-squad-democrats.html/", "/Users/florianzierer/Desktop/screenshot.png")
