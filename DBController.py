import mysql.connector
from Availability import Availability
from Request import Request
from Lecturer import Lecturer

class DBController:
    lavail = {}
    pavail = {}
    savail = {}

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(DBController, self).__new__(self)
        return self.instance
   
    
    ''' 
    Functions to Add entries to database tables
    '''
    # Add new SAT to table Student Staff
    def addSAT(sid,fname,lname):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'INSERT INTO StudentStaff (StudentID, FirstName, LastName) VALUES ({sid},"{fname}","{lname}");')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "SAT successfully added"
        except Exception as e:
            return "Error"

    # Add new equipment to table Equipment
    def addEquip(eid,rtype):
        dows = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        
        # Add new equipment to availability structure
        if DBController.lavail == {}:       
            DBController.setAvailability()
        if rtype == 'Laptop':
            for dow in dows:
                DBController.lavail[dow].addResource(eid)
        else:
            for dow in dows:
                DBController.pavail[dow].addResource(eid)

        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'INSERT INTO Equipment (EquipmentID, EType) VALUES ({eid}, "{rtype}");')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Equipment added Successfully"
        except Exception as e:
            return "Error\nEquipment not added"
 
    # Add new Lecturer data
    def add_lecturer(title,name,email,phone):
        lid = Lecturer(title,name,email,phone)
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'INSERT INTO Lecturer (LecturerID,flname,Title,Email,Telephone) VALUES ({lid}, "{name}", "{title}", "{email}","{phone}");')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Lecturer added Successfully"
        except Exception as e:
            return "Error\nLecturer not added"

    # Record student staff availability
    def addAvailability(sid,stime,etime,dow):
        # Add availability to dictionary structure
        stme = [int(x) for x in stime.split(':')]
        etme = [int(x) for x in etime.split(':')]
        if DBController.savail == {}:
            DBController.setAvailability()
        for i in range((etme[0])-stme[0]):
            for j in range(4):
                DBController.savail[dow].addSATavail(sid,(stme[0]+i,stme[1]+(j*15)))
        
        # Add to the database
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'INSERT INTO SATAvailability (StudentID,DayOfWeek,StartTime,EndTime) VALUES ({sid},"{dow}","{stime}","{etime}");')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Availability added Successfully"
        except Exception as e:
            return "Error\nDatabase was not updated"

    def addRequest(lid,stime,etime,dow,room,sdate,edate):
        req = Request(lid,stime,etime,dow,room,sdate,edate)
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'INSERT INTO Request (RequestID,LecturerID,ClassLocation,DayOfWeek,StartTime,EndTime) VALUES ({req.getID()},{lid},"{room}","{dow}","{stime}","{etime}");')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return req.getID()
        except Exception as e:
            return "Error\nDatabase was not updated"


    '''
    Functions to remove entries in database tables
    '''
    # Remove equipment with ID id from the table Equipment
    def removeEquip(rtype,id):
        # Remove from availability structure
        print(DBController.lavail)
        if rtype == "Laptop":
            for dow in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']:
                DBController.lavail[dow].remove(id)
        else:
            for dow in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']:
                DBController.pavail[dow].remove(id)

        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'DELETE from Equipment WHERE EquipmentID = {id};')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Equipment record successfully removed"
        except Exception as e:
            return "Error \nEquipment not removed"

    # Remove SAT with ID id from the table 
    def removeSAT(id):
        # Remove from Availability structure
        for dow in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']:
            DBController.savail[dow].remove(id)

        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'DELETE from StudentStaff WHERE StudentID = {id};')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "SAT successfully removed"
        except Exception as e:
            return "Error \nSAT not removed"

    def removeAvailability(sid,stime,dow):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'DELETE from SATAvailability WHERE StudentID = {sid} and StartTime = "{stime}" and DayOfWeek = "{dow}";')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Availability successfully updated"
        except Exception as e:
            return "Error \nAvailability not updated"

    def removeRequest(rid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'DELETE from Request WHERE RequestID = {rid};')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Request successfully cancelled"
        except Exception as e:
            return "Error \nRequest not cancelled"

    # Remove SAT with ID sid from SATAssignment where request ID is rid
    def removeSATreq(sid,rid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'DELETE from SATAssignment WHERE StudentID = {sid} AND RID = {rid};')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Error \nSAT still assigned to request"
        except Exception as e:
            return "Error"

    # Remove Equipment with ID eid from EquipmentAssignment where request ID is rid
    def removeEquipreq(eid,rid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'DELETE from EquipmentAssignment WHERE EquipmentID = {eid} AND RID = {rid};')
            
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Equipment removed from Request"
        except Exception as e:
            return "Error"

    '''
    Functions to get data from database tables
    '''
    # Get all equipment of the type specified by rtype, eg: laptop, projector, mouse
    def getall_equip(rtype):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24', 
                                          host='localhost', 
                                          auth_plugin='mysql_native_password', 
                                          database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM Equipment WHERE EType = "{rtype}";')
            equip = crsr.fetchall()
            elst = []
            for equipment in equip:
                elst += [equipment]
            
            crsr.close()
            cnx.close()
            return elst
        except Exception as e:
            print(e)
            return "Error"

    # Get all SAT from the table Student Staff
    def getall_sat():
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM StudentStaff;')
            s = crsr.fetchall()
            slst = []
            for StudentID, FirstName, LastName in s:
                slst += [(StudentID,FirstName,LastName)]
            
            crsr.close()
            cnx.close()
            return slst
        except Exception as e:
            print("Error-eq")
            return "Error"

    # get all requests for a day of the week
    def getall_requests(dow):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM Request WHERE DayOfWeek = {dow};')
            s = crsr.fetchall()
            slst = []
            for rid,olid,room,dow,stime,etime in s:
                slst += [(rid,olid,room,dow,stime,etime)]
            
            crsr.close()
            cnx.close()
            return slst
        except Exception as e:
            print("Error-eq")
            return "Error"

    # Get all SAT available to work on a weekday 
    def getall_satAvail(dow):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT StudentID, StartTime FROM SATAvailability WHERE DayOfWeek = "{dow}" ORDER BY StartTime;')
            s = crsr.fetchall()
            slst = {(k,j*15):[] for k in range(7,22) for j in range(4)}
            for StudentID, StartTime in s:
                tme = StartTime.split(":")
                tme = [int(t) for t in tme]
                slst[(tme[0],tme[1])] += [StudentID]
            
            crsr.close()
            cnx.close()
            return slst
        except Exception as e:
            print("Error-sat")
            return "Error"

    # Get all requests with the equipment with eid assigned
    def gete_request(eid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT RID FROM EquipmentAssigment WHERE EquipmentID = {eid};')        # Needs revision
            r = crsr.fetchall()
            rlst = []
            for RID in r:
                rlst += [RID]
            
            crsr.close()
            cnx.close()
            return rlst
        except Exception as e:
            return "Error"

    # Get the StudentID of the Student with name, name
    def getSATn(name):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT StudentID FROM StudentStaff WHERE FirstName = {name[0]} AND LastName = {name[1]};')
            sat = crsr.fetchone()[0]
            
            crsr.close()
            cnx.close()
            return sat
        except Exception as e:
            return "Error"

    # Get all requests with the SAT with sid assigned
    def gets_request(sid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM SATAssignment WHERE StudentID = {sid};')
            sata = crsr.fetchall()
            salst = []
            for StudentID, RID, sType, dow in sata:
                salst += [(StudentID,RID,sType,dow)]
            
            crsr.close()
            cnx.close()
            return salst
        except Exception as e:
            return "Error"

    # Find request ID given start and end time, weekday, room start and end date or create the new request
    def get_RID(stime,dow,room):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT RequestID FROM Requests WHERE StartTime = "{stime}" and DayOfWeek = "{dow}" and ClassLocation = "{room}";')
            rid = crsr.fetchone()[0]

            crsr.close()
            cnx.close()
            return rid
        except Exception as e:
            return "Error"
        
    def getLID(email):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT LecturerID FROM Lecturer WHERE Email = "{email}";')
            lid = crsr.fetchone()

            crsr.close()
            cnx.close()
            return lid
        except Exception as e:
            return "Error"

    # Get requests and their location from Requests
    def getl_request(stime,dow):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT RequestID,ClassLocation FROM Request WHERE Starttime = {stime} AND DayOfWeek "{dow}";')         # Needs revision to match MySQL data type
            rloc = crsr.fetchall()
            rllst =[]
            for RequestID, ClassLocation in rloc:
                crsr.execute(f'SELECT Building FROM RoomsSupported WHERE RoomName = "{ClassLocation}";')
                Building = crsr.fetchone()[0]
                rllst += [(RequestID,Building)]
            
            crsr.close()
            cnx.close()
            return rllst
        except Exception as e:
            return "Error"

    def getLecRequests(lid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM Request WHERE LecturerID = {lid};')
            lrs = crsr.fetchall()
            lrslst = []
            for rid,olid,room,dow,stime,etime in lrs:
                lrslst += [(rid,olid,room,dow,stime,etime)]
            
            crsr.close()
            cnx.close()
            return lrslst
        except Exception as e:
            return "Error"


    # Get graph of UWI Campus
    def getMap():
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM Map;')
            dis = crsr.fetchall()
            
            crsr.close()
            cnx.close()
            return dis
        except Exception as e:
            return "Error"

    # Get all the buildings with supported rooms
    def get_allBuildings():
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT Distinct Building FROM RoomsSupported;')
            dis = crsr.fetchall()
            
            crsr.close()
            cnx.close()
            return dis
        except Exception as e:
            return "Error"

    # Get SATs working at a time stime on the day of the week dow
    def gets_working(stime,rid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT StudentID FROM SATAssignment WHERE RID = {rid} AND StartTime = {stime};')       # Needs revision to match Mysql datetime
            sid = crsr.fetchone()[0]

            crsr.close()
            cnx.close()
            return sid
        except Exception as e:
            return "Error"
        
    # Get building of a request
    def get_Building(rid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT Building FROM Requests WHERE RID = {rid};')
            bl = crsr.fetchone()[0]

            crsr.close()
            cnx.close()
            return bl
        except Exception as e:
            return "Error"

    def getSubTimes(sid):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM SATAvailability WHERE StudentID = {sid};')
            bl = crsr.fetchall()
            tlst = []
            for StudentID, DayOfWeek, StartTime, EndTime in bl:
                tme = {}
                tme['StudentID'] = StudentID
                tme['DayOfWeek'] = DayOfWeek
                tme['StartTime'] = str(StartTime)
                tme['Endtime']  = str(EndTime)
                tlst += [tme]

            crsr.close()
            cnx.close()
            return tlst
        except Exception as e:
            return "Error"

    '''
    Functions to retrive resource availabilty
    '''

    '''
    # Get the available times of all SAT on day grouped by 15min interval       IS THIS REALLY NECESSARY????????? PROBABLY WILL BE OMITTED
    def get_satAvail(self,day):
        try: 
            cnx = mysql.connector.connect(user='project_user', password='password',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'SELECT * FROM SATAvailability WHERE DayOfWeek = {day};')       # Needs revision
            
            crsr.close()
            cnx.close()
        except Exception as e:
            return "Error" '''

    # Initialise or restore availability data structure
    def setAvailability():
        dows = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        DBController.lavail = {k: Availability('Laptop',DBController.getall_equip('Laptop')) for k in dows}
        DBController.pavail = {k: Availability('Projector',DBController.getall_equip('Projector')) for k in dows}
        DBController.savail = {k: Availability('SAT',[]) for k in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']}

    # Get all SAT available on weekday dow at time tme
    def getAvails(tme,dow):
        if DBController.savail == {} and DBController.getall_requests(dow) != []:
            DBController.setAvailability()
        return DBController.savail[dow].getAvailable(tme)

    # Get all equipment available on weekday dow at time tme
    def getAvaile(tme,dow,rtype):
        # print("lavail: ",DBController.lavail)
        if DBController.lavail == {} and DBController.getall_requests(dow) != []:
            DBController.setAvailability()
        if rtype == "Laptop":
            return DBController.lavail[dow].getAvailable(tme)       # Need revision all equipment in the dictionary currently no way to tell equipment apart
        return DBController.pavail[dow].getAvailable(tme)

    '''
    Functions to assign SAT and Equipment to the request with id rid
    '''
    # Assign SAT with id sid to request with id rid     
    def assignSAT(rid,sid,dtype,dow,stime):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()                                                     # NEEDS TO BE REVISED TO FIT MYSQL DATETIME TYPE
            crsr.execute(f'INSERT INTO SATAssignment (StudentID,RID,sType,DayOfWeek,Starttime,EndTime) VALUES ({sid},{rid},"{dtype},"{dow},{stime},{stime+30}");')
            DBController.savail[dow].markUnavailable(stime,sid)

            cnx.commit()
            crsr.close()
            cnx.close()
            return "SAT assigned successfully"
        except Exception as e:
            return "Error"

    # Assign Equipment with id eid to request with id rid  
    def assignEquip(self,rid,eid,stime,etime,dow,rtype):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'INSERT INTO EquipmentAssignment (EquipmentID,RID) VALUES ({rid},{eid});')
            
            if rtype == 'Laptop':
                for i in range(stime,etime):
                    self.lavail[dow].markUnavailable(i,eid)
            else:
                for i in range(stime,etime):
                    self.pavail[dow].markUnavailable(i,eid)

            cnx.commit()
            crsr.close()
            cnx.close()
            return "Equipment Assigned"
        except Exception as e:
            return "Error"