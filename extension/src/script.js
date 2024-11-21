document.getElementById('start-recording').addEventListener('click', startRecording);
document.getElementById('take-screenshot').addEventListener('click', takeScreenshot);

function startRecording() {
  chrome.desktopCapture.chooseDesktopMedia(['screen', 'window'], (sourceId) => {
    if (sourceId) {
      console.log("Recording started for source ID: ", sourceId);
      //  screen recording logic here
    }
  });
}

function takeScreenshot() {
  chrome.tabs.captureVisibleTab((screenshotUrl) => {
    console.log('Screenshot taken', screenshotUrl);
    sendScreenshotToBackend(screenshotUrl);
  });
}

function sendScreenshotToBackend(imageUrl) {
  fetch('https://your-backend-api.com/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: imageUrl })
  })
  .then(response => response.json())
  .then(data => console.log('Data received from server:', data))
  .catch(error => console.error('Error uploading screenshot:', error));
}
