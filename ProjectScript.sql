CREATE DATABASE projectdb;

USE projectdb;

-- Student Staff Table
CREATE TABLE StudentStaff (
    StudentID INT PRIMARY KEY,
    FirstName varchar(50),
    LastName varchar(50)
);

-- Equipment Table
CREATE TABLE Equipment (
    EquipmentID int PRIMARY KEY,
    EType VARCHAR(15),
);

-- Lecturer Table
CREATE TABLE Lecturer(
    LecturerID int PRIMARY KEY,
    FirstName varchar(50),
    LastName varchar(50),
    Title varchar(3),
    Email varchar(50),
    Telephone varchar(10)
);

-- Student Availability Table
CREATE TABLE SATAvailability(
    StudentID int FOREIGN KEY REFERENCES StudentStaff,
    DayOfWeek varchar(10),
    StartTime time,
    EndTime time
);

-- Support Request Table
CREATE TABLE Request(
    RequestID INT PRIMARY KEY,
    LecturerID int FOREIGN KEY REFERENCES Lecturer,
    ClassLocation VARCHAR(50),
    DayOfWeek varchar(10),
    StartTime time,
    EndTime time
); -- include a start date and end date 

-- Equipment Assignment Table
CREATE TABLE EquipmentAssignment(
	EquipmentID int,
    RID int FOREIGN KEY REFERENCES Request
);

-- SAT Assignment Table
CREATE TABLE SATAssignment(
    StudentID int FOREIGN KEY REFERENCES StudentStaff,
    RID int FOREIGN KEY REFERENCES Request
    sType varchar(2),
    DayOfWeek varchar(10),
    StartTime time,
    EndTime time
);

-- Locations or Rooms supported link each room to a building
CREATE TABLE RoomsSupported(
    RoomName varchar(30) PRIMARY KEY,
    Building varchar(15)
);

-- Distance between buildings
CREATE TABLE Map(
    sBuilding varchar(30),
    eBuilding varchar(30),
    Distance int
);

-- populate rooms supported table and distance between buildinings