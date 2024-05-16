import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import urllib.request
import os
from zipfile import ZipFile
from bs4 import BeautifulSoup
import threading

# Function to extract file name from URL
def extract_filename(url):
    return os.path.basename(url).replace(".zip", "")

# Global flag to indicate whether download is in progress
download_in_progress = False

# Method to lock the application during download
def lock_app():
    global download_in_progress
    download_in_progress = True
    lock_window = tk.Toplevel()
    lock_window.title("Downloading...")
    lock_window.geometry('300x50')
    frame = ttk.Frame(lock_window)
    frame.pack(fill='both', expand=True)
    progressbar = ttk.Progressbar(frame, orient='horizontal', mode='determinate')
    progressbar.pack(pady=10)
    progressbar.configure(maximum=100)
    return progressbar, lock_window

# Method to unlock the application after download completes
def unlock_app(progressbar, lock_window):
    global download_in_progress
    download_in_progress = False
    lock_window.destroy()

# Method to create GUI buttons for zip links
def create_buttons(url):
    try:
        root = tk.Tk()
        root.title("Map Grabber")
        root.geometry("400x600")
        root.resizable(False, False)

        # Default download directory
        default_download_directory = 'C:/Program Files (x86)/Steam/steamapps/common/Left 4 Dead 2/left4dead2/addons'

        # Frame for addons directory
        dir_frame = ttk.Frame(root)
        dir_frame.pack(side='top', fill='x')
        ttk.Label(dir_frame, text='Addons Directory:').pack(side='left', padx=5, pady=5)
        download_directory = tk.StringVar(value=default_download_directory)
        download_entry = ttk.Entry(dir_frame, width=30, textvariable=download_directory)
        download_entry.pack(side='left', padx=5, pady=5)
        ttk.Button(dir_frame, text='Browse', command=lambda: select_directory(download_directory)).pack(side='left', padx=5, pady=5)

        ttk.Frame(root, relief='ridge', borderwidth=2).pack(side='top', fill='x', padx=5, pady=5)

        # Frame for map buttons
        map_frame = ttk.Frame(root)
        map_frame.pack(side='top', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(map_frame)
        scrollbar.pack(side='right', fill='y')
        listbox = tk.Listbox(map_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=listbox.yview)

        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response, 'html.parser')
        zip_links = soup.find_all('a', href=lambda href: href and href.endswith('.zip'))

        # Sort zip links alphabetically
        zip_links = sorted(zip_links, key=lambda link: extract_filename(link['href']))

        for link in zip_links:
            filename = extract_filename(link['href'])
            listbox.insert('end', filename)

        # Binding double-click event to handle the action
        listbox.bind('<Double-1>', lambda event: on_double_click(event, listbox, url, download_directory))

        root.mainloop()
    except Exception as e:
        print("An error occurred:", e)

# Function to select directory and create the addons folder if it doesn't exist
def select_directory(download_directory):
    directory = filedialog.askdirectory()
    if directory:
        download_directory.set(directory)
        addons_folder = os.path.join(directory, "addons")
        if not os.path.exists(addons_folder):
            os.makedirs(addons_folder)
            messagebox.showinfo("Directory Created", f"The directory {addons_folder} was created.")

# Method to handle the double-click action
def on_double_click(event, listbox, website_url, download_directory):
    global download_in_progress
    if not download_in_progress:
        index = listbox.curselection()  # Get the index of the clicked item
        if index:
            filename = listbox.get(index)  # Get the filename from the listbox
            download_link = f"{website_url}/{filename}.zip"  # Construct the download link

            # Display the download link in a message box
            messagebox.showinfo("Download Link", f"Downloading: {download_link}")

            # Lock the application during download
            progressbar, lock_window = lock_app()

            # Download the file in a separate thread
            threading.Thread(target=download_file, args=(download_link, filename, download_directory.get(), progressbar, lock_window)).start()

# Method to download the file
def download_file(url, filename, download_directory, progressbar, lock_window):
    def update_progress(blocknum, block_size, total_size):
        nonlocal downloaded
        downloaded += block_size
        percent = (downloaded / total_size) * 100
        progressbar['value'] = percent
        progressbar.update_idletasks()

    downloaded = 0
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info()['Content-Length'])
        urllib.request.urlretrieve(url, os.path.join(download_directory, f"{filename}.zip"), reporthook=update_progress)

    # Unzip the file
    unzip_file(filename, download_directory)

    # Unlock the application after download completes
    unlock_app(progressbar, lock_window)

# Method to unzip the downloaded file and move its contents to the download directory
def unzip_file(filename, download_directory):
    zip_file_path = os.path.join(download_directory, f"{filename}.zip")
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(download_directory)

    # Delete the downloaded ZIP file after extraction
    os.remove(zip_file_path)

# Define website_url here or pass it as an argument to create_buttons
website_url = "http://spirit.hosted.nfoservers.com"

# Call the function to create GUI buttons for zip links
create_buttons(website_url)
