from DBController import DBController

class lecturerController:

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(lecturerController, self).__new__(self)
            self.dis = {}
        return self.instance

    def getEquip(self,stime,etime,elst,dow):
        # Get available equipment
        eavail = {}
        for e in elst:
            eavail[e] = []
            for i in range(stime[0],etime[0]):
                a = DBController.getAvaile(e,stime+i,dow,e)
                if a != []:
                    eavail[e] = list(set(a) & set(eavail))
                else:
                    return False
                if eavail[e] == []:
                    return False
        # Get one of each type of equipment to assign to the request
        elst = []
        for eq in eavail:
            elst += [eq[0]]
        return elst

    # find the short distance between the buildings
    def findDistance(self):
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
            self.dis[nd] = {k:v for [k,v] in distance}

    # Get shortest distance between two buildings
    def getDistance(self,b1,b2):
        return self.dis[b1][b2]

    def reshuffleSAT(self,rid,stime,dow,dtype):
        # Get the building the duty will be on
        bldng = DBController.get_Building(rid)

        # Get where staff is working around this time (rid,building)
        rloc = DBController.get_dbController().getl_request(stime,dow)
        if rloc == False:
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

        # if no of buildings is less than the no of requests
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

    def getSAT(self,stime,dow):
        # Get available SATs
        sats = DBController.getAvails(stime,dow)
        if sats != []:
            return sats[0]
        else:       
            return 0
        
    # Create a similar version to allocate SAT to lab duties
    def allocateR(self,rid,stime,etime,elst,dow):
        lst = self.getEquip(stime,etime,elst)
        sat = self.getSAT(stime,dow)
        sat2 = self.getSAT(etime,dow)
        if sat != 0 and sat2 != 0 and lst != []:
            for e in lst:
                DBController.assignEquip(rid,e,stime,etime,dow)
            DBController.assignSAT(rid,sat,"SU",dow,stime)
            DBController.assignSAT(rid,sat2,"PU",dow,etime)
            return True
        elif sat == 0:
            return self.reshuffleSAT(rid,stime,dow,'SU')
        elif sat2 == 0:
            return self.reshuffleSAT(rid,etime,dow,'PU')
        
    # Cancellation of a request
    def cancel_request(self):
        pass
        
    # Updating a request