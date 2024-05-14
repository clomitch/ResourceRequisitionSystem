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
    EType VARCHAR(15)
);

-- Lecturer Table
CREATE TABLE Lecturer(
    LecturerID int PRIMARY KEY,
    FullName varchar(100),
    Title varchar(3),
    Email varchar(50),
    Telephone varchar(10)
);

-- Student Availability Table
CREATE TABLE SATAvailability(
    StudentID int,
    DayOfWeek varchar(10),
    StartTime time,
    EndTime time,
    FOREIGN KEY (StudentID) REFERENCES StudentStaff(StudentID)
);

-- Support Request Table
CREATE TABLE Request(
    RequestID INT PRIMARY KEY,
    LecturerID int,
    ClassLocation VARCHAR(50),
    DayOfWeek varchar(10),
    StartTime time,
    EndTime time,
    FOREIGN KEY (LecturerID) REFERENCES Lecturer(LecturerID)
); -- include a start date and end date 

-- Equipment Assignment Table
CREATE TABLE EquipmentAssignment(
	EquipmentID int,
    RID int, 
    FOREIGN KEY (RID) REFERENCES Request(RequestID)
);

-- SAT Assignment Table
CREATE TABLE SATAssignment(
    StudentID int,
    RID int,
    sType varchar(2),
    DayOfWeek varchar(10),
    StartTime time,
    EndTime time,
    FOREIGN KEY (StudentID) REFERENCES StudentStaff(StudentID),
    FOREIGN KEY (RID) REFERENCES Request(RequestID)
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

-- Populating rooms supported table
INSERT INTO RoomsSupported (RoomName, Building) VALUES
    ('Office of the Dean Room 54', 'MSBM-S'),
    ('FSS_Seminar Room D-101', 'MSBM-N'),
    ('FSS_Graduate Lounge D-102', 'MSBM-N'),
    ('FSS_Seminar Room F-202', 'MSBM-N'),
    ('FSS_Seminar Room F-204', 'MSBM-N'),
    ('FSS_Conference Room F-203', 'MSBM-N'),
    ('FSS_Seminar Room G-101', 'MSBM-N'),
    ('FSS_Seminar Room G-102', 'MSBM-N'),
    ('FSS_PSYC Lab G-202', 'MSBM-N'),
    ('FSS_PSYC Lab G-204', 'MSBM-N'),
    ('FSS_GradLab A', 'FSS-1'),
    ('FSS_GradLabB', 'FSS-1'),
    ('FSS_Seminar Room I-101', 'MSBM-N'),
    ('FSS_Seminar Room I-102', 'MSBM-N'),
    ('FSS_Faculty Room', 'MSBM-S'),
    ('FSS_SR2', 'MSBM-N'),
    ('FSS_SR4', 'FSS-2'),
    ('FSS_SR5', 'FSS-2'),
    ('FSS_SR6', 'FSS-2'),
    ('FSS_SR8', 'FSS-2'),
    ('FSS_SR10', 'MSBM-S'),
    ('FSS_SR11', 'MSBM-S'),
    ('FSS_SR12', 'MSBM-S'),
    ('FSS_SR14', 'MSBM-S'),
    ('FSS_SR15', 'MSBM-S'),
    ('FSS_SR16', 'MSBM-S'),
    ('FSS_SR17', 'MSBM-S'),
    ('FSS_SR23', 'MSBM-S'),
    ('FSS_SSLT', 'SSLT'),
    ('FSS_TR10', 'FSS-3'),
    ('FSS_TR11', 'FSS-3'),
    ('FSS_TR12', 'FSS-3'),
    ('FSS_TR20', 'FSS-3'),
    ('FSS_Computer Lab H-101', 'MSBM-N'),
    ('FSS_Computer Lab E-102', 'MSBM-N'),
    ('FSS_Computer Lab Annex E-105', 'MSBM-N'),
    ('FSS_MSBM Computer Lab Main', 'MSBM-S'),
    ('FSS_MSBM Computer Lab Graduate', 'MSBM-S'),
    ('FSS_MSBM Computer Lab Annex', 'MSBM-S'),
    ('FSS_ExecutiveSR1', 'MSBM-N'),
    ('FSS_ExecutiveSR2', 'MSBM-N'),
    ('FSS_ExecutiveLT', 'MSBM-N'),
    ('FSS_SALISES Seminar Room', 'FSS-4'),
    ('FSS_SALISES Conference Rm1', 'FSS-4'),
    ('FSS_SALISES Conference Rm2', 'FSS-4'),
    ('FHE_Arts01', 'FHE-1'),
    ('FHE_Arts02', 'FHE-1'),
    ('FHE_Arts03', 'FHE-1'),
    ('FHE_Arts04', 'FHE-1'),
    ('FHE_N1', 'FHE-2'),
    ('FHE_N2', 'FHE-2'),
    ('FHE_N3', 'FHE-2'),
    ('FHE_N4', 'FHE-2'),
    ('FST_BioLT', 'FST-2'),
    ('FST_Chem2', 'FST-2'),
    ('FST_Chem5', 'FST-2'),
    ('FST_Chem7', 'FST-2'),
    ('FST_Chem/PhysLT', 'FST-2'),
    ('FST_IFLT', 'FST-1'),
    ('FST_IFSR1', 'FST-1'),
    ('FST_IFSR2', 'FST-1'),
    ('FST_Science-LT1', 'FST-2'),
    ('FST_Science-LT2', 'FST-2'),
    ('FST_Science-LT3', 'FST-2');

-- Populating Map table with distance between buildings
INSERT INTO Map (sBuilding, eBuilding, Distance) VALUES
    ('MSBM-S', 'FST-1', 6),
    ('MSBM-S', 'FSS-1', 1),
    ('MSBM-S', 'FSS-4', 1),
    ('MSBM-S', 'FHE-1', 5),
    ('MSBM-N', 'FSS-3', 2),
    ('FSS-1', 'FSS-2', 1),
    ('FSS-1', 'SSLT', 1),
    ('FSS-2', 'FSS-3', 1),
    ('FSS-2', 'FSS-4', 1),
    ('FSS-2', 'SSLT', 1),
    ('FSS-3', 'SSLT', 1),
    ('FST-1', 'FST-2', 1),
    ('FHE-1', 'FHE-2', 1);

-- Populate the Equipment table
INSERT INTO Equipment (EquipmentID,EType) VALUES 
	(1,'Laptop'),
	(2,'Laptop'),
    (3,'Projector'),
    (4,'Projector'),
    (5,'Surge Protector'),
    (6,'Surge Protector'),
    (7,'Surge Protector'),
    (8,'HDMI Cord'),
    (9,'HDMI Cord'),
    (10,'HDMI Cord');
    
select * from SATAvailability;
INSERT INTO SATAvailability (StudentID,DayOfWeek,StartTime,EndTime) VALUES (1,"Monday","08:00:00","12:00:00");
SELECT RequestID,ClassLocation FROM Request WHERE TIMEDIFF("9:0:00","9:0:00") = 0 AND (DayOfWeek = "Monday");
DROP table Lecturer;