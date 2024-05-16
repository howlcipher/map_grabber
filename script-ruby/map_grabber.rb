require 'net/http'
require 'uri'
require 'nokogiri'
require 'tk'
require 'zip' # Ensure this is correct and in place

# Function to extract file name from URL
def extract_filename(url)
  File.basename(url, ".zip")
end

# Global flag to indicate whether download is in progress
$download_in_progress = false

# Method to lock the application during download
def lock_app
  $download_in_progress = true
  @lock_window = TkToplevel.new { title "Downloading..."; geometry '300x50' }
  frame = TkFrame.new(@lock_window).pack(fill: :both, expand: true)
  @progressbar = Tk::Tile::Progressbar.new(frame) { orient 'horizontal'; mode 'determinate' }.pack(pady: 10)
  @progressbar.configure(:maximum => 100)
end

# Method to unlock the application after download completes
def unlock_app
  @lock_window&.destroy
  $download_in_progress = false
end

# Method to create GUI buttons for zip links
def create_buttons(url)
  begin
    root = TkRoot.new { title "Map Grabber"; resizable(false, false) }

    root.geometry("400x600") # Set fixed window dimensions to 400x600
    

    # Default download directory
    default_download_directory = 'C:/Program Files (x86)/Steam/steamapps/common/Left 4 Dead 2/left4dead2/addons'

    # Frame for addons directory
    dir_frame = TkFrame.new(root).pack(side: :top, fill: :x)
    TkLabel.new(dir_frame) { text 'Addons Directory:' }.pack(side: :left, padx: 5, pady: 5)
    download_directory = TkVariable.new(default_download_directory)
    download_entry = TkEntry.new(dir_frame) { width 30; textvariable download_directory }.pack(side: :left, padx: 5, pady: 5)
    TkButton.new(dir_frame) { text 'Browse'; command { download_directory.value = Tk.chooseDirectory } }.pack(side: :left, padx: 5, pady: 5)

    TkFrame.new(root) { relief 'ridge'; borderwidth 2 }.pack(side: :top, fill: :x, padx: 5, pady: 5)

    # Frame for map buttons
    map_frame = TkFrame.new(root).pack(side: :top, fill: :both, expand: true)
    scrollbar = TkScrollbar.new(map_frame) { pack(side: :right, fill: :y) }
    listbox = TkListbox.new(map_frame, yscrollcommand: proc { |*args| scrollbar.set(*args) }) do
      pack(side: :left, fill: :both, expand: true)
    end
    scrollbar.command(proc { |*args| listbox.yview(*args) })

    uri = URI.parse(url)
    response = Net::HTTP.get_response(uri)

    if response.is_a?(Net::HTTPSuccess)
      doc = Nokogiri::HTML(response.body)
      zip_links = doc.css('a[href$=".zip"]')

      # Sort zip links alphabetically
      zip_links = zip_links.sort_by { |link| extract_filename(link['href']) }

      zip_links.each_with_index do |link, index|
        filename = extract_filename(link['href'])
        listbox.insert('end', filename)
      end
    else
      puts "Failed to fetch the URL: #{response.message}"
    end

    # Binding double-click event to handle the action
    listbox.bind('Double-1', proc { |event| on_double_click(event, listbox, url, download_directory) })

    Tk.mainloop
  rescue StandardError => e
    puts "An error occurred: #{e.message}"
    puts e.backtrace
  end
end

# Method to handle the double-click action
def on_double_click(event, listbox, website_url, download_directory)
  return if $download_in_progress
  
  index = listbox.index('active') # Get the index of the clicked item
  if index
    filename = listbox.get(index) # Get the filename from the listbox
    download_link = "#{website_url}/#{filename}.zip" # Construct the download link

    # Display the download link in a message box
    Tk.messageBox(
      'type'    => "ok",
      'icon'    => "info",
      'title'   => "Download Link",
      'message' => "Downloading: #{download_link}"
    )

    # Lock the application during download
    lock_app

    # Download the file
    download_file(download_link, filename, download_directory)

    # Unzip the file and move its contents to the download directory
    unzip_and_move_file(filename, download_directory)

    # Unlock the application after download completes
    unlock_app
  end
end

# Method to download the file
def download_file(url, filename, download_directory)
  uri = URI.parse(url)
  Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == 'https') do |http|
    request = Net::HTTP::Get.new(uri)
    http.request(request) do |response|
      total_size = response['content-length'].to_i
      downloaded = 0

      File.open("#{download_directory}/#{filename}.zip", 'wb') do |file|
        response.read_body do |chunk|
          file.write(chunk)
          downloaded += chunk.bytesize
          percent = (downloaded.to_f / total_size * 100).to_i
          @progressbar.value = percent # Update progress bar
          Tk.update # Keep GUI responsive
        end
      end
    end
  end
end

# Method to unzip the downloaded file and move its contents to the download directory
def unzip_and_move_file(filename, download_directory)
  zip_file_path = "#{download_directory}/#{filename}.zip"
  
  Zip::File.open(zip_file_path) do |zip_file|
    zip_file.each do |entry|
      # Construct the destination path (same as download directory)
      destination_path = File.join(download_directory, entry.name)

      # Skip extraction if the file already exists
      next if File.exist?(destination_path)

      # Ensure that the parent directory of the entry exists
      FileUtils.mkdir_p(File.dirname(destination_path))

      # Extract the entry
      entry.extract(destination_path)
    end
  end

  # Delete the downloaded ZIP file after extraction
  File.delete(zip_file_path) if File.exist?(zip_file_path)
end

# Define website_url here or pass it as an argument to create_buttons
website_url = "http://spirit.hosted.nfoservers.com"

# Call the function to create GUI buttons for zip links
create_buttons(website_url)
