# PubScraper

The PubScraper currently consists of two Python scripts designed for web scraping publisher information from distinct sources: the Swedish ISBN database and the Allabolag.se website. These scripts automate the collection of data such as publisher names, email addresses, and websites, and then forward this information to a Google Sheet via a Google Apps Script web app. This approach simplifies data extraction and management.

## Overview

- `pubscraper_kb.py`: Scrapes publisher information from the Swedish ISBN database (https://isbn.kb.se/sok/), focusing on active publishers and filtering out certain email domains.
- `pubscraper_allabolag.py`: Extracts company names from the Allabolag.se website, specifically targeting the book publishing sector.

## Technologies Used

- **Python 3**: The primary programming language for the scripts.
- **Beautiful Soup**: Utilized for parsing HTML documents, facilitating the extraction of data from web pages.
- **Selenium WebDriver**: Employed for automating web browser interaction in `pubscraper_allabolag.py`, enabling the scraping of JavaScript-rendered content.
- **Requests**: A library for making HTTP requests, used to send scraped data to the Google Apps Script web app and to fetch web pages in `pubscraper_kb.py`.
- **Google Sheets and Google Apps Script**: Serve as the backend for storing the scraped data, offering an accessible and manageable format.

## Getting Started

### Prerequisites

- Ensure Python 3 is installed on your system.
- Have pip available for installing Python libraries.
- A Google account with access to Google Sheets and the ability to create Google Apps Script web apps.

### Installation

1. Clone the repository:
```sh
git clone https://github.com/uchusei/pubscraper.git
```
2. Navigate to the directory:
```sh
cd pubscraper
```
3. Install required libraries:
```sh
pip install beautifulsoup4 selenium requests
```

### Configuration

1. Create a Google Apps Script web app that can accept POST requests and write the received data into a Google Sheet. The script could look something like this:
```javascript
function doPost(e) {
  var postData = JSON.parse(e.postData.contents);
  var sheetName = postData.type === 'KB' ? 'Scraping KB' : 'Scraping Allabolag';
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  
  if(postData.type === 'KB') {
    sheet.appendRow([postData.name, postData.email, postData.web]);
  } else if(postData.type === 'Allabolag') {
    sheet.appendRow([postData.name]);
  }
  
  return ContentService.createTextOutput(JSON.stringify({"result": "success"}))
    .setMimeType(ContentService.MimeType.JSON);
}
```
Update the `web_app_url` in both Python scripts to match the URL of your deployed Google Apps Script web app.

### Running the Scripts

To run the scripts and start the scraping process:
```sh
python3 pubscraper_kb.py
python3 pubscraper_allabolag.py
```

## Customization

Both scripts and the Google Apps Script can be modified to meet specific requirements, like changing the data source, the data being scraped, or the destination Google Sheet. For instance, you can adjust the list of excluded email domains in pubscraper_kb.py by modifying the relevant condition.

## Note

This project is intended for educational and non-commercial use. Users should ensure they are allowed to scrape the chosen websites and comply with any applicable terms of service or legal restrictions.
