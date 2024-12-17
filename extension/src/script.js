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

// Timer Variables
let timerElement = document.getElementById('timer');
let seconds = 0, minutes = 0, hours = 0;
let timerInterval = null;
let isPaused = false;

// Update Timer Display
function updateTimerDisplay() {
  timerElement.textContent = 
    `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Start Timer
function startTimer() {
  if (!timerInterval) {
    timerInterval = setInterval(() => {
      if (!isPaused) {
        seconds++;
        if (seconds === 60) {
          seconds = 0;
          minutes++;
        }
        if (minutes === 60) {
          minutes = 0;
          hours++;
        }
        updateTimerDisplay();
      }
    }, 1000);
  }
}

// Pause Timer
function pauseTimer() {
  isPaused = !isPaused; // Toggle pause state
}

// Stop Timer
function stopTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
  seconds = 0;
  minutes = 0;
  hours = 0;
  isPaused = false;
  updateTimerDisplay();
}

// Event Listeners
document.getElementById('start-recording').addEventListener('click', startTimer);
document.getElementById('pause-recording').addEventListener('click', pauseTimer);
document.getElementById('stop-recording').addEventListener('click', stopTimer);