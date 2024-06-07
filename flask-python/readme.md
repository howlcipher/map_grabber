# Map Downloader

This application allows users to download maps for a game. It's built using Python Flask framework and utilizes BeautifulSoup for web scraping.

## Requirements

- Python 3.x
- Flask
- BeautifulSoup
- Werkzeug

## Installation

1. Clone or download the repository.
2. Install the required Python packages using pip: `pip install flask beautifulsoup4`

## Usage

1. Run the Flask server:`python app.py`

2. Open a web browser and navigate to `http://localhost:5000/` to access the application.

3. You'll see a list of available maps. Click the "Download" button next to the desired map to start downloading.

4. You will be prompted to enter the download directory. Provide the directory path and click OK.

5. The download will start, and you will receive a notification when it's complete.

## Files

- `app.py`: Contains the Flask application code.
- `index.html`: HTML template for the web interface.

