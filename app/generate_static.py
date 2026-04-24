"""
Run this script once to generate a static index.html for GitHub Pages.
Usage: python generate_static.py
Output: ../docs/index.html  (GitHub Pages reads from /docs by default)
"""

import os
import mysql.connector
from pymongo import MongoClient

# ── Connections ────────────────────────────────────────
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "mysql",
    "database": "SV_Seedbank_DB"
}

MONGO_URI = "mongodb+srv://matt:lagrou@lagrou355.qp9qtge.mongodb.net/noteapp?retryWrites=true&w=majority"

def run_sql(query):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cur = conn.cursor(dictionary=True)
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        return [{"error": str(e)}]

def run_mongo(fn):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["SV_Seedbank"]
        rows = list(fn(db))
        for row in rows:
            if "_id" in row:
                row["id"] = str(row.pop("_id"))
        client.close()
        return rows
    except Exception as e:
        return [{"error": str(e)}]


# ── Data ───────────────────────────────────────────────
pages = {
    "species": {
        "title": "Species",
        "sql": run_sql("SELECT common_name, scietific_name, description FROM Species ORDER BY common_name"),
    },
    "batch": {
        "title": "Batches",
        "sql": run_sql("""
            SELECT b.batch_id, s.common_name AS species, cl.loc_name AS collection_loc,
                   sl.loc_name AS storage_loc, CONCAT(m.f_name,' ',m.l_name) AS collected_by,
                   b.date, b.start_quantity, b.current_quantity
            FROM Batch b
            JOIN Species s ON b.species_id = s.species_id
            JOIN Location cl ON b.collection_loc = cl.location_id
            LEFT JOIN Location sl ON b.storage_loc = sl.location_id
            LEFT JOIN Member m ON b.collected_by = m.member_id
            ORDER BY b.date DESC
        """),
    },
    "members": {
        "title": "Members",
        "sql": run_sql("SELECT member_id, f_name, l_name, email, join_date, status FROM Member ORDER BY l_name"),
    },
    "activities": {
        "title": "Activity Log",
        "sql": run_sql("""
            SELECT a.activity_id, m.f_name AS first_name, m.l_name AS last_name,
                   l.loc_name AS location, a.hours, a.date, a.description
            FROM Activity_log a
            JOIN Member m ON a.member_id = m.member_id
            JOIN Location l ON a.loc_id = l.location_id
            ORDER BY a.date DESC
        """),
    },
    "distributions": {
        "title": "Distributions",
        "sql": run_sql("""
            SELECT m.f_name AS first_name, m.l_name AS last_name,
                   s.common_name AS species, SUM(d.quantity) AS seeds_dispersed
            FROM Member m, Species s, Distribution d, Batch b
            WHERE m.member_id = d.member_id AND s.species_id = b.species_id AND d.batch_id = b.batch_id
            GROUP BY m.f_name, m.l_name, s.common_name ORDER BY m.l_name
        """),
    },
    "events": {
        "title": "Events",
        "sql": run_sql("""
            SELECT e.event_name, e.event_date, e.event_type, l.loc_name AS location
            FROM Event e, Location l WHERE e.loc_id = l.location_id ORDER BY e.event_date DESC
        """),
    },
    "guests": {
        "title": "Guests",
        "sql": run_sql("""
            SELECT e.event_name, g.guest_name AS name, g.guest_email AS email
            FROM Event_guest g JOIN Event e ON g.event_id = e.event_id
            ORDER BY e.event_name, g.guest_name
        """),
    },
    "partners": {
        "title": "Partners",
        "sql": run_sql("SELECT p_name, contact, email, address FROM Partner ORDER BY p_name"),
    },
}

