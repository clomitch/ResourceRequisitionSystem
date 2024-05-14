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
        clid += 1