-- Species database module 
    -- 1. What species require full sun and low water?

    SELECT common_name, sun.requirement as "Sun Requirement", water.requirement as "Water Requirement"
    FROM species, sun_requirement sun,  water_requirement water
    WHERE sun_req = sun.req_id 
    AND water_req = water.req_id
    AND sun.requirement = "Full Sun"
    AND water.requirement = "Low"

    --2. What species have never had seeds collected?

    SELECT common_name
    FROM species
    WHERE species_id NOT IN(
            SELECT species_id 
            FROM batch
)



-- Seed inventory module 
    --3. What is the current seed inventory, sorted alphabetically by common name?

    SELECT common_name, SUM(current_quantity) as Quantity
    FROM batch b, species s
    WHERE b.species_id = s.species_id
    GROUP BY common_name LIMIT 0, 25


-- Seed batch module 
    --4. Hhow many batches, and how many total seeds, have been collected from each location?

    SELECT loc_name as Location, COUNT(batch_id) as Batches, SUM(start_quantity) as "Total Seeds"
    FROM location l, batch b
    WHERE l.location_id = b.collection_loc
    GROUP BY loc_name

    --5. Which members have collected an above average number of batches?

    SELECT l_name AS "Last Name", f_name AS "First Name", COUNT(batch_id) as "Count"
    FROM member, batch
    WHERE collected_by = member_id 
    GROUP BY l_name, f_name
    HAVING COUNT(batch_id) > ( SELECT AVG(BATCH_COUNT)
                            FROM (SELECT COUNT(batch_id) AS BATCH_COUNT
                                    FROM batch
                                    GROUP BY collected_by) AS CB
                            )


--Member / Volunteer module 
    -- 6. How many hours has each active member volunteered?

    SELECT f_name as "First Name", l_name as "Last Name", SUM(hours) as Hours
    FROM member m, activity_log a
    WHERE m.member_id = a.member_id
    AND m.status = "active"
    GROUP BY f_name, l_name 

-- Distribution module 
    --7. Who has received which species of seeds, and how many?

    SELECT f_name as "First Name", l_name as "Last Name", common_name as "Species", SUM(quantity) as "Seeds Dispersed"
    FROM member m, species s, distribution d, batch b
    WHERE m.member_id = d.member_id
    AND s.species_id = b.species_id
    AND d.batch_id = b.batch_id
    GROUP BY f_name, l_name, common_name

-- Partner module 
    -- 8. Which partners have collection locations?

    SELECT p_name AS "Partner", loc_name AS "Location", loc_type AS "Type"
    FROM partner p, location l
    WHERE p.partner_id = l.partner_id;

-- Education module
    --9. What are the 3 most popular events and what was the attendence of each?

    SELECT event_name as "Event", COUNT(DISTINCT m.member_id) + COUNT(DISTINCT g.guest_email) AS "Total Attendees"
    FROM event e
    LEFT JOIN event_member m ON e.event_id = m.event_id
    LEFT JOIN event_guest g ON e.event_id = g.event_id
    GROUP BY event_name
    ORDER BY COUNT(DISTINCT m.member_id) + COUNT(DISTINCT g.guest_email) DESC
    LIMIT 3

    --10. Return a list of every guest and their emails who has attended at least 1 event
    SELECT DISTINCT guest_name as "Name", guest_email as "Email"
    FROM event_guest

-- Reporting / Analytics 
    --11.  List seeds collected vs seed distributed for each species

    SELECT common_name AS "Species", SUM(b.start_quantity) AS "Seeds Collected", SUM(d.quantity) AS "Seeds Distributed"
    FROM species s
    JOIN batch b ON s.species_id = b.species_id
    LEFT JOIN distribution d ON b.batch_id = d.batch_id
    GROUP BY common_name;

