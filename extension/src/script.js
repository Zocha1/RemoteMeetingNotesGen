console.log("Script.js loaded successfully.");

// Add event listeners for buttons
document.getElementById('start-recording').addEventListener('click', startRecording);
document.getElementById('stop-recording').addEventListener('click', stopRecording);
document.getElementById('take-screenshot').addEventListener('click', takeScreenshot);
document.getElementById('pause-recording').addEventListener('click', pauseTimer);

document.getElementById('plan-recording').addEventListener('click', function () {
  chrome.tabs.create({ url: 'http://localhost:5000/recording' });
});

document.getElementById('manage-notes').addEventListener('click', function () {
  chrome.tabs.create({ url: 'http://localhost:5000/notes' });
});

// Timer Variables
let timerElement = document.getElementById('timer');
let seconds = 0, minutes = 0, hours = 0;
let timerInterval = null;
let isPaused = false;

// Function to update the timer display
function updateTimerDisplay() {
  timerElement.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

// Function to start the timer
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

// Function to pause the timer
function pauseTimer() {
  isPaused = !isPaused; // Toggle pause state
}

// Function to stop the timer
function stopTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
  seconds = 0;
  minutes = 0;
  hours = 0;
  isPaused = false;
  updateTimerDisplay();
}

// Function to start recording
async function startRecording() {
  try {
    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const streamId = await chrome.tabCapture.getMediaStreamId({
        targetTabId: tabs[0].id
      });
      chrome.runtime.sendMessage(
        { type: "START_RECORDING", streamId },
        (response) => {
          if (response?.status) {
            console.log(response.status);
            alert("Nagrywanie rozpoczęte!"); // Show alert when recording starts
            startTimer(); // Start the timer when recording starts
          } else {
            console.error("Failed to start recording.");
          }
        }
      );
    });
  } catch (error) {
    console.error("Error starting recording:", error);
  }
}

// Function to stop recording
function stopRecording() {
  chrome.runtime.sendMessage({ type: "STOP_RECORDING" }, (response) => {
    console.log(response?.status || "No response");
    alert("Nagrywanie zakończone!"); // Show alert when recording stops
    stopTimer(); // Stop the timer when recording stops
  });
}

// Function to take a screenshot
function takeScreenshot() {
  try {
    chrome.tabs.captureVisibleTab((screenshotUrl) => {
      if (screenshotUrl) {
        console.log('Screenshot taken:', screenshotUrl);
        sendScreenshotToBackend(screenshotUrl);
      } else {
        console.error("Failed to capture screenshot.");
      }
    });
  } catch (error) {
    console.error("Error taking screenshot:", error);
  }
}

// Function to send the screenshot to the backend
function sendScreenshotToBackend(imageUrl) {
  fetch('http://localhost:5000/upload-screenshot', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: imageUrl })
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

// Listen for messages from background.js
chrome.runtime.onMessage.addListener((message) => {
  if (message.type === "recording-started") {
    console.log("Recording started.");
    alert("Nagrywanie rozpoczęte!"); // Show alert
    startTimer(); // Start the timer
  } else if (message.type === "recording-stopped") {
    console.log("Recording stopped.");
    alert("Nagrywanie zakończone!"); // Show alert
    stopTimer(); // Stop the timer
  }
});
