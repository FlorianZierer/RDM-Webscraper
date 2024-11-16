# RDM-Webscraper

This tool accesses web pages, parses, and filters the content to retrieve only the relevant parameters, and saves the processed data for analysis.

## Data Collection Overview

### Data Selection Criteria:
- **Bold Terms**: Identified using the `<strong>` HTML tag.
- **Image Tags**: Extracted via the `<img>` HTML tag.
- **Donation Options**: Located by searching for keywords such as "donat" and "Donat" in the page content.

### Manual Data Collection:
For this project, all data was collected manually to ensure accuracy when automated access was restricted. This approach enabled the retrieval of relevant content despite technical limitations.

### Preservation of Original Structure:
By not normalizing the articles, the original structure and presentation of each webpage were retained. This method ensures an authentic representation of how content is displayed to readers, allowing meaningful analysis of naturally occurring elements like image counts and bold terms without imposing artificial uniformity.

## Data Storage:
The collected data is saved in **CSV files** that represent:

- **Low-Quality Website Data**
- **High-Quality Website Data**

These datasets are represented as **distance matrices**, allowing for quantitative comparison and analysis of the differences between low- and high-quality website structures and features.

### Special Case:
For the **[Geller Report](https://gellerreport.com/2024/11/steel-city-terror-national-guard-member-is-hamas-terrorist-mohamad-hamad-bought-explosives-for-fireball-bomb-vandalized-jewish-buildings-donated-to-jihad-squad-democrats.html/)** website, a Python script was developed to take a screenshot, ensuring consistency with the other websites since the original screenshot was missing.
