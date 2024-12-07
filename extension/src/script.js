// Add event listeners for buttons
document.getElementById('start-recording').addEventListener('click', startRecording);
document.getElementById('stop-recording').addEventListener('click', stopRecording);
document.getElementById('take-screenshot').addEventListener('click', takeScreenshot);

document.getElementById('plan-recording').addEventListener('click', function() {
  chrome.tabs.create({ url: 'http://localhost:5000/recording' });
});

document.getElementById('manage-notes').addEventListener('click', function() {
  chrome.tabs.create({ url: 'http://localhost:5000/notes' });
});

// Function to start screen recording
function startRecording() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const activeTab = tabs[0];
    if (activeTab) {
      chrome.tabCapture.capture({ audio: true, video: false }, (stream) => {
        if (stream) {
          chrome.runtime.sendMessage(
            { type: "START_RECORDING", streamId: null, stream },
            (response) => {
              console.log(response.status);
            }
          );
        } else {
          console.error("Failed to capture stream.");
        }
      });
    } else {
      console.error("No active tab found.");
    }
  });
}

function stopRecording() {
  chrome.runtime.sendMessage({ type: "STOP_RECORDING" }, (response) => {
    console.log(response.status);
  });
}

// Function to take a screenshot
function takeScreenshot() {
  chrome.tabs.captureVisibleTab((screenshotUrl) => {
    console.log('Screenshot taken:', screenshotUrl);
    sendScreenshotToBackend(screenshotUrl);
  });
}

// Function to send the screenshot to the backend
function sendScreenshotToBackend(imageUrl) {
  fetch('http://localhost:5000/upload-screenshot', { // Replace with your backend's URL
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: imageUrl }) // Send the base64-encoded screenshot
  })
  .then(response => {
    if (response.ok) return response.json();
    throw new Error('Failed to upload screenshot');
  })
  .then(data => {
    console.log('Response from server:', data);
    alert('Screenshot uploaded successfully!');
  })
  .catch(error => console.error('Error uploading screenshot:', error));
}

