
INSERT INTO Sun_Requirement (req_id, requirement) VALUES
(1,Full Sun);
INSERT INTO Sun_Requirement (req_id, requirement) VALUES
(2,Full Sun / Part Shade);
INSERT INTO Sun_Requirement (req_id, requirement) VALUES
(3,Part Shade);
INSERT INTO Sun_Requirement (req_id, requirement) VALUES
(4,Full Shade);
INSERT INTO Sun_Requirement (req_id, requirement) VALUES



INSERT INTO Soil_Requirement (req_id, requirement) VALUES
(1,Sandy / Dry);
INSERT INTO Soil_Requirement (req_id, requirement) VALUES
(2,Loamy);
INSERT INTO Soil_Requirement (req_id, requirement) VALUES
(3,Sandy / Clay);
INSERT INTO Soil_Requirement (req_id, requirement) VALUES
(4,Well-drained);
INSERT INTO Soil_Requirement (req_id, requirement) VALUES
(5,Moist / Rich);
INSERT INTO Soil_Requirement (req_id, requirement) VALUES
(6,Moist);

INSERT INTO Water_Requirement (req_id, requirement) VALUES
(1,Low);
INSERT INTO Water_Requirement (req_id, requirement) VALUES
(2,Low / Medium);
INSERT INTO Water_Requirement (req_id, requirement) VALUES
(3,Medium);
INSERT INTO Water_Requirement (req_id, requirement) VALUES
(4,Medium / High);
INSERT INTO Water_Requirement (req_id, requirement) VALUES
(5,High);

INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(1,Asclepias tuberosa,Butterfly Weed,1,1,1,"Full sun, dry soil specialist; monarch host plant");
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(2,Echinacea purpurea,Purple Coneflower,2,2,3,Adaptable prairie perennial; medicinal uses);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(3,Lobelia cardinalis,Cardinal Flower,3,5,5,Shade-tolerant; brilliant red; hummingbird magnet);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(4,Andropogon gerardii,Big Bluestem,1,3,2,Dominant tallgrass prairie grass; deep roots);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(5,Baptisia australis,Blue Wild Indigo,1,4,1,"Drought tolerant legume; slow to establish");
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(6,Monarda fistulosa,Wild Bergamot,1,2,3,Fragrant lavender blooms; excellent for bees);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(7,Sorghastrum nutans,Indiangrass,1,3,1,Warm season grass; golden fall color);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(8,Penstemon digitalis,Foxglove Beardtongue,2,2,3,Tolerates clay; white tubular flowers);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(9,Rudbeckia hirta,Black-eyed Susan,1,4,2,Classic adaptable wildflower; very hardy);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(10,Zizia aurea,Golden Alexanders,3,6,4,Early spring bloomer; supports specialist bees);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(11,Trillium grandiflorum,White Trillium,4,5,4,Full shade woodland wildflower; slow growing);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(12,Aquilegia canadensis,Wild Columbine,3,4,3,Part shade; red and yellow; hummingbird favorite);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(13,Carex pensylvanica,Pennsylvania Sedge,4,2,3,Full shade groundcover; low maintenance);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(14,Mertensia virginica,Virginia Bluebells,3,5,4,Spring ephemeral; moist woodland edges,);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(15,Spartina pectinata,Prairie Cordgrass,1,6,5,Full sun; wet to moist; excellent erosion control);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(16,Iris virginica,Southern Blue Flag,2,6,5,Wetland iris; blue-violet blooms);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(17,Solidago canadensis,Canada Goldenrod,2,2,2,Adaptable; late season pollinator powerhouse);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(18,Symphyotrichum novae-angliae,New England Aster,2,3,3,Fall bloomer; critical for migrating monarchs);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(19,Schizachyrium scoparium,Little Bluestem,1,1,1,Dry sandy soil specialist; stunning fall color);
INSERT INTO Species (species_id, common_name, scietific_name, sun_req, soil_req, water_req, description) VALUES
(20,Podophyllum peltatum,Mayapple,4,5,3,Full shade groundcover; spreads by rhizome);

INSERT INTO Partner (partner_id, p_name, contact, email, address) VALUES
();

INSERT INTO Member (member_id, f_name, l_name, email, join_date, status) VALUES
();

INSERT INTO Location (location_id, partner_id, loc_name, loc_type, address) VALUES
();

INSERT INTO Batch (batch_id, collection_loc, storage_loc, species_id, collected_by, date, start_quantity, current_quantity) VALUES
();

INSERT INTO Distribution (dist_id, member_id, batch_id, quantity, date) VALUES
();

INSERT INTO Event (event_id, loc_id, event_name, event_date, event_type) VALUES
();

INSERT INTO Event_member (event_id, member_id) VALUES
();

INSERT INTO Event_guest (event_id, guest_email, guest_name) VALUES
();

INSERT INTO Activity_log (activity_id, member_id, loc_id, hours, date, description) VALUES
();