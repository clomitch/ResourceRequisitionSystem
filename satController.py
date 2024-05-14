from DBController import DBController

class satController: 

    # Add available time for a SAT
    def submit_time(sid,stime,etime,dow):
        stme = stime.split(":")
        stme = [int(s) for s in stme]
        etme = etime.split(":")
        etme = [int(e) for e in etme]
        return DBController.addAvailability(sid,stme,etme,dow)
    
    def getTimesSub(sid):          # Maybe switch to ID by adding a login feature
        return DBController.getSubTimes(sid)

    def remove_availability(sid,stime,dow):
        stme = stime.split(":")
        stme = [int(s) for s in stme]
        return DBController.removeAvailability(sid,stime,dow)
