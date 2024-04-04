from flask import Flask, request, jsonify
import sctController
import lecturerController
import satController
import Request

app = Flask(__name__)

'''
App routes for the SCT Page
'''
# Get all Equipment
@app.route('/get_equipment', methods=['GET'])
def get_equipment():
    return sctController.get_equip()

# Add new Equipment
@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    data = request.get_json()
    mes = sctController.add_equip(data['EquipmentID'],data['Type'])
    return jsonify({"message": mes})

# Remove Equipment
@app.route('/remove_equipment/<int:id>', methods=['DELETE'])
def delete_equipment(id):
    mes = sctController.remove_equip(id)
    return jsonify({"message": mes})

# Get all SAT
@app.route('/get_student-staff', methods=['GET'])
def get_student_staff():
    return sctController.getSAT()

# Add new SAT
@app.route('/add_student-staff', methods=['POST'])
def add_student_staff():
    data = request.get_json()
    mes = sctController.addSAT(data['StudentID','First Name','Last Name'])
    return jsonify({"message": mes})

# Remove SAT
@app.route('/remove_student-staff/<int:id>', methods=['DELETE'])
def delete_student_staff(id):
    mes = sctController.removeSAT(id)
    return jsonify({"message": mes})

'''
App routes for the Lecturer page
'''
# Submit Support request
app.route('/submit_request', methods=['POST'])
def schedule_tech_item():
    # Extracting form data
    data = {
        "request_type": request.form.get('requestType'),
        "title": request.form.get('title'),
        "full_name": request.form.get('fullName'),
        "email": request.form.get('email'),
        "mobile": request.form.get('mobile'),
        "department": request.form.get('department'),
        "course_or_event": request.form.get('courseOrEvent'),
        "room_assigned": request.form.get('roomAssigned'),
        "day_of_week": request.form.get('dayOfWeek'),
        "start_date": request.form.get('startDate'),
        "end_date": request.form.get('endDate'),
        "start_time": request.form.get('startTime'),
        "end_time": request.form.get('endTime'),
        "equipment_request": request.form.get('equipmentRequest')
    }
    # rid,stime,etime,elst,dow          rid,stime,etime,room,building
    if data['request_type'] == 'New':
        req = Request(data['start_time'],data['end_time'],data['room_assigned'])        # Needs revision the request class needs more details
        mes = lecturerController.allocateR(req.getID(),req.get_stime(),req.get_etime,data['equipment_request'],data['day_of_week'])
        if mes:
            return jsonify({"success": True, "message": "Tech item scheduled successfully!"})
    elif data['request_type'] == 'Cancellation':
        pass        # Write cancellation function in lecturer controller
    else:
        # It is an update to a request
        pass

    return jsonify({"success": True, "message": "Tech item scheduled successfully!"})

'''
App routes for the student staff page
'''
# Submit Available times
@app.route('/submit_availability', methods=['POST'])
def submit_availability():
    # Extract form data
    name = request.form.get('name')
    dates = request.form.getlist('dates[]')
    start_times = request.form.getlist('startTimes[]')
    end_times = request.form.getlist('endTimes[]')
    comments = request.form.get('comments')

    # Process the data (here we are just printing it)
    print("Name:", name)
    print("Dates:", dates)
    print("Start Times:", start_times)
    print("End Times:", end_times)
    print("Comments:", comments)

    # write functions in satController and DBController to add the new available times

    return jsonify({"success": True, "message": "Availability submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
