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

// Obsługuje formularz planowania nagrywania
document.getElementById('planRecordingForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const date = document.getElementById('date').value;

  console.log('Email addresses:', email);
  console.log('Recording planned for:', date);

  // Tutaj dodaj logikę zapisywania planu w bazie danych lub wysyłania na backend
  // Możesz wysłać te dane do backendu:
  // fetch('https://your-backend-api.com/plan-recording', { method: 'POST', body: JSON.stringify({ email, date }) });

  alert('Recording planned successfully!');
});