analytics = [
    {
        "number": 1,
        "question": "What species require Full Sun and Low water?",
        "sql_text": "SELECT s.common_name, sun.requirement AS sun_req, water.requirement AS water_req\nFROM Species s, Sun_Requirement sun, Water_Requirement water\nWHERE s.sun_req = sun.req_id AND s.water_req = water.req_id\n  AND sun.requirement = 'Full Sun' AND water.requirement = 'Low'",
        "mongo_text": 'db["Species"].find({$and:[{"requirements.sun":"Full Sun"},{"requirements.water":"Low"}]})',
        "sql": run_sql("""
            SELECT s.common_name, sun.requirement AS sun_req, water.requirement AS water_req
            FROM Species s, Sun_Requirement sun, Water_Requirement water
            WHERE s.sun_req = sun.req_id AND s.water_req = water.req_id
              AND sun.requirement = 'Full Sun' AND water.requirement = 'Low'
        """),
        "mongo": run_mongo(lambda db: db["Species"].find(
            {"$and": [{"requirements.sun": "Full Sun"}, {"requirements.water": "Low"}]},
            {"_id": 0, "common_name": 1, "requirements": 1}
        )),
    },
    {
        "number": 2,
        "question": "What species have never had seeds collected?",
        "sql_text": "SELECT common_name FROM Species\nWHERE species_id NOT IN (SELECT species_id FROM Batch)",
        "mongo_text": "db['Species'].aggregate([\n  {$lookup:{from:'Batch',localField:'common_name',foreignField:'species',as:'species'}},\n  {$match:{species:{$size:0}}}\n])",
        "sql": run_sql("SELECT common_name FROM Species WHERE species_id NOT IN (SELECT species_id FROM Batch)"),
        "mongo": run_mongo(lambda db: db["Species"].aggregate([
            {"$lookup": {"from": "Batch", "localField": "common_name", "foreignField": "species", "as": "batches"}},
            {"$match": {"batches": {"$size": 0}}},
            {"$project": {"_id": 0, "common_name": 1}}
        ])),
    },
    {
        "number": 3,
        "question": "What is the current seed inventory, sorted alphabetically by common name?",
        "sql_text": "SELECT common_name, SUM(current_quantity) AS quantity\nFROM Batch b, Species s WHERE b.species_id = s.species_id\nGROUP BY common_name ORDER BY common_name",
        "mongo_text": 'db["Batch"].aggregate([{$group:{_id:"$species", totalInventory:{$sum:"$current_quantity"}}}])',
        "sql": run_sql("""
            SELECT s.common_name, SUM(b.current_quantity) AS quantity
            FROM Batch b, Species s WHERE b.species_id = s.species_id
            GROUP BY s.common_name ORDER BY s.common_name
        """),
        "mongo": run_mongo(lambda db: db["Batch"].aggregate([
            {"$group": {"_id": "$species", "totalInventory": {"$sum": "$current_quantity"}}},
            {"$sort": {"_id": 1}}
        ])),
    },
    {
        "number": 4,
        "question": "How many batches and total seeds have been collected from each location?",
        "sql_text": "SELECT loc_name AS location, COUNT(batch_id) AS batches, SUM(start_quantity) AS total_seeds\nFROM Location l, Batch b WHERE l.location_id = b.collection_loc\nGROUP BY loc_name ORDER BY total_seeds DESC",
        "mongo_text": 'db["Batch"].aggregate([\n  {$group:{_id:"$collection_loc.name", collectionEvents:{$sum:1}, totalSeeds:{$sum:"$start_quantity"}}},\n  {$sort:{collectionEvents:-1}}\n])',
        "sql": run_sql("""
            SELECT l.loc_name AS location, COUNT(b.batch_id) AS batches, SUM(b.start_quantity) AS total_seeds
            FROM Location l, Batch b WHERE l.location_id = b.collection_loc
            GROUP BY l.loc_name ORDER BY total_seeds DESC
        """),
        "mongo": run_mongo(lambda db: db["Batch"].aggregate([
            {"$group": {"_id": "$collection_loc.name", "collectionEvents": {"$sum": 1}, "totalSeeds": {"$sum": "$start_quantity"}}},
            {"$sort": {"collectionEvents": -1}}
        ])),
    },
    {
        "number": 5,
        "question": "Which members have collected an above-average number of batches? (MongoDB: total hours per member)",
        "sql_text": "SELECT l_name, f_name, COUNT(batch_id) AS batch_count\nFROM Member, Batch WHERE collected_by = member_id\nGROUP BY l_name, f_name\nHAVING COUNT(batch_id) > (SELECT AVG(bc) FROM (SELECT COUNT(batch_id) AS bc FROM Batch GROUP BY collected_by) AS sub)",
        "mongo_text": 'db["Activities"].aggregate([{$group:{_id:"$member", totalHours:{$sum:"$hours"}}}])',
        "sql": run_sql("""
            SELECT m.l_name AS last_name, m.f_name AS first_name, COUNT(b.batch_id) AS batch_count
            FROM Member m, Batch b WHERE b.collected_by = m.member_id
            GROUP BY m.l_name, m.f_name
            HAVING COUNT(b.batch_id) > (SELECT AVG(bc) FROM (SELECT COUNT(batch_id) AS bc FROM Batch GROUP BY collected_by) AS sub)
            ORDER BY batch_count DESC
        """),
        "mongo": run_mongo(lambda db: db["Activities"].aggregate([
            {"$group": {"_id": "$member", "totalHours": {"$sum": "$hours"}}}
        ])),
    },
    {
        "number": 6,
        "question": "How many hours has each active member volunteered? (MongoDB: distributions per member)",
        "sql_text": "SELECT f_name, l_name, SUM(hours) AS hours\nFROM Member m, Activity_log a WHERE m.member_id = a.member_id AND m.status = 'active'\nGROUP BY f_name, l_name ORDER BY hours DESC",
        "mongo_text": 'db["Distribution"].aggregate([{$group:{_id:"$member", numberBatches:{$sum:1}}}])',
        "sql": run_sql("""
            SELECT m.f_name AS first_name, m.l_name AS last_name, SUM(a.hours) AS hours
            FROM Member m, Activity_log a WHERE m.member_id = a.member_id AND m.status = 'active'
            GROUP BY m.f_name, m.l_name ORDER BY hours DESC
        """),
        "mongo": run_mongo(lambda db: db["Distribution"].aggregate([
            {"$group": {"_id": "$member", "numberBatches": {"$sum": 1}}}
        ])),
    },
    {
        "number": 7,
        "question": "Who has received which species of seeds, and how many? (MongoDB: seeds dispersed per species)",
        "sql_text": "SELECT f_name, l_name, common_name AS species, SUM(quantity) AS seeds_dispersed\nFROM Member m, Species s, Distribution d, Batch b\nWHERE m.member_id=d.member_id AND s.species_id=b.species_id AND d.batch_id=b.batch_id\nGROUP BY f_name, l_name, common_name",
        "mongo_text": 'db["Distribution"].aggregate([{$group:{_id:"$species", seedDispersed:{$sum:"$quantity"}}}])',
        "sql": run_sql("""
            SELECT m.f_name AS first_name, m.l_name AS last_name,
                   s.common_name AS species, SUM(d.quantity) AS seeds_dispersed
            FROM Member m, Species s, Distribution d, Batch b
            WHERE m.member_id = d.member_id AND s.species_id = b.species_id AND d.batch_id = b.batch_id
            GROUP BY m.f_name, m.l_name, s.common_name ORDER BY m.l_name
        """),
        "mongo": run_mongo(lambda db: db["Distribution"].aggregate([
            {"$group": {"_id": "$species", "seedDispersed": {"$sum": "$quantity"}}}
        ])),
    },
    {
        "number": 8,
        "question": "Which partners have collection locations? (MongoDB: all partners with name, contact, address)",
        "sql_text": "SELECT p_name AS partner, loc_name AS location, loc_type AS type\nFROM Partner p, Location l WHERE p.partner_id = l.partner_id",
        "mongo_text": 'db["Partners"].find({}, {_id:0, p_name:1, contact:1, address:1})',
        "sql": run_sql("""
            SELECT p.p_name AS partner, l.loc_name AS location, l.loc_type AS type
            FROM Partner p, Location l WHERE p.partner_id = l.partner_id ORDER BY p.p_name
        """),
        "mongo": run_mongo(lambda db: db["Partners"].find({}, {"_id": 0, "p_name": 1, "contact": 1, "address": 1})),
    },
    {
        "number": 9,
        "question": "What are the 3 most popular events and what was the attendance of each?",
        "sql_text": "SELECT event_name, COUNT(DISTINCT m.member_id) + COUNT(DISTINCT g.guest_email) AS total_attendees\nFROM Event e\nLEFT JOIN Event_member m ON e.event_id = m.event_id\nLEFT JOIN Event_guest g ON e.event_id = g.event_id\nGROUP BY event_name ORDER BY total_attendees DESC LIMIT 3",
        "mongo_text": 'db["Events"].aggregate([\n  {$group:{_id:"$event_name", attendance:{$sum:{$add:[{$size:"$guest_attendance"},{$size:"$member_attendance"}]}}}},\n  {$sort:{attendance:-1}}, {$limit:3}\n])',
        "sql": run_sql("""
            SELECT e.event_name,
                   COUNT(DISTINCT m.member_id) + COUNT(DISTINCT g.guest_email) AS total_attendees
            FROM Event e
            LEFT JOIN Event_member m ON e.event_id = m.event_id
            LEFT JOIN Event_guest g ON e.event_id = g.event_id
            GROUP BY e.event_name ORDER BY total_attendees DESC LIMIT 3
        """),
        "mongo": run_mongo(lambda db: db["Events"].aggregate([
            {"$group": {"_id": "$event_name", "attendance": {"$sum": {"$add": [{"$size": "$guest_attendance"}, {"$size": "$member_attendance"}]}}}},
            {"$sort": {"attendance": -1}},
            {"$limit": 3}
        ])),
    },
    {
        "number": 10,
        "question": "Return a list of every guest and their email who has attended at least 1 event.",
        "sql_text": "SELECT DISTINCT guest_name AS name, guest_email AS email FROM Event_guest ORDER BY guest_name",
        "mongo_text": 'db["Events"].aggregate([\n  {$unwind:"$guest_attendance"},\n  {$project:{_id:0, name:"$guest_attendance.name", email:"$guest_attendance.email"}}\n])',
        "sql": run_sql("SELECT DISTINCT guest_name AS name, guest_email AS email FROM Event_guest ORDER BY guest_name"),
        "mongo": run_mongo(lambda db: db["Events"].aggregate([
            {"$unwind": "$guest_attendance"},
            {"$project": {"_id": 0, "name": "$guest_attendance.name", "email": "$guest_attendance.email"}}
        ])),
    },
]


