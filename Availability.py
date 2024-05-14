class Availability:
    avail = {}
    
    def __init__(self,rtype,rlst):
        labels = []
        if rtype == 'SAT':
            for i in range(15):
                for j in range(4):
                    labels += [(7+i,15*j)]
            if rlst == []:
                self.avail = {labels[i]:[] for i in range(len(labels))}
            else:
                self.avail = {labels[i]: [rlst[labels[i]]] for i in range(len(labels))}
            print(self.avail)
        else:
            self.avail = {(i,0): rlst for i in range(8,22)}
        #print(self.avail)
        
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
            self.avail[t] = list(set(self.avail[t]) - set([rsrc]))
    