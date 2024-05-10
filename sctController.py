import DBController
import lecturerController

class sctContoller:

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(sctContoller, self).__new__(self)
        return self.instance
    
    # Get all Equipment
    def get_equip(self):
        elst = []
        for t in ['Laptop','Projector']:
            elst += DBController.getall_equip(t)
        return elst

    # Add new equipment
    def add_equip(self,eid,rtype):
        return DBController.addEquip(eid,rtype)

    # Remove Equipment
    def remove_equip(self,eid):
        return DBController.removeEquip(eid)
    
    # Get all SAT
    def getSAT(self):
        return DBController.getall_sat()
    
    def addSAT(self,sid,fname,lname):
        return DBController.addSAT(sid,fname,lname)
    
    def removeSAT(self,sid):
        return DBController.removeSAT(sid)

    # Allocate new equipment to a request
    def equip_reallocate(self, rid, etype, stime, etime, dow):
        evail = lecturerController.get_Equip(stime, etime, [etype], dow)
        if evail:
            for e in evail:
                DBController.assignEquip(rid, e, stime, etime, dow)
            return True
        else:
            # If the equipment is not available, try to reshuffle
            return self.reshuffleEquip(rid, etype, stime, etime, dow)

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

    def assignToLab(self,dow):
        pass