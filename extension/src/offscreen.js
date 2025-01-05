let mediaRecorder;
let recordedChunks = [];

chrome.runtime.onMessage.addListener(async (message) => {
  if (message.target === "offscreen") {
    if (message.type === "start-recording") {
      startRecording(message.data);
    } else if (message.type === "stop-recording") {
      stopRecording();
    }
  }
});

async function startRecording(streamId) {
  try {
    console.log("Starting recording with streamId:", streamId);

    const media = await navigator.mediaDevices.getUserMedia({
      audio: {
        mandatory: {
          chromeMediaSource: "tab",
          chromeMediaSourceId: streamId,
        },
      },
      video: {
        mandatory: {
          chromeMediaSource: "tab",
          chromeMediaSourceId: streamId,
        },
      },
    });

    mediaRecorder = new MediaRecorder(media, { mimeType: "video/webm" });

    mediaRecorder.ondataavailable = (event) => recordedChunks.push(event.data);

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: "video/webm" });
      const blobUrl = URL.createObjectURL(blob);

      // Wyślij URL nagrania z powrotem do background.js
      chrome.runtime.sendMessage({
        type: "recording-finished",
        blobUrl,
      });

      recordedChunks = [];
    };

    mediaRecorder.start();
    console.log("MediaRecorder started in offscreen document.");
  } catch (error) {
    console.error("Error in offscreen recording:", error);
  }
}

function stopRecording() {
  if (mediaRecorder) {
    mediaRecorder.stop();
    console.log("MediaRecorder stopped in offscreen document.");
  } else {
    console.warn("No active MediaRecorder to stop.");
  }
}
