document.getElementById('start-recording').addEventListener('click', startRecording);
document.getElementById('stop-recording').addEventListener('click', stopRecording);

document.addEventListener('DOMContentLoaded', function () {
    const startRecordingButton = document.getElementById('start-recording');
    const stopRecordingButton = document.getElementById('stop-recording');

    if (startRecordingButton) {
        startRecordingButton.addEventListener('click', startRecording);
    }

    if (stopRecordingButton) {
        stopRecordingButton.addEventListener('click', stopRecording);
    }
});

async function authorizeGoogle() {
    window.open('/authorize-google', '_blank');
}

async function syncMeeting() {
    const meetingDate = document.getElementById('meeting-date').value;
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;

    // Ensure times are filled and formatted correctly
    if (!meetingDate || !startTime || !endTime) {
        alert("Please ensure all date and time fields are filled.");
        return;
    }

    const meetingData = {
        title: document.getElementById('meeting-title').value,
        start_time: `${meetingDate}T${startTime}:00Z`,
        end_time: `${meetingDate}T${endTime}:00Z`,
        attendees: [] // Add email addresses of attendees here, if needed
    };

    try {
        const response = await fetch('/sync-google-calendar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(meetingData),
        });

        const data = await response.json();
        if (response.ok) {
            alert('Meeting synchronized with Google Calendar!');
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (err) {
        console.error("Error syncing meeting:", err);
    }
}


async function authorizeZoom() {
    window.open('/zoom/authorize', '_blank');
}

async function syncZoomMeeting() {
    const meetingData = {
        title: document.getElementById('meeting-title').value,
        start_time: document.getElementById('meeting-date').value + 'T' + document.getElementById('start-time').value + ':00Z',
        end_time: document.getElementById('meeting-date').value + 'T' + document.getElementById('end-time').value + ':00Z',
    };
    const response = await fetch('/zoom/sync-meeting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(meetingData)
    });
    const data = await response.json();
    if (response.ok) {
        alert('Meeting synchronized with Zoom successfully!');
        console.log(data);
    } else {
        alert(`Error: ${data.error}`);
    }
}
