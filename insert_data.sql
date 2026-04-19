
INSERT INTO Sun_Requirement (req_id, requirement) VALUES
(1,'Full Sun'),
(2,'Full Sun / Part Shade'),
(3,'Part Shade'),
(4,'Full Shade');



INSERT INTO Soil_Requirement (req_id, requirement) VALUES
(1,'Sandy / Dry'),
(2,'Loamy'),
(3,'Sandy / Clay'),
(4,'Well-drained'),
(5,'Moist / Rich'),
(6,'Moist');

INSERT INTO Water_Requirement (req_id, requirement) VALUES
(1,'Low'),
(2,'Low / Medium'),
(3,'Medium'),
(4,'Medium / High'),
(5,'High');

INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(1,'Asclepias tuberosa','Butterfly Weed',1,1,1,"Full sun, dry soil specialist; monarch host plant"),
(2,'Echinacea purpurea','Purple Coneflower',2,2,3,'Adaptable prairie perennial; medicinal uses'),
(3,'Lobelia cardinalis','Cardinal Flower',3,5,5,'Shade-tolerant; brilliant red; hummingbird magnet'),
(4,'Andropogon gerardii','Big Bluestem',1,3,2,'Dominant tallgrass prairie grass; deep roots'),
(5,'Baptisia australis','Blue Wild Indigo',1,4,1,"Drought tolerant legume; slow to establish"),
(6,'Monarda fistulosa,Wild Bergamot',1,2,3,'Fragrant lavender blooms; excellent for bees'),
(7,'Sorghastrum nutans','Indiangrass',1,3,1,'Warm season grass; golden fall color'),
(8,'Penstemon digitalis','Foxglove Beardtongue',2,2,3,'Tolerates clay; white tubular flowers'),
(9,'Rudbeckia hirta','Black-eyed Susan',1,4,2,'Classic adaptable wildflower; very hardy'),
(10,'Zizia aurea','Golden Alexanders',3,6,4,'Early spring bloomer; supports specialist bees'),
(11,'Trillium grandiflorum','White Trillium',4,5,4,'Full shade woodland wildflower; slow growing'),
(12,'Aquilegia canadensis','Wild Columbine',3,4,3,'Part shade'; 'red and yellow; hummingbird favorite)',
(13,Carex pensylvanica,Pennsylvania Sedge,4,2,3,Full shade groundcover; low maintenance),
(14,Mertensia virginica,Virginia Bluebells,3,5,4,Spring ephemeral; moist woodland edges,),
(15,Spartina pectinata,Prairie Cordgrass,1,6,5,Full sun; wet to moist; excellent erosion control),
(16,Iris virginica,Southern Blue Flag,2,6,5,Wetland iris; blue-violet blooms),
(17,Solidago canadensis,Canada Goldenrod,2,2,2,Adaptable; late season pollinator powerhouse),
(18,Symphyotrichum novae-angliae,New England Aster,2,3,3,Fall bloomer; critical for migrating monarchs),
(19,Schizachyrium scoparium,Little Bluestem,1,1,1,Dry sandy soil specialist; stunning fall color),
(20,Podophyllum peltatum,Mayapple,4,5,3,Full shade groundcover; spreads by rhizome);

INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(1,Saginaw Chippewa Tribal College,Dr. Anne Becker,abecker@sctc.edu,"2274 Enterprise Dr, Mt Pleasant MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(2,Dow Diamond Community Garden,Jorge Reyes,jreyes@dowdiamond.org,"1 Willow St, Midland MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(3,Bay City State Park,Linda Marsh,lmarsh@michigan.gov,"3582 State Park Dr, Bay City MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(4,Saginaw Basin Land Conservancy,Tom Gruber,tgruber@sblc.org,"5085 Mackinaw Rd, Saginaw MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(5,MSU Extension Saginaw County,Rachel Kim,kimr@msu.edu,"111 S Michigan Ave, Saginaw MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(6,Chippewa Nature Center,Paul Denton,pdenton@chippewanature.org,"400 S Badour Rd, Midland MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(7,Saginaw Valley State University,Dr. Lena Hart,lhart@svsu.edu,"7400 Bay Rd, University Center MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(8,Northside Community Garden,Amara Diallo,amara@nscgarden.org,"1820 N Michigan Ave, Saginaw MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(9,Great Lakes Bay Regional Alliance,Steve Nowak,snowak@glbra.org,"515 N Washington Ave, Saginaw MI");
INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
(10,Crow Island Woods Preserve,Janet Osei,josei@crowisland.org,"Crow Island Rd, Saginaw MI");


INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(1,Sarah,Kowalski,sarah.k@email.com,'2021-03-15',active);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(2,Marcus,Trent,mtrent@email.com,'2022-06-01',active);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(3,Dana,Flores,dflores@email.com,'2023-09-10',inactive);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(4,James,Obi,jobi@email.com,'2024-04-20',inactive);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(5,Priya,Nair,pnair@email.com,'2024-05-05',active);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(6,Tom,Walcott,twalcott@email.com,'2020-01-08',active);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(7,Celia,Beaumont,cbeaumont@email.com,'2021-11-03',active);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(8,Raj,Patel,rpatel@email.com,'2023-02-14',inactive);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(9,Nora,Stein,nstein@email.com,'2024-08-19',active);
INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
(10,Derek,Hung,dhung@email.com,'2019-06-22',active);

INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(1,1,SCTC Greenhouse,greenhouse,"2274 Enterprise Dr, Mt Pleasant MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(2,2,Dow Diamond Garden Plot A,garden,"1 Willow St, Midland MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(3,3,Bay City State Park Prairie,natural area,"3582 State Park Dr, Bay City MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(4,7,SVSU Seedbank Storage,storage facility,"7400 Bay Rd, University Center MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(5,1,SCTC Seed Lab,lab,"2274 Enterprise Dr, Mt Pleasant MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(6,6,Chippewa Nature Center Trail,natural area,"400 S Badour Rd, Midland MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(7,4,SBLC Restoration Site,restoration site,"5085 Mackinaw Rd, Saginaw MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(8,8,Northside Garden Plots,garden,"1820 N Michigan Ave, Saginaw MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(9,5,MSU Extension Office,office,"111 S Michigan Ave, Saginaw MI");
INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
(10,,Member Garden - Kowalski,private garden,Saginaw MI);


INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(1,1,1,50,'2024-03-10');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(2,3,1,100,'2024-04-02');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(3,2,2,75,'2024-04-1');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(4,1,3,30,'2024-07-01');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(5,6,4,200,'2024-08-05');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(6,7,5,150,'2024-03-25');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(7,10,6,10,'2024-07-20');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(8,2,8,80,'2024-05-10');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(9,1,9,70,'2024-06-03');
INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
(10,4,3,25,'2024-08-22');

INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(1,1,1,50,'2024-03-10');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(2,3,1,100,'2024-04-02');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(3,2,2,75,'2024-04-15');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(4,1,3,30,'2024-07-01');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(5,6,4,200,'2024-08-05');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(6,7,5,150,'2024-03-25');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(7,10,6,10,'2024-07-2');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(8,2,8,80,'2024-05-10');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(9,1,9,70,'2024-06-03');
INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
(10,4,3,25,'2024-08-2'2);

INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(1,2,Spring Seed Swap,'2024-04-06',member);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(2,3,Prairie Restoration Day,'2024-05-18',volunteer);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(3,1,Native Plant Workshop,'2024-06-15',educational);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(4,4,Fall Harvest & Processing,'2024-09-28',member);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(5,6,Chippewa Trail Walk,'2024-07-13',public);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(6,9,Partner Info Session,'2024-03-02',partner);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(7,8,Community Garden Planting,'2024-05-04',voluntee);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(8,7,SBLC Restoration Kickoff,'2024-08-10',volunteer);
INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
(9,5,School Outreach Demo,'2024-10-03',educational);

INSERT INTO Event_member (event_id, member_id) VALUES
(1,1);
INSERT INTO Event_member (event_id, member_id) VALUES
(1,2);
INSERT INTO Event_member (event_id, member_id) VALUES
(1, 4);
INSERT INTO Event_member (event_id, member_id) VALUES
(2, 1);
INSERT INTO Event_member (event_id, member_id) VALUES
(2,6);
INSERT INTO Event_member (event_id, member_id) VALUES
(3,2);
INSERT INTO Event_member (event_id, member_id) VALUES
(3,3);
INSERT INTO Event_member (event_id, member_id) VALUES
(4,1);
INSERT INTO Event_member (event_id, member_id) VALUES
(4,1);
INSERT INTO Event_member (event_id, member_id) VALUES
(4,10);
INSERT INTO Event_member (event_id, member_id) VALUES
(5,7);
INSERT INTO Event_member (event_id, member_id) VALUES
(6,10);
INSERT INTO Event_member (event_id, member_id) VALUES
(6, 6);
INSERT INTO Event_member (event_id, member_id) VALUES
(7,7);
INSERT INTO Event_member (event_id, member_id) VALUES
(8,1);
INSERT INTO Event_member (event_id, member_id) VALUES
(8,2);
INSERT INTO Event_member (event_id, member_id) VALUES
(9,10);
INSERT INTO Event_member (event_id, member_id) VALUES
(10,1);
INSERT INTO Event_member (event_id, member_id) VALUES
(10,6);
INSERT INTO Event_member (event_id, member_id) VALUES
(10,10);






INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(1,walkerin@gmail.com,Karen Walker);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(1,dsharma@gmail.com,Dev Sharma);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(2,lgravs@hotmail.com,Lila Graves);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(3,ohussain@email.com,Omar Hussain);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(3,tbrooks@yahoo.com,Tanya Brooks);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(4,mjanssen@gmail.com,Mike Janssen);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(5,rdelgado@email.com,Rosa Delgado);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(7,fcalloway@yahoo.com,Finn Calloway);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(8,ytanaka@gmail.com,Yuki Tanaka);
INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
(9,bcromwell@email.com,Beth Cromwell);

INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(1,1,5,3,2024-04-05,Seed cleaning);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(2,2,5,2.5,2024-04-05,Seed cleaning);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(3,6,3,4,2024-05-18,Prairie restoration planting);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(4,1,4,1.5,2024-06-10,Inventory update);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(5,3,4,2,2024-03-22,Packet assembly);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(6,7,6,3.5,2024-07-03,Field collection - Bergamot);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(7,10,10,5,2024-08-18,Field collection - Indiangrass);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(8,2,2,2,2024-09-28,Harvest processing);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(9,6,2,1,2024-09-28,Harvest processing);
INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
(10,1,4,3,2024-10-05,Species data entry);
