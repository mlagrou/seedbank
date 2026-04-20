
CREATE DATABASE SV_Seedbank_DB; 

USE SV_Seedbank_DB; 

CREATE TABLE Sun_Requirement(
    req_id INT PRIMARY KEY, 
    requirement VARCHAR(100) NOT NULL

);
CREATE TABLE Soil_Requirement(
    req_id INT PRIMARY KEY, 
    requirement VARCHAR(100) NOT NULL

);
CREATE TABLE Water_Requirement(
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
    FOREIGN KEY(water_req) REFERENCES Water_Requirement(req_id)
);

CREATE TABLE Partner(

    partner_id INT PRIMARY KEY ,
    p_name VARCHAR(100) NOT NULL,
    contact VARCHAR(100), 
    email VARCHAR(100) NOT NULL, 
    address VARCHAR(150) 

);

CREATE TABLE Member (

    member_id INT PRIMARY KEY, 
    f_name VARCHAR(100) NOT NULL,
    l_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL, 
    join_date DATE NOT NULL, 
    status VARCHAR(100) NOT NULL


);

CREATE TABLE Location (
    location_id INT PRIMARY KEY,
    partner_id INT,
    loc_name VARCHAR(100) NOT NULL,
    loc_type VARCHAR (100),
    address VARCHAR(150) NOT NULL,

    FOREIGN KEY (partner_id) REFERENCES Partner(partner_id)
);

CREATE TABLE Batch (
    batch_id INT PRIMARY KEY, 
    collection_loc INT NOT NULL, 
    storage_loc INT, 
    species_id INT NOT NULL, 
    collected_by INT, 
    date DATE NOT NULL, 
    start_quantity INT NOT NULL, 
    current_quantity INT NOT NULL,

    FOREIGN KEY(collection_loc) REFERENCES Location(location_id),
    FOREIGN KEY(storage_loc) REFERENCES Location(location_id),
    FOREIGN KEY(species_id) REFERENCES Species(species_id),
    FOREIGN KEY(collected_by) REFERENCES Member(member_id)

);

CREATE TABLE Distribution(
    dist_id INT PRIMARY KEY,
    batch_id INT NOT NULL, 
    member_id INT NOT NULL, 
    quantity INT NOT NULL, 
    date DATE NOT NULL, 

    FOREIGN KEY(member_id) REFERENCES Member(member_id), 
    FOREIGN KEY(batch_id) REFERENCES Batch(batch_id)
);


CREATE TABLE Event (
    event_id INT PRIMARY KEY,
    loc_id INT NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    event_type VARCHAR(50),

    FOREIGN KEY(loc_id) REFERENCES Location(location_id)
);

CREATE TABLE Event_member (
    event_id INT,
    member_id INT,

    PRIMARY KEY(event_id, member_id),
    FOREIGN KEY(event_id) REFERENCES Event(event_id),
    FOREIGN KEY(member_id) REFERENCES Member(member_id)
);

CREATE TABLE Event_guest (
    event_id INT,
    guest_email VARCHAR(100),
    guest_name VARCHAR(100),

    PRIMARY KEY(event_id, guest_email),
    FOREIGN KEY(event_id) REFERENCES Event(event_id)
);

CREATE TABLE Activity_log (
    activity_id INT PRIMARY KEY,
    member_id INT NOT NULL,
    loc_id INT NOT NULL,
    hours DECIMAL(4,1) NOT NULL,
    date DATE NOT NULL,
    description TEXT,

    FOREIGN KEY(member_id) REFERENCES Member(member_id),
    FOREIGN KEY(loc_id) REFERENCES Location(location_id)
);