# ── HTML Helpers ───────────────────────────────────────
def make_table(rows):
    if not rows:
        return '<p class="text-muted">No results.</p>'
    if "error" in rows[0]:
        return f'<p class="text-danger">{rows[0]["error"]}</p>'
    cols = list(rows[0].keys())
    th = "".join(f"<th>{c}</th>" for c in cols)
    trs = ""
    for row in rows:
        tds = "".join(f"<td>{v if v is not None else '—'}</td>" for v in row.values())
        trs += f"<tr>{tds}</tr>"
    return f"""
    <div class="table-responsive">
      <table class="table table-sm table-bordered table-hover mb-0">
        <thead><tr>{th}</tr></thead>
        <tbody>{trs}</tbody>
      </table>
    </div>"""

def make_page_section(key, page):
    table = make_table(page["sql"])
    return f"""
    <section id="{key}" class="mb-5">
      <h2>{page["title"]}</h2>
      {table}
    </section>"""

def make_analytics_section(q):
    sql_table = make_table(q["sql"])
    mongo_table = make_table(q["mongo"])
    uid = q["number"]
    return f"""
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-header" style="background-color:#d8f3dc;">
        <strong>Q{uid}.</strong> {q["question"]}
      </div>
      <div class="card-body p-0">
        <ul class="nav nav-tabs px-3 pt-2" role="tablist">
          <li class="nav-item">
            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#sql{uid}">MySQL</button>
          </li>
          <li class="nav-item">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#mongo{uid}">MongoDB</button>
          </li>
        </ul>
        <div class="tab-content px-3 pb-3 pt-2">
          <div class="mb-2">
            <div id="sqltext{uid}"><pre class="bg-light border rounded p-2 small mb-2" style="white-space:pre-wrap;">{q["sql_text"]}</pre></div>
            <div id="mongotext{uid}" style="display:none;"><pre class="bg-light border rounded p-2 small mb-2" style="white-space:pre-wrap;">{q["mongo_text"]}</pre></div>
          </div>
          <div class="tab-pane fade show active" id="sql{uid}">{sql_table}</div>
          <div class="tab-pane fade" id="mongo{uid}">{mongo_table}</div>
        </div>
      </div>
    </div>"""


