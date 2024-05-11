from DBController import DBController

class satController: 

    # Add available time for a SAT
    def submit_time(sid,stime,etime,dow):
        return DBController.addAvailability(sid,stime,etime,dow)
    
    def getTimesSub(sid):          # Maybe switch to ID by adding a login feature
        return DBController.getSubTimes(sid)

    # def remove_availability(self,name,stime,etime,dow):
'''
    def reshuffle_SAT(rid, stime, etime, dow, type):
        available_sats = DBController.getAvails(stime, dow)
        if available_sats:
            DBController.assignSAT(rid, available_sats[0], type, dow, stime)
            print(f"Reshuffle successful: Assigned alternative SAT for Request ID {rid}, Type {type}, on {dow}.")
            return True
        return False

    def reallocateSAT(self, name, rid, stime, etime, dow):
        sid = DBController.getSATn(name)
        if sid == 'Error':
            return "Student Staff entered does not exist."

        sat_start = DBController.getAvails(stime, dow)
        sat_end = DBController.getAvails(etime, dow)

        if sid in sat_start and sid in sat_end:
            DBController.assignSAT(rid, sid, "Setup", dow, stime)
            DBController.assignSAT(rid, sid, "Pickup", dow, etime)
            return "SAT reallocated successfully"
        else:
            if sid not in sat_start:
                if not self.reshuffle_SAT(rid, stime, dow, 'Setup'):
                    return "Could not reshuffle SAT for start time."

            if sid not in sat_end:
                if not self.reshuffle_SAT(rid, etime, dow, 'Pickup'):
                    return "Could not reshuffle SAT for end time."

            return "Reallocated with necessary reshuffles"
                
    
'''