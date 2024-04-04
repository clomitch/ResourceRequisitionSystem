class Request:

    #Constructor
    def __init__(self,stime,etime,room):
        #self.rid = rid              # request ID
        self.sup = []               # IDs of staff and equipment being provided
        self.stime = stime          # Start time
        self.etime = etime          # End time
        self.room = room            # Location of event/class
        #self.building = building    # Building the room is on

    def provSup(self,resID):
        self.sup += resID
        # update database to reflect changes

    def getID(self):
        return self.ID

    def get_stime(self):
        return self.stime 
    
    def get_etime(self):
        return self.etime
    
    def get_room(self):
        return self.room
    
    def toString(self):
        return " "