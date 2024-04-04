import DBController

class Availability:
    #Dictionary Implementation

    #import time

    # Time as tuples (hour,minute)
    
    def __init__(self,rtype):
        #tdy = time.gmtime()
        labels = []
        if rtype == 'SAT':
            for i in range(15):
                for j in range(4):
                    labels += [(7+i,15*j)]
            values = DBController.get_satAvail()
        else:
            for i in range(14):
                labels += [(8+i,0)]
            values = DBController.getall_equip()
        self.avail = {labels[i]: values for i in range(len(labels))}
        
    def addResource(self,rsrc):
        for t in self.avail.keys():
            self.avail[t] += [rsrc]
    
    def addSATavail(self,sid,time):
        self.avail[time] += [sid]

    def getAvailable(self,time):
        return self.avail[time]
    
    def markUnavailable(self,time,rsrc):
        self.avail[time] -= [rsrc]
        
    # in the event a device stops working or a SAT leaves remove them altogether
    def remove(self,rsrc):
        for t in self.avail.keys():
            self.avail[t] -= [rsrc]
    
    '''
    Tree implementation
    # Constructor
    def __init__(self,root):
        self.status = []                        # Resources available at time in root
        self.lefttree = Availability(None)      # Seems kinda problematic to me, not sure
        # self.lefttree = None
        self.righttree = Availability(None)
        self.root = root                        # Time represented at node

    def get_status(self):
        return self.status
    
    def get_root(self):
        return self.root
    
    def get_lefttree(self):
        return self.lefttree
    
    def get_righttree(self):
        return self.righttree

    def set_root(self,nroot):
        self.root = nroot

    def set_status(self,nstat):
        self.status = nstat

    # add new node
    def insert(self, value):
        if self.get_root() == None:
            self.set_root(value)
        elif self.get_root() == value:
            print("Error entry already exists")
        elif self.get_root() < value:
            self.get_righttree().insert(value)
        else:
            self.get_lefttree().insert(value)

    # Add new resource to each node
    def addResource(self, rsrc):
        if self.get_root() != None:
            self.set_status(self.get_status() + rsrc)
            self.get_lefttree().addResource(rsrc)
            self.get_righttree().addResource(rsrc)

    # Remove resource from the available resources at specified time
    def remove(self, value, res):
        if self.get_root() == None:
            print("Value does not exist")
        elif self.get_root() == value:
            self.set_status(self.get_status() - res)
        elif self.get_root() < value:
            self.get_righttree().remove(value,res)
        else:
           self.get_lefttree().remove(value,res)

    # check and return resources available for a specific time
    def isAvailable(self,time):
        if self.get_root() == None:
            return []
        elif self.get_root() == time:
            return self.get_status()
        elif self.get_root() < time:
            self.get_righttree().isAvailable(time)
        else:
            self.get_lefttree().isAvailable(time)

    # Specifically for equipment
    def assign(self,request):
        equip = []
        for i in range(request.get_stime(),request.get_etime()):
            avail = self.isAvailable(i)
            if i == request.get_stime() & avail != []:
                equip = avail
            # ensure resource is available for the full period
            elif avail != []:     
                equip = list(set(equip) & set(avail))
            else:
                print("Sufficient resources are not available to support request")
                break
        if equip != []:
            request.provSup(equip[0])
            for j in range(request.get_stime(),request.get_etime()+1):
                self.remove(i,equip[0])     # Indicating unavailability

    # Specifically for stdent staff
    def assign2(self,request):
        # check who is available to work complete the setup for the class/event
        satavail1 = self.isAvailable(request.get_stime() - 15)      # If the location is relatively far from the support area increase 15 to 30
        satavail1 = list(set(satavail1) & set(self.isAvailable(request.get_stime() + 15)))
        if satavail1 == []:
            # if location is factored in then here is where we would check if there is a SAT assigned to a class nearby
            # If there is such a SAT we can add the request to their activities
            print("Sufficient resource are not available to fulfil this request")
        else:
            # Get students available 15 minutes before and after the class end times
            satavail2 = self.isAvailable(request.get_etime() - 15) 
            satavail2 = list(set(satavail2) & set(self.isAvailable(request.get_etime() + 15))) 
            if satavail2 == []:
                # Again, if location is factored in here is where we would check if another SAT is on duty nearby
                print("Insufficient resources available")
            else:
                request.provSup(satavail1[0])
                request.provSup(satavail2[0])
                satavail = [satavail1[0],satavail[0]]
                # Remove student staff fromt list of available student staff for the period assigned
                for i in [request.get_stime(),request.get_etime()]:
                    self.remove(i - 15,satavail[0])
                    self.remove(i + 15,satavail[0])
                    satavail.pop(0)     

    # Not necessary
    def toString(self):
        return " "
    ''' 
