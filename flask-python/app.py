from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import urllib.request
from zipfile import ZipFile
from bs4 import BeautifulSoup
import threading
from werkzeug.utils import safe_join

app = Flask(__name__)

# Function to extract file name from URL
def extract_filename(url):
    return os.path.basename(url).replace(".zip", "")

# Function to download and unzip the file
def download_and_unzip(url, download_directory):
    filename = extract_filename(url)
    file_path = os.path.join(download_directory, f"{filename}.zip")
    
    urllib.request.urlretrieve(url, file_path)

    # Unzip the file
    with ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(download_directory)

    # Delete the downloaded ZIP file after extraction
    os.remove(file_path)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_maps')
def fetch_maps():
    website_url = "http://spirit.hosted.nfoservers.com"
    response = urllib.request.urlopen(website_url)
    soup = BeautifulSoup(response, 'html.parser')
    zip_links = soup.find_all('a', href=lambda href: href and href.endswith('.zip'))
    
    maps = sorted([extract_filename(link['href']) for link in zip_links])
    return jsonify(maps)

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    download_directory = request.args.get('directory', 'downloads')
    
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    website_url = "http://spirit.hosted.nfoservers.com"
    download_link = f"{website_url}/{filename}.zip"
    
    # Download and unzip file in a separate thread
    threading.Thread(target=download_and_unzip, args=(download_link, download_directory)).start()
    
    return jsonify({"status": "Downloading"})

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    download_directory = request.args.get('directory', 'downloads')
    download_directory = os.path.abspath(download_directory)

    if not os.path.exists(download_directory):
        return jsonify({"error": "Directory does not exist"}), 404

    # Provide the direct download link for the zip file
    file_path = safe_join(download_directory, f"{filename}.zip")
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    return send_from_directory(download_directory, f"{filename}.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
