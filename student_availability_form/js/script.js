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

    // Additional JavaScript for form submission and validation
    // ...
});
