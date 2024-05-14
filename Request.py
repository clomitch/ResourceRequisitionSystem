class Request:
    crid = 0

    #Constructor
    def __init__(self,lid,stime,etime,room,dow,sdate,edate):
        Request.nxtRID()
        self.rid = Request.crid          # request ID
        self.LID = lid                   # lecturer's ID
        self.stime = stime               # Start time
        self.etime = etime               # End time
        self.room = room                 # Location of event/class
        self.dow = dow
        self.sdate = sdate               # Start date
        self.edate = edate               # End date

    @staticmethod
    def nxtRID():
        Request.crid += 1
    
    def getID():
        return Request.ID

    def get_stime(self):
        return self.stime 
    
    def get_etime(self):
        return self.etime
    
    def get_room(self):
        return self.room