document.addEventListener('DOMContentLoaded', function() {
    const dateInputsContainer = document.getElementById('dateInputsContainer');

    // Function to add a new date-time frame input set
    function addDateTimeFrameInput() {
        const inputDiv = document.createElement('div');
        inputDiv.className = 'date-time-frame';
        inputDiv.innerHTML = `
            <label>Date: <input type="date" name="dates[]" required></label>
            <label>From: <input type="time" name="startTimes[]" required></label>
            <label>To: <input type="time" name="endTimes[]" required></label>
        `;
        dateInputsContainer.appendChild(inputDiv);
    }

    // Add the initial set of inputs
    addDateTimeFrameInput();

    // Handle the "Add More Dates" button click
    document.getElementById('addMoreDates').addEventListener('click', function() {
        addDateTimeFrameInput();
    });

    // Handle form submission
    document.getElementById('availabilityForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Prepare data to send to the backend
        const formData = new FormData(this);
        
        // Make a fetch request to submit availability
        fetch('/submit_availability', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle success response
            console.log(data);
            
        })
        .catch(error => {
            // Handle error
            console.error('There was a problem with the fetch operation:', error);
        });
    });

});
