const { contextBridge, ipcRenderer } = require('electron');
window.ipcRenderer = ipcRenderer;
contextBridge.exposeInMainWorld('electron', {
  fetchLinks: () => fetch('http://localhost:5000/links').then(response => response.json()),
  downloadFile: (url, downloadDirectory) => fetch('http://localhost:5000/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url, downloadDirectory })
  }).then(response => response.json())
});
