let mediaRecorder;
let recordedChunks = [];

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "START_RECORDING") {
    startRecording(message.stream);
    sendResponse({ status: "Recording started" });
  } else if (message.type === "STOP_RECORDING") {
    stopRecording(sendResponse);
    return true; // Informuje Chrome, że odpowiedź będzie wysyłana asynchronicznie
  }
});

function startRecording(stream) {
  try {
    // Uzyskaj mikrofon i połącz strumienie
    navigator.mediaDevices.getUserMedia({ audio: true }).then((micStream) => {
      const combinedStream = new MediaStream([
        ...stream.getAudioTracks(),
        ...micStream.getAudioTracks(),
      ]);

      mediaRecorder = new MediaRecorder(combinedStream);
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunks.push(event.data);
        }
      };

      mediaRecorder.start();
      console.log("Recording started with combined stream");
    }).catch(err => {
      console.error("Error obtaining microphone stream:", err);
    });
  } catch (err) {
    console.error("Error starting recording:", err);
  }
}

function stopRecording(sendResponse) {
  if (mediaRecorder) {
    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: "audio/webm" });
      recordedChunks = [];
      saveRecording(blob);
      sendResponse({ status: "Recording stopped" });
    };
    mediaRecorder.stop();
  } else {
    sendResponse({ status: "No recording in progress" });
  }
}

function saveRecording(blob) {
  const formData = new FormData();
  formData.append("audio", blob, "recording.webm");

  fetch("http://localhost:5000/upload-audio", {
    method: "POST",
    body: formData,
  })
  .then(response => response.json())
  .then(data => console.log("Upload successful:", data))
  .catch(error => console.error("Error uploading audio:", error));
}
