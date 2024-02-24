# PubScraper

PubScraper is a simple Python script designed to scrape publisher information from the Swedish ISBN database website (https://isbn.kb.se/sok/). The script navigates through the website, page by page, collecting information about publishers, including their names, email addresses, and websites, and then sends this data to a specified Google Sheet via a Google Apps Script web app for easy storage and access.

## Technologies Used

- Python 3: The core programming language used for the script.
- Beautiful Soup: A Python library for parsing HTML and XML documents. It's used to extract the data from the web pages.
- Requests: A Python library used to make HTTP requests. This is used for both scraping the website and sending data to the Google Apps Script web app.
- Google Sheets and Google Apps Script: For storing the scraped data in an accessible and easy-to-manage format.

## Getting Started

To use PubScraper, follow these steps:

### Prerequisites

- Python 3 installed on your machine.
- Pip (Python package installer) for installing the necessary Python libraries.
- Access to Google Sheets and the ability to create a Google Apps Script web app.

### Installation

1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/uchusei/pubscraper.git

2. Navigate to the cloned repository:
   ```sh
   cd pubscraper
   
3. Install the required Python libraries:
   ```sh
   pip install beautifulsoup4 requests

### Configuration

1. Create a Google Apps Script web app following the instructions provided in the Google Apps Script documentation. The script should be designed to accept POST requests and write the data to a Google Sheet. Example:
```javascript
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Scraping');
  var data = JSON.parse(e.postData.contents);
  sheet.appendRow([data.name, data.email, data.web]);
  return ContentService.createTextOutput(JSON.stringify({"result": "success"}))
    .setMimeType(ContentService.MimeType.JSON);
}
```
2. Update the `web_app_url` variable in the script with the URL of your Google Apps Script web app.

### Running the Script
Execute the script by running:
   ```sh
   python3 pubscraper_kb.py
```

## Modifying the Code
The script can be easily modified to fit specific needs, such as changing the source website, adjusting the data being scraped, or altering the destination for the scraped data. To modify the list of excluded email domains, adjust the if condition that filters out certain email addresses based on their domains.

## Note
This script is a simple demonstration of web scraping and automated data entry into Google Sheets. It's intended for educational and non-commercial use, and users should ensure they have permission to scrape the website in question and comply with any relevant terms of service.
