class Resource:
    sid_c = 0
    rid_c = 0

    # constructor
    def __init__(self, rtype):
        self.rtype = rtype
        self.id = self.get_nextID(rtype)

    # maybe get last id from db then return the next id
    @staticmethod
    def get_nextID(self,rtype):
        # Check for student staff type since equipment can be laptop, projector and so on
        if rtype == "SAT":
            self.sid_c += 1
            return self.sid_c
        else:
            self.rid_c += 1
            return self.rid_c
        
    def toString(self):
        return " "
