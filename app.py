from flask import Flask, request, jsonify
from sctController import sctController
from lecturerController import lecturerController
from satController import satController

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
@app.route('/remove_equipment/<string:rtype>/<int:id>', methods=['DELETE'])
def delete_equipment(rtype,id):
    mes = sctController.remove_equip(rtype,id)
    return jsonify({"message": mes})

# Get all SAT
@app.route('/get_student-staff', methods=['GET'])
def get_student_staff():
    return sctController.getSAT()

# Add new SAT
@app.route('/add_student-staff', methods=['POST'])
def add_student_staff():
    data = request.get_json()
    mes = sctController.addSAT(data['StudentID'],data['First Name'],data['Last Name'])
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
@app.route('/submit_request', methods=['POST'])
def schedule_tech_item():
    data = request.get_json()
    #print('got the data')
    # lid,stime,etime,room,sdate,edate          stime,etime,elst,dow)
    if data['Request Type'] == 'New':
        lid = lecturerController.getLID(data['Email'])      # Needs revision the request class needs more details
        if lid == 0:
            lecturerController.addLecturer(data['Title'],data['Full Name'],data['Email'],data['Mobile'])
        lecturerController.allocateR(lid,data['Start Time'],data['End Time'],data['Day Of Week'],data["Room Assigned"],data["Start Date"],data['End Date'],data['Equipment Needed'])    
    else:
        lecturerController.cancel_request(data['Day Of Week'],data['Start Time'],data['Room Assigned'])
        if data['request_type'] == 'Update':
            lecturerController.allocateR(lid,data['Start Time'],data['End time'],data['Day Of Week'],data["Room Assigned"],data["Start Date"],data['End Date'],data['Equipment Needed'])

    return jsonify({"success": True, "message": "Request submitted/nCheck email for denial/approval of your request"})

# View requests made by a Lecturer
@app.route('/view_requests/<int:lid>')
def viewRequests(lid):
    return lecturerController.viewRequests(lid)

'''
App routes for the student staff page
'''
# Submit Available times
@app.route('/submit_availability', methods=['POST'])
def submit_availability():
    data = request.get_json()
    
    mes = satController.submit_time(data['StudentID'],data['StartTime'],data['EndTime'],data['DayOfWeek'])
    return jsonify({"message": mes})

# View Available Times Submitted
@app.route('/getAvailableTimes/<int:sid>',methods=['GET'])
def get_times(sid):
    return satController.getTimesSub(sid)

# Delete Available Times submitted
@app.route('/remove_availability/<int:sid>/<string:dow>/<string:stime>', methods=['DELETE'])
def removeTime(sid,dow,stime):
    return satController.remove_availability(sid,stime,dow)

if __name__ == '__main__':
    app.run(debug=True)
