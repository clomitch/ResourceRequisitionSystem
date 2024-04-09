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
    def equip_reallocate(self,rid,etype,stime,etime,dow):
        # use the usual allocate function to allocate the equipment 
        evail = lecturerController.get_Equip(stime,etime,[etype],dow)
        if evail != False:
            DBController.assignEquip(rid,evail[0],stime,etime,dow)
            return True
        else:
            return False
            #notify the SCT 

    def assignToLab(self,dow):
        pass