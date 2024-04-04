import DBController

class satController: 

    # Add available time for a SAT
    def submit_time(self,name,stime,etime,dow):
        sid = DBController.getSATn(name)
        if sid == 'Error':
            return "Student Staff entered does not exists"
        DBController.addAvailability(sid,stime,etime,dow)
        pass
    
    # def view_availbility(self,name):          # Maybe switch to ID by adding a login feature

    # def remove_availability(self,name,stime,etime,dow):
