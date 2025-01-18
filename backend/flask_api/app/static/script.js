//document.getElementById('start-recording').addEventListener('click', startRecording);
//document.getElementById('stop-recording').addEventListener('click', stopRecording);

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('meeting-form');

        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission

            const title = document.getElementById('meeting-title').value;
            const meetingDate = document.getElementById('meeting-date').value;
            const startTime = document.getElementById('start-time').value;
            const endTime = document.getElementById('end-time').value;

            const platformCheckbox = document.querySelectorAll('input[name="platform"]:checked');
            const platforms = Array.from(platformCheckbox).map(checkbox => checkbox.value);
            const platform = platforms.length > 0 ? platforms[0] : '';

            const participants = []; // for now let's leave it empty, because we don't have fields for them


            // Combine date and time strings into one ISO formatted string
            let scheduledTime = null;
            if (startTime){
                scheduledTime = new Date(meetingDate + 'T' + startTime).toISOString();
                console.log("Scheduled Time:", scheduledTime)
            }


             const meetingData = {
                title: title,
                scheduled_time: scheduledTime,
                platform: platform,
                 participants: participants
            };
             console.log("Meeting Data:", meetingData)
             fetch('/add-meeting', {
                 method: 'POST',
                 headers: {
                     'Content-Type': 'application/json',
                 },
                 body: JSON.stringify(meetingData),
                })
             .then(response => {
                 if (!response.ok) {
                     return response.json().then(error => { throw new Error(error.error) });
                    }
                 return response.json();
                })
             .then(data => {
                 console.log('Meeting added successfully:', data);
                 alert('Meeting added successfully:!\nID: ' + data.meeting_id);
            // Dodaj kod obsługujący sukces (np. przekierowanie)
                })
             .catch(error => {
                console.error('Error adding meeting:', error);
                alert('Error adding meeting: ' + error);
                 // Dodaj kod do obsługi błędu
             });
      });
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
