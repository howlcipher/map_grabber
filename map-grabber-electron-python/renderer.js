const { ipcRenderer } = require('electron');
document.addEventListener('DOMContentLoaded', () => {
  const listBox = document.getElementById('listBox');
  const downloadDirectoryInput = document.getElementById('downloadDirectory');
  const browseButton = document.getElementById('browseButton');
  const downloadButton = document.getElementById('downloadButton');
  const errorMsg = document.getElementById('errorMsg');
  const defaultDownloadDirectory = 'C:/Program Files (x86)/Steam/steamapps/common/Left 4 Dead 2/left4dead2/addons';

  downloadDirectoryInput.value = defaultDownloadDirectory;

  browseButton.addEventListener('click', async () => {
    try {
      console.log('Sending select-directory request');
      const result = await ipcRenderer.invoke('select-directory');
      console.log('Received dialog result:', result);
      const selectedDirectory = result.filePaths[0];
      if (selectedDirectory) {
        downloadDirectoryInput.value = selectedDirectory;
      }
    } catch (error) {
      console.error('Error selecting directory:', error);
      alert('Error selecting directory: ' + error);
    }
  });
  
  // Assuming window.electron.fetchLinks() is working fine
  window.electron.fetchLinks().then(data => {
      const zipLinks = data.links;
      zipLinks.forEach(link => {
          const option = document.createElement('option');
          option.textContent = link.split('/').pop();
          option.value = link;
          listBox.appendChild(option);
      });
  });

  downloadButton.addEventListener('click', async () => {
      const websiteUrl = 'http://spirit.hosted.nfoservers.com'; // Update this with your base URL
      const filename = listBox.value;
      const downloadDirectory = downloadDirectoryInput.value;

      if (!filename) {
          errorMsg.textContent = 'Please select a file.';
          return;
      }

      const downloadLink = `${websiteUrl}/${filename}`; // Construct the download link
      console.log('Downloading:', downloadLink);

      // Call the Python backend to download the file
      try {
          const response = await fetch('http://localhost:5000/download', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ url: downloadLink, downloadDirectory })
          });

          const data = await response.json();
          console.log('Downloaded file path:', data.file_path);
          alert(`Downloaded to: ${data.file_path}`);
      } catch (error) {
          console.error('Error downloading file:', error);
          alert('Error downloading file. Please try again.');
      }
  });
});
