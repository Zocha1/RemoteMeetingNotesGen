// Handle scheduling form submission
document.getElementById('planRecordingForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const email = document.getElementById('email').value;
    const date = document.getElementById('date').value;
  
    console.log('Email:', email);
    console.log('Scheduled date:', date);
  
    // Logic to save the schedule
    fetch('http://localhost:5000/plan-recording', { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, date })
    })
    .then(response => {
      if (response.ok) return response.json();
      throw new Error('Failed to schedule recording');
    })
    .then(data => {
      console.log('Response from server:', data);
      alert('Recording scheduled successfully!');
    })
    .catch(error => console.error('Error scheduling recording:', error));
  });
  