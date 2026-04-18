
CREATE DATABASE SV_Seedbank_DB; 

USE employee_db; 

CREATE TABLE SunRequirement(
    req_id INT PRIMARY KEY, 
    requirement VARCHAR(100) NOT NULL

);
CREATE TABLE SoilRequirement(
    req_id INT PRIMARY KEY, 
    requirement VARCHAR(100) NOT NULL

);
CREATE TABLE WaterRequirement(
    req_id INT PRIMARY KEY, 
    requirement VARCHAR(100) NOT NULL

);

CREATE TABLE Species(

    species_id INT PRIMARY KEY,
    common_name VARCHAR(100) NOT NULL,
    scietific_name VARCHAR(100)NOT NULL, 
    sun_req INT NOT NULL,
    soil_req INT NOT NULL, 
    water_req INT NOT NULL, 
    description TEXT, 

    FOREIGN KEY(sun_req) REFERENCES Sun_Requirement(req_id),
    FOREIGN KEY(soil_req) REFERENCES Soil_Requirement(req_id),
    FOREIGN KEY(water_req) REFERENCES WaterRequirements(req_id)
);

CREATE TABLE Partner(

    partner_id INT PRIMARY KEY ,
    p_name VARCHAR(100) NOT NULL,
    contact VARCHAR(100), 
    email VARCHAR(100) NOT NULL, 
    address VARCHAR(150) 

);

ALTER TABLE DEPARTMENT ADD CONSTRAINT foreignKey FOREIGN KEY(Mgr_ssn) REFERENCES EMPLOYEE(Ssn);

CREATE TABLE DEPT_LOCATIONS (

    Dnumber INTEGER,
    Dlocation VARCHAR(50),

    PRIMARY KEY(Dnumber, Dlocation),

    FOREIGN KEY(Dnumber) REFERENCES DEPARTMENT(Dnumber)


);

CREATE TABLE PROJECT (
    Pname VARCHAR(50) NOT NULL,
    Pnumber INTEGER PRIMARY KEY,
    Plocation VARCHAR(50) NOT NULL,
    Dnum INTEGER,

    FOREIGN KEY (Dnum) REFERENCES DEPARTMENT(Dnumber)
);

CREATE TABLE WORKS_ON (
    Essn CHAR(9),
    Pno INTEGER,
    Hours DECIMAL,

    PRIMARY KEY(Essn, Pno),

    FOREIGN KEY(Essn) REFERENCES EMPLOYEE(Ssn),
    FOREIGN KEY(Pno) REFERENCES PROJECT(Pnumber)
);

CREATE TABLE DEPENDENT(
    Essn CHAR(9), 
    Dependent_name VARCHAR(30), 
    Sex CHAR(1),
    Bdate DATE,
    Relationship VARCHAR(30),

    PRIMARY KEY(Essn, Dependent_name),

    FOREIGN KEY(Essn) REFERENCES EMPLOYEE(Ssn)
);

