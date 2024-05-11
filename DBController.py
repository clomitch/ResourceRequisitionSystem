import mysql.connector
from Availability import Availability

class DBController:
    lavail = {}
    pavail = {}
    savail = {}

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(DBController, self).__new__(self)
        return self.instance
    
    '''def __init__():
        dows = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        for day in dows:
            print("start")
            DBController.lavail[day] = Availability('Laptop',DBController.getall_equip('Laptop'))
            DBController.pavail[day] = Availability('Projector',DBController.getall_equip('Laptop'))
            DBController.savail[day] = Availability('SAT',DBController.getall_equip('Laptop'))
            print("end")
        self.lavail = {k: Availability('Laptop',DBController.getall_equip('Laptop')) for k in dows}
        self.pavail = {k: Availability('Projector',DBController.getall_equip('Projector')) for k in dows}
        self.savail = {k: Availability('SAT',DBController.getall_satAvail(k)) for k in dows}'''
    
    
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

    # Record student staff availability
    def addAvailability(sid,stime,etime,dow):
        # Add availability to dictionary structure
        stme = [int(x) for x in stime.split(':')]
        etme = [int(x) for x in etime.split(':')]
        if DBController.savail == {}:
            DBController.savail = {k: Availability('SAT',DBController.getall_satAvail(k)) for k in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']}

        for i in range((etme[0])-stme[0]):
            for j in range(4):
                if etme[1]+(j*15) != 60:
                    DBController.savail[dow].addSATavail(sid,(stme[0]+i,stme[1]+(j*15)))
        # Add to the database
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()
            crsr.execute(f'INSERT INTO SATAvailability (StudentID,DayOfWeek,StartTime,EndTime) VALUES ({sid},"{dow}","{stime}","{etime}");')
            
            print("check")
            cnx.commit()
            crsr.close()
            cnx.close()
            return "Availability added Successfully"
        except Exception as e:
            return "Error\nDatabase was not updated"

    '''
    Functions to remove entries in database tables
    '''
    # Remove equipment with ID id from the table Equipment
    def removeEquip(id):
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

    # Remove SAT with ID sid from SATAssignment where request ID is rid
    def removeSATreq(self,sid,rid):
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
        except Exception as e:
            return "Error"

    # Remove Equipment with ID eid from EquipmentAssignment where request ID is rid
    def removeEquipreq(self,eid,rid):
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
                slst[(tme[0],tme[1])] += [StudentID]
            
            crsr.close()
            cnx.close()
            return slst
        except Exception as e:
            print("Error-sat")
            return "Error"

    # Get all requests with the equipment with eid assigned
    def gete_request(self,eid):
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
    def getSATn(self,name):
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
    def gets_request(self,sid):
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

    # Get requests and their location from Requests
    def getl_request(self,stime,dow):
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
        
    # Get graph of UWI Campus
    def getMap(self):
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
    def get_allBuildings(self):
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
    def gets_working(self,stime,rid):
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
    def get_Building(self,rid):
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

    # Get all SAT available on weekday dow at time tme
    def getAvails(self,tme,dow):
        return self.savail[dow].getAvailable(tme)

    # Get all equipment available on weekday dow at time tme
    def getAvaile(self,tme,dow,rtype):
        if rtype == "Laptop":
            return self.lavail[dow].getAvailable(tme)       # Need revision all equipment in the dictionary currently no way to tell equipment apart
        return self.pavail[dow].getAvailable(tme)

    '''
    Functions to assign SAT and Equipment to the request with id rid
    '''
    # Assign SAT with id sid to request with id rid     
    def assignSAT(self,rid,sid,dtype,dow,stime):
        try: 
            cnx = mysql.connector.connect(user='RRSuser', password='f$$RRsystem24',
                                    host='localhost',
                                    auth_plugin='mysql_native_password',
                                    database='projectdb')
            crsr = cnx.cursor()                                                     # NEEDS TO BE REVISED TO FIT MYSQL DATETIME TYPE
            crsr.execute(f'INSERT INTO SATAssignment (StudentID,RID,sType,DayOfWeek,Starttime,EndTime) VALUES ({sid},{rid},"{dtype},"{dow},{stime},{stime+30}");')
            self.savail[dow].markUnavailable(stime,sid)

            cnx.commit()
            crsr.close()
            cnx.close()
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
        except Exception as e:
            return "Error"