# ── Build HTML ─────────────────────────────────────────
nav_links = "".join(
    f'<li class="nav-item"><a class="nav-link" href="#{k}">{v["title"]}</a></li>'
    for k, v in pages.items()
)
nav_links += '<li class="nav-item"><a class="nav-link" href="#analytics">Analytics</a></li>'

page_sections = "".join(make_page_section(k, v) for k, v in pages.items())
analytics_cards = "".join(make_analytics_section(q) for q in analytics)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SV Seedbank</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background-color: #f5f8f2; }}
    .navbar {{ background-color: #2d6a4f !important; position: sticky; top: 0; z-index: 1000; }}
    .navbar-brand, .nav-link {{ color: #fff !important; }}
    .nav-link:hover {{ color: #b7e4c7 !important; }}
    h2 {{ color: #2d6a4f; margin-top: 1.5rem; }}
    .table thead {{ background-color: #40916c; color: white; }}
  </style>
</head>
<body>
<nav class="navbar navbar-expand-lg mb-4">
  <div class="container">
    <a class="navbar-brand fw-bold" href="#">SV Seedbank</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="nav">
      <ul class="navbar-nav ms-auto">{nav_links}</ul>
    </div>
  </div>
</nav>
<div class="container pb-5">
  <div class="text-center py-4">
    <h1 class="display-5 fw-bold" style="color:#2d6a4f;">SV Seedbank Management System</h1>
    <p class="lead text-muted">A database-backed web application for managing seed collections, members, events, and partners.</p>
    <hr>
  </div>
  {page_sections}
  <section id="analytics" class="mb-5">
    <h2>Data Analytics</h2>
    <p class="text-muted">All 10 queries run against both MySQL and MongoDB.</p>
    {analytics_cards}
  </section>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
document.querySelectorAll('[data-bs-toggle="tab"]').forEach(function(btn) {{
  btn.addEventListener('shown.bs.tab', function(e) {{
    var target = e.target.getAttribute('data-bs-target');
    var num = target.replace(/\\D/g, '');
    var isMongo = target.startsWith('#mongo');
    document.getElementById('sqltext' + num).style.display = isMongo ? 'none' : 'block';
    document.getElementById('mongotext' + num).style.display = isMongo ? 'block' : 'none';
  }});
}});
</script>
</body>
</html>"""

# ── Write output ───────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done! Static site written to: {os.path.abspath(out_path)}")
print("Next steps:")
print("  1. git add docs/index.html && git commit -m 'add static site'")
print("  2. git push")
print("  3. In GitHub repo settings → Pages → set source to /docs")
