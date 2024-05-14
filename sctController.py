from DBController import DBController
from lecturerController import lecturerController

class sctController:

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(sctController, self).__new__(self)
        return self.instance

    # Get all Equipment
    def get_equip():
        elst = []
        for t in ['Laptop','Projector','HDMI Cord','Surge Protector']:
            elst += DBController.getall_equip(t)
        return elst

    # Add new equipment
    def add_equip(eid,rtype):
        return DBController.addEquip(eid,rtype)

    # Remove Equipment
    def remove_equip(rtype,eid):
        return DBController.removeEquip(rtype,eid)
    
    # Get all SAT
    def getSAT():
        return DBController.getall_sat()
    
    # Get all SATs
    def addSAT(sid,fname,lname):
        return DBController.addSAT(sid,fname,lname)
    
    # Fire SAT with ID sid
    def removeSAT(sid):
        return DBController.removeSAT(sid)

    # Allocate new equipment to a request
    def equip_reallocate(self, rid, etype, stime, etime, dow):
        stme = stime.split(":")
        stme = tuple([int(s) for s in stme])
        etme = etime.split(":")
        etme = tuple([int(e) for e in etme])

        evail = lecturerController.get_Equip(stme, etme, [etype], dow)
        if evail:
            for e in evail:
                DBController.assignEquip(rid, e, stme, etme, dow)
            return True
        else:
            # If the equipment is not available, try to reshuffle
            return self.reshuffleEquip(rid, etype, stme, etme, dow)

    def reshuffleEquip(self, rid, etype, stime, etime, dow):
        # Try to find any alternative equipment available at the same time
        available_equips = DBController.getAvaile(etype, stime, etime, dow)
        if available_equips:
            # If found, assign the first available equipment
            DBController.assignEquip(rid, available_equips[0], stime, etime, dow)
            print(f"Reshuffle successful: Assigned alternative equipment for Resource ID {rid}, Type {etype}, on {dow}.")
            return True

        # If no alternative equipment is available return False
        return False

    def assignToLab(self, dow, start_hour, end_hour):
        """
        Assign SATs for lab duties each day, in 1-hour increments.

        :param dow: Day of the week
        :param start_hour: Starting hour of the lab assignment
        :param end_hour: Ending hour for lab assignments
        :return: True if the assignments are made, False otherwise
        """
        current_hour = start_hour
        while current_hour < end_hour:
            # Fetch available SATs for this hour
            available_sats = DBController.getAvailableSATs(current_hour, dow)

            # If SATs are available, assign each to a 1-hour increment
            if available_sats:
                for sat in available_sats:
                    DBController.assignSATToLab(sat, current_hour, current_hour + 1, dow)
                current_hour += 1
            else:
                print(f"No available SATs found for hour {current_hour} on {dow}")
                return False

        print(f"SATs assigned for lab duties on {dow} from hour {start_hour} to {end_hour}")
        return True