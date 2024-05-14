from DBController import DBController

class lecturerController:
    dis = {}

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(lecturerController, self).__new__(self)
        return self.instance

    def addLecturer(title,name,email,phone):
        DBController.add_lecturer(title,name,email,phone)

    def getLID(email):
        return DBController.getLID(email)
    
    def viewRequests(lid):
        return DBController.getall_requests(lid)

    def getEquip(stime,etime,elst,dow):
        # Get available equipment
        eavail = {}
        for e in elst:
            eavail[e] = ()
            for i in range(stime[0],etime[0]):
                val = DBController.getAvaile((stime[0]+i,0),dow,e)
                a = (val)
                if a != ():
                    if eavail[e] == ():
                        eavail[e] = a
                    else:
                        eavail[e] = tuple(set(a) & set(eavail[e]))
                else:
                    return False
                if eavail[e] == ():
                    return False
        # Get one of each type of equipment to assign to the request
        elst = []
        for eq in eavail.keys():
            elst += eavail[eq][0]
        return elst

    # find the short distance between the buildings
    def findDistance():
        graph = DBController.getMap()
        nodes = DBController.get_allBuildings()

        # Dijktra algorithm to find the shortest path from one building to all others
        for nd in nodes:
            visited = []
            distance = [[nd,0]]
            while visited != nodes:
                distance.sort(key = lambda x:x[1])
                curr = distance[0]
                if curr not in visited:
                    visited += [curr[0]]
                    for edge in graph:
                        if edge[0] == curr[0]:
                            distance += [[edge[0],edge[2]+curr[1]]]
                        elif edge[1] == curr[0]:
                            distance += [[edge[1],edge[2]+curr[1]]]
            lecturerController.dis[nd] = {k:v for [k,v] in distance}

    # Get shortest distance between two buildings
    def getDistance(b1,b2):
        return lecturerController.dis[b1][b2]

    def reshuffleSAT(rid,stime,dow,dtype):
        # Get the building the duty will be on
        bldng = DBController.get_Building(rid)

        # Get where staff is working around this time (rid,building)
        rloc = DBController.getl_request(stime,dow)
        #print(stime,dow)
        if rloc == 'Error':
            return False
        rloc += [(rid,bldng)]

        # Get persons working at this time
        slst = set()        # Using set will prevent duplicates
        for x in rloc:
            slst = slst.union(set(DBController.gets_working(x[0],stime)))
        slst = list(slst)

        # remove assigned classes
        for i in range(len(rloc)):
            DBController.removeSATreq(slst[i],rloc[i][0])

        # count distinct buildings
        b = set()
        for x in rloc:
            b = b.union(set(x[1]))
        b = list(b)

        # if no of buildings is less than the no of requests --> change to SAT
        if len(b) < len(rloc):          
            # get the distance between the buildings
            dlst = []
            for i in range(len(b)-1):
                for j in range(i+1,len(b)):     # getDistance in this class now
                    dlst += [([b[i],b[j]],DBController.getDistance(b[i],b[j]))]

            # sort by distance in ascending order
            dlst.sort(key = lambda x: x[1])

            # the join the closest buildings until its equal
            dlst = dlst[:(len(rloc)-len(b))]

            # Get allottment of requests
            lst,rlst = []
            for x in dlst:
                lst += x[0]
                rlst += [[a[0] for a in rloc if a[1] in x]]         # Each element assigned to one SAT, first the request grouped for one SAT
            rlst += [[y[0]] for y in rloc if (lst.find(y[1]) == -1)]  # Remaining requests
            
            # add new assignments
            for s in slst:
                for req in rlst:    # rlst is a nested list so two loops are needed
                    for r in req:
                        DBController.assignSAT(r,s,dtype,dow,stime)        # Need revision we need to know whether its a setup or pick up may need to add another funtion to DBController

        # the number of building at most is the same number of requests
        else: 
            # Group requests by building
            rlst = []
            for bl in b:
                rlst += [[h[0] for h in rloc if (r[1] in bl)]]                        
            # Add new assignments
            for s in slst:
                for req in rlst:      # rlst is a nested list so two loops are needed
                    for r in req:
                        DBController.assignSAT(r,s,dtype,dow,stime)   

    def getSAT(stime,dow):
        # Get available SATs
        sats = DBController.getAvails(stime,dow)
        #print(sats)
        
        if sats != []:
            return sats[0]
        else:       
            return 0
    
    # Allocate resources to a request
    def allocateR(lid,stime,etime,dow,room,sdate,edate,elst,):
        stme = stime.split(":")
        stme = (int(stme[0]),int(stme[1]))
        etme = etime.split(":")
        etme = (int(etme[0]),int(etme[1]))
        rid = DBController.addRequest(lid,stime,etime,dow,room,sdate,edate)
        print("Got RID",rid)
        lst = lecturerController.getEquip(stme,etme,elst,dow)
        print("Equipment",lst)
        sat = lecturerController.getSAT(stme,dow)
        sat2 = lecturerController.getSAT(etme,dow)
        print("SAT",sat,sat2)
        if sat != 0 and sat2 != 0 and lst != []:
            for e in lst:
                DBController.assignEquip(rid,e,stme,etme,dow)
            DBController.assignSAT(rid,sat,"SU",dow,stme,)
            DBController.assignSAT(rid,sat2,"PU",dow,etme)
            return True
        elif sat == 0:
            if not lecturerController.reshuffleSAT(rid,stme,dow,'SU'):
                return False
        if sat2 == 0:
            if not lecturerController.reshuffleSAT(rid,etme,dow,'PU'):
                return False
        
    # Cancellation of a request
    def cancel_request(stime,dow,room):
        stme = stime.split(":")
        stme = (int(stime[0]),int(stime[1]))
        rid = DBController.get_RID(stme,dow,room)
        return DBController.removeRequest(rid)
