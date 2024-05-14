//This is the updated  of script.js in sct_page version that implements Fetch API

let equipmentData = [];
let studentStaffData = [];

// Fetch Equipment Data from Flask
function fetchEquipmentData() {
    fetch('/get_equipment')
        .then(response => response.json())
        .then(data => {
            equipmentData = data;
            populateEquipmentTable();
        })
        .catch(error => console.error('Error fetching equipment data:', error));
}

// Fetch Student Staff Data from Flask
function fetchStudentStaffData() {
    fetch('/get_student-staff')
        .then(response => response.json())
        .then(data => {
            studentStaffData = data;
            populateStudentStaffTable();
        })
        .catch(error => console.error('Error fetching student staff data:', error));
}

// Function to populate equipment table
function populateEquipmentTable() {
    const tbody = document.getElementById('equipmentList');
    tbody.innerHTML = ''; // Clear existing table rows

    equipmentData.forEach(item => {
        const row = tbody.insertRow();
        const nameCell = row.insertCell(0);
        const quantityCell = row.insertCell(1);
        const specificationsCell = row.insertCell(2);
        const actionsCell = row.insertCell(3);

        nameCell.textContent = item.name;
        quantityCell.textContent = item.quantity;
        specificationsCell.textContent = item.specifications;

        // Action Buttons 
        const modifyButton = document.createElement('button');
        modifyButton.textContent = 'Modify';
        modifyButton.className = 'modifyButton'; 
        modifyButton.onclick = () => modifyEquipment(item.id);

        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.className = 'removeButton'; 
        removeButton.onclick = () => removeEquipment(item.id);

        actionsCell.append(modifyButton, removeButton);
    });
}

// Function to populate student staff table
function populateStudentStaffTable() {
    const tbody = document.getElementById('studentStaffList');
    tbody.innerHTML = '';

    studentStaffData.forEach(item => {
        const row = tbody.insertRow();
        const nameCell = row.insertCell(0);
        const contactCell = row.insertCell(1);
        const actionsCell = row.insertCell(2);

        nameCell.textContent = item.name;
        contactCell.textContent = item.contact;

        const modifyButton = document.createElement('button');
        modifyButton.className = 'modifyButton';
        modifyButton.textContent = 'Modify';
        modifyButton.addEventListener('click', () => modifyStudentStaff(item.id));

        const removeButton = document.createElement('button');
        removeButton.className = 'removeButton';
        removeButton.textContent = 'Remove';
        removeButton.addEventListener('click', () => removeStudentStaff(item.id));

        actionsCell.appendChild(modifyButton);
        actionsCell.appendChild(removeButton);
    });
}

// Function to add equipment
function addEquipment() {
    const newName = prompt('Enter new equipment name:', '');
    if (!newName) return alert('Equipment name is required.');

    const quantityInput = prompt('Enter quantity:', '0');
    const newQuantity = parseInt(quantityInput, 10);
    if (isNaN(newQuantity) || newQuantity < 0) return alert('Invalid quantity.');

    const newSpecs = prompt('Enter specifications:', '');
    if (!newSpecs) return alert('Specifications are required.');

    const newEquipment = {
        EquipmentID: generateUniqueId('equipment'),
        Type: newSpecs
    };

    fetch('/add_equipment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newEquipment)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchEquipmentData();
    })
    .catch(error => console.error('Error adding equipment:', error));
}


// Function to add student staff
function addStudentStaff() {
    const newName = prompt('Enter new student staff Name:', '');
    if (!newName) return alert('Student staff name is required.');

    const newContact = prompt('Enter contact information:', '');
    if (!newContact) return alert('Contact information is required.');

    const newStudentStaff = {
        StudentID: generateUniqueId('studentStaff'),
        'First Name': newName.split(' ')[0],
        'Last Name': newName.split(' ')[1],
    };

    fetch('/add_student-staff', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newStudentStaff)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchStudentStaffData();
    })
    .catch(error => console.error('Error adding student staff:', error));
}


// Get reference to the "Add Equipment" and "Add Student Staff" button // Attach event listener to the button
const equipmentButton = document.getElementById('equipmentButton');
equipmentButton.addEventListener('click', addEquipment);

const studentStaffButton = document.getElementById('studentStaffButton');
studentStaffButton.addEventListener('click', addStudentStaff);

// Function to modify equipment details 
function modifyEquipment(itemId) {
    const equipment = equipmentData.find(item => item.id === itemId);

    if (equipment) {
        openModal('Enter new equipment name:', equipment.name, function(newName) {
            const newQuantity = parseInt(prompt('Enter new quantity:', equipment.quantity)) || equipment.quantity;
            const newSpecs = prompt('Enter new specifications:', equipment.specifications);

            if (newName && newQuantity >= 0 && newSpecs) {
                equipment.name = newName;
                equipment.quantity = newQuantity;
                equipment.specifications = newSpecs;
                populateEquipmentTable();
            }
        });
    }
}

// Function to modify student staff details 
function modifyStudentStaff(itemId) {
    const staff = studentStaffData.find(item => item.id === itemId);

    if (staff) {
        openModal('Enter new student staff name:', staff.name, function(newName) {
            const newContact = prompt('Enter new contact information:', staff.contact);

            if (newName && newContact) {
                staff.name = newName;
                staff.contact = newContact;
                populateStudentStaffTable();
            }
        });
    }
}

// Function to remove equipment
function removeEquipment(itemId) {
    const confirmed = confirm('This action will remove the equipment. Press "OK" to proceed or "Cancel" to cancel.');

    if (confirmed) {
        fetch(`/remove_equipment/${itemId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchEquipmentData();
        })
        .catch(error => console.error('Error removing equipment:', error));
    } else {
        alert('Removal canceled. The equipment was not removed.');
    }
}

// Function to remove student staff
function removeStudentStaff(itemId) {
    const confirmed = confirm('This action will remove the student staff. Press "OK" to proceed or "Cancel" to cancel.');

    if (confirmed) {
        fetch(`/remove_student-staff/${itemId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchStudentStaffData();
        })
        .catch(error => console.error('Error removing student staff:', error));
    } else {
        alert('Removal canceled. The student staff was not removed.');
    }
}


function generateUniqueId(type) {
    const prefix = (type === 'equipment') ? 'E' : 'S';
    return prefix + Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

function openModal(title, defaultValue, callback) {
    const userInput = prompt(title, defaultValue);
    if (userInput !== null) {
        callback(userInput);
    }
}
// Call functions to populate tables
populateEquipmentTable();
populateStudentStaffTable();
