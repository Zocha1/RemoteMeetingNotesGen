chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  try {
    if (message.type === "START_RECORDING") {
      console.log("START_RECORDING message received:", message);

      const streamId = message.streamId;

      // Sprawdź, czy dokument offscreen już istnieje
      const offscreenContexts = await chrome.runtime.getContexts({});
      const existingOffscreen = offscreenContexts.find(
        (context) => context.contextType === "OFFSCREEN_DOCUMENT"
      );

      if (!existingOffscreen) {
        // Stwórz dokument offscreen
        console.log("Creating offscreen document...");
        await chrome.offscreen.createDocument({
          url: "src/offscreen.html",
          reasons: ["USER_MEDIA"],
          justification: "Required for screen recording using tabCapture",
        });
      }

      // Wyślij wiadomość do dokumentu offscreen, aby rozpocząć nagrywanie
      chrome.runtime.sendMessage({
        target: "offscreen",
        type: "start-recording",
        data: streamId,
      });

      // Wyślij wiadomość do popupu, że nagrywanie się rozpoczęło
      chrome.runtime.sendMessage({
        type: "recording-started",
      });

      sendResponse({ status: "Recording started in offscreen document" });
    } else if (message.type === "STOP_RECORDING") {
      console.log("STOP_RECORDING message received.");

      // Wyślij wiadomość do dokumentu offscreen, aby zatrzymać nagrywanie
      chrome.runtime.sendMessage({
        target: "offscreen",
        type: "stop-recording",
      });

      // Wyślij wiadomość do popupu, że nagrywanie zostało zakończone
      chrome.runtime.sendMessage({
        type: "recording-stopped",
      });

      sendResponse({ status: "Recording stopped in offscreen document" });
    } else {
      console.error("Unrecognized message type:", message.type);
      sendResponse({ status: "Error", error: "Unknown message type" });
    }
  } catch (error) {
    console.error("Error in background.js:", error);
    sendResponse({ status: "Error", error: error.message });
  }
});

// Obsługa wiadomości zwrotnej z dokumentu offscreen
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'recording-finished') {
    console.log('Received recording-finished message:', message.blobUrl);

    // Pobierz Blob na podstawie Blob URL
    fetch(message.blobUrl)
      .then((response) => response.blob()) // Konwertuj odpowiedź na Blob
      .then((blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'recording.webm');

        // Wyślij plik na backend
        fetch('http://localhost:5000/upload-audio', {
          method: 'POST',
          body: formData,
        })
          .then((response) => {
            if (response.ok) {
              console.log('Recording successfully uploaded to backend.');
            } else {
              console.error('Failed to upload recording. Status:', response.status);
            }
          })
          .catch((error) => {
            console.error('Error uploading recording to backend:', error);
          });
      })
      .catch((error) => {
        console.error('Error fetching blob from Blob URL:', error);
      });
  }
});
