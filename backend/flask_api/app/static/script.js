// document.getElementById('start-recording').addEventListener('click', startRecording);
// document.getElementById('stop-recording').addEventListener('click', stopRecording);

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('meeting-form');

    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault(); // Zapobiega domyślnemu przesyłaniu formularza

            const meetingData = {
                title: document.getElementById('meeting-title').value,
                scheduled_time: `${document.getElementById('meeting-date').value}T${document.getElementById('start-time').value}:00`,
                platform: document.getElementById('selected-platform').value, // Pobierz wybraną platformę
                participants: [] // Możesz dodać obsługę uczestników, jeśli jest wymagana
            };

            try {
                const response = await fetch('/add-meeting', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(meetingData)
                });

                if (response.ok) {
                    const data = await response.json();
                    alert('Meeting saved successfully!');
                    console.log(data);
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.error}`);
                }
            } catch (err) {
                console.error('Error saving meeting:', err);
                alert('An error occurred while saving the meeting.');
            }
        });
    } else {
        console.error('Form element not found!');
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

document.querySelectorAll('.platform-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Usuń klasę "selected" z wszystkich przycisków
        document.querySelectorAll('.platform-btn').forEach(btn => btn.classList.remove('selected'));
        // Dodaj klasę "selected" do klikniętego przycisku
        button.classList.add('selected');
        // Ustaw wartość wybranej platformy w ukrytym polu
        document.getElementById('selected-platform').value = button.getAttribute('data-platform');
    });
});
