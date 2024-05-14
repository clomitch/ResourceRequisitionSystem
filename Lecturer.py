class Lecturer:
    clid = 0

    def __init__(self,title,name,email,phone):
        Lecturer.nxtID()
        self.lid = Lecturer.clid
        self.title = title
        self.name = name
        self.email = email
        self.phone = phone


    @staticmethod
    def nxtID():
        Lecturer.clid += 1

    def getID(self):
        return self.lid