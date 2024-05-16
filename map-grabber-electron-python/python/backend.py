from flask import Flask, jsonify, request
import urllib.request
from bs4 import BeautifulSoup
import os
from zipfile import ZipFile

app = Flask(__name__)

def extract_filename(url):
    return os.path.basename(url).replace(".zip", "")

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    download_directory = data['downloadDirectory']
    filename = extract_filename(url)

    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    file_path = os.path.join(download_directory, f"{filename}.zip")

    def download_file():
        urllib.request.urlretrieve(url, file_path)
        with ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(download_directory)
        os.remove(file_path)

    download_file()
    return jsonify({"status": "success", "file_path": file_path})

@app.route('/links')
def links():
    url = "http://spirit.hosted.nfoservers.com"
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    zip_links = [link.get('href') for link in soup.find_all('a', href=lambda href: href and href.endswith('.zip'))]
    return jsonify({"links": zip_links})

if __name__ == "__main__":
    app.run(port=5000)
