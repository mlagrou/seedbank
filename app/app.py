import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://matt:lagrou@lagrou355.qp9qtge.mongodb.net/noteapp?retryWrites=true&w=majority"
)

_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = _client["SV_Seedbank"]


def to_list(cursor):
    rows = list(cursor)
    for r in rows:
        r["_id"] = str(r["_id"])
    return rows


# ── Home ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ══ SPECIES ════════════════════════════════════════════
@app.route("/species", methods=["GET", "POST"])
def species():
    if request.method == "POST":
        d = request.get_json()
        db["Species"].insert_one({
            "common_name": d["common_name"],
            "scientific_name": d["scientific_name"],
            "requirements": {
                "sun": d.get("sun", ""),
                "soil": d.get("soil", ""),
                "water": d.get("water", "")
            },
            "description": d.get("description", ""),
            "drought_tolerant": d.get("drought_tolerant") == "true"
        })
        return jsonify({"ok": True})
    rows = to_list(db["Species"].find().sort("common_name", 1))
    return render_template("species.html", species=rows)


@app.route("/species/<sid>", methods=["PUT", "DELETE"])
def species_item(sid):
    if request.method == "DELETE":
        db["Species"].delete_one({"_id": ObjectId(sid)})
        return jsonify({"ok": True})
    d = request.get_json()
    db["Species"].update_one({"_id": ObjectId(sid)}, {"$set": {
        "common_name": d["common_name"],
        "scientific_name": d["scientific_name"],
        "requirements": {
            "sun": d.get("sun", ""),
            "soil": d.get("soil", ""),
            "water": d.get("water", "")
        },
        "description": d.get("description", ""),
        "drought_tolerant": d.get("drought_tolerant") == "true"
    }})
    return jsonify({"ok": True})


# ══ MEMBERS ════════════════════════════════════════════
@app.route("/members", methods=["GET", "POST"])
def members():
    if request.method == "POST":
        d = request.get_json()
        db["Member"].insert_one({
            "f_name": d["f_name"],
            "l_name": d["l_name"],
            "email": d["email"],
            "join_date": d.get("join_date", ""),
            "status": d.get("status", "active")
        })
        return jsonify({"ok": True})
    rows = to_list(db["Member"].find().sort("l_name", 1))
    return render_template("members.html", rows=rows)


@app.route("/members/<mid>", methods=["PUT", "DELETE"])
def members_item(mid):
    if request.method == "DELETE":
        db["Member"].delete_one({"_id": ObjectId(mid)})
        return jsonify({"ok": True})
    d = request.get_json()
    db["Member"].update_one({"_id": ObjectId(mid)}, {"$set": {
        "f_name": d["f_name"],
        "l_name": d["l_name"],
        "email": d["email"],
        "join_date": d.get("join_date", ""),
        "status": d.get("status", "active")
    }})
    return jsonify({"ok": True})


# ══ BATCH ══════════════════════════════════════════════
@app.route("/batch", methods=["GET", "POST"])
def batch():
    if request.method == "POST":
        d = request.get_json()
        db["Batch"].insert_one({
            "species": d["species"],
            "collection_loc": {"name": d.get("collection_loc", "")},
            "storage_loc": {"name": d.get("storage_loc", "")},
            "collected_by": d.get("collected_by", ""),
            "date": d.get("date", ""),
            "start_quantity": int(d.get("start_quantity", 0)),
            "current_quantity": int(d.get("current_quantity", 0))
        })
        return jsonify({"ok": True})
    rows = to_list(db["Batch"].find().sort("date", -1))
    return render_template("batch.html", rows=rows)


@app.route("/batch/<bid>", methods=["PUT", "DELETE"])
def batch_item(bid):
    if request.method == "DELETE":
        db["Batch"].delete_one({"_id": ObjectId(bid)})
        return jsonify({"ok": True})
    d = request.get_json()
    db["Batch"].update_one({"_id": ObjectId(bid)}, {"$set": {
        "species": d["species"],
        "collection_loc": {"name": d.get("collection_loc", "")},
        "storage_loc": {"name": d.get("storage_loc", "")},
        "collected_by": d.get("collected_by", ""),
        "date": d.get("date", ""),
        "start_quantity": int(d.get("start_quantity", 0)),
        "current_quantity": int(d.get("current_quantity", 0))
    }})
    return jsonify({"ok": True})


# ══ DISTRIBUTIONS ══════════════════════════════════════
@app.route("/distributions", methods=["GET", "POST"])
def distributions():
    if request.method == "POST":
        d = request.get_json()
        batch_id = d.get("batch_id", "")
        quantity = int(d.get("quantity", 0))
        if batch_id:
            db["Batch"].update_one(
                {"_id": ObjectId(batch_id)},
                {"$inc": {"current_quantity": -quantity}}
            )
        db["Distribution"].insert_one({
            "batch_id": batch_id,
            "species": d["species"],
            "member": d["member"],
            "quantity": quantity,
            "date": d.get("date", "")
        })
        return jsonify({"ok": True})
    rows = to_list(db["Distribution"].find().sort("date", -1))
    batches = to_list(db["Batch"].find({"current_quantity": {"$gt": 0}}).sort("species", 1))
    return render_template("distributions.html", rows=rows, batches=batches)


@app.route("/distributions/<did>", methods=["PUT", "DELETE"])
def distributions_item(did):
    if request.method == "DELETE":
        dist = db["Distribution"].find_one({"_id": ObjectId(did)})
        if dist and dist.get("batch_id"):
            try:
                db["Batch"].update_one(
                    {"_id": ObjectId(dist["batch_id"])},
                    {"$inc": {"current_quantity": dist.get("quantity", 0)}}
                )
            except Exception:
                pass
        db["Distribution"].delete_one({"_id": ObjectId(did)})
        return jsonify({"ok": True})
    d = request.get_json()
    dist = db["Distribution"].find_one({"_id": ObjectId(did)})
    old_qty = dist.get("quantity", 0) if dist else 0
    new_qty = int(d.get("quantity", 0))
    batch_id = d.get("batch_id") or (dist.get("batch_id") if dist else "")
    if batch_id:
        try:
            db["Batch"].update_one(
                {"_id": ObjectId(batch_id)},
                {"$inc": {"current_quantity": old_qty - new_qty}}
            )
        except Exception:
            pass
    db["Distribution"].update_one({"_id": ObjectId(did)}, {"$set": {
        "batch_id": batch_id,
        "species": d["species"],
        "member": d["member"],
        "quantity": new_qty,
        "date": d.get("date", "")
    }})
    return jsonify({"ok": True})


# ══ ACTIVITIES ═════════════════════════════════════════
@app.route("/activities", methods=["GET", "POST"])
def activities():
    if request.method == "POST":
        d = request.get_json()
        db["Activities"].insert_one({
            "member": d["member"],
            "location": d.get("location", ""),
            "hours": float(d.get("hours", 0)),
            "date": d.get("date", ""),
            "description": d.get("description", "")
        })
        return jsonify({"ok": True})
    rows = to_list(db["Activities"].find().sort("date", -1))
    return render_template("activities.html", rows=rows)


@app.route("/activities/<aid>", methods=["PUT", "DELETE"])
def activities_item(aid):
    if request.method == "DELETE":
        db["Activities"].delete_one({"_id": ObjectId(aid)})
        return jsonify({"ok": True})
    d = request.get_json()
    db["Activities"].update_one({"_id": ObjectId(aid)}, {"$set": {
        "member": d["member"],
        "location": d.get("location", ""),
        "hours": float(d.get("hours", 0)),
        "date": d.get("date", ""),
        "description": d.get("description", "")
    }})
    return jsonify({"ok": True})


# ══ EVENTS ═════════════════════════════════════════════
@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        d = request.get_json()
        db["Events"].insert_one({
            "event_name": d["event_name"],
            "event_date": d.get("event_date", ""),
            "event_type": d.get("event_type", ""),
            "location": d.get("location", ""),
            "member_attendance": [],
            "guest_attendance": []
        })
        return jsonify({"ok": True})
    rows = to_list(db["Events"].find().sort("event_date", -1))
    return render_template("events.html", rows=rows)


@app.route("/events/<eid>", methods=["PUT", "DELETE"])
def events_item(eid):
    if request.method == "DELETE":
        db["Events"].delete_one({"_id": ObjectId(eid)})
        return jsonify({"ok": True})
    d = request.get_json()
    db["Events"].update_one({"_id": ObjectId(eid)}, {"$set": {
        "event_name": d["event_name"],
        "event_date": d.get("event_date", ""),
        "event_type": d.get("event_type", ""),
        "location": d.get("location", "")
    }})
    return jsonify({"ok": True})


# ══ PARTNERS ═══════════════════════════════════════════
@app.route("/partners", methods=["GET", "POST"])
def partners():
    if request.method == "POST":
        d = request.get_json()
        db["Partners"].insert_one({
            "p_name": d["p_name"],
            "contact": d.get("contact", ""),
            "email": d.get("email", ""),
            "address": d.get("address", "")
        })
        return jsonify({"ok": True})
    rows = to_list(db["Partners"].find().sort("p_name", 1))
    return render_template("partners.html", rows=rows)


@app.route("/partners/<pid>", methods=["PUT", "DELETE"])
def partners_item(pid):
    if request.method == "DELETE":
        db["Partners"].delete_one({"_id": ObjectId(pid)})
        return jsonify({"ok": True})
    d = request.get_json()
    db["Partners"].update_one({"_id": ObjectId(pid)}, {"$set": {
        "p_name": d["p_name"],
        "contact": d.get("contact", ""),
        "email": d.get("email", ""),
        "address": d.get("address", "")
    }})
    return jsonify({"ok": True})


# ══ INVENTORY (read-only aggregate) ═══════════════════
@app.route("/inventory")
def inventory():
    rows = list(db["Batch"].aggregate([
        {"$group": {"_id": "$species", "quantity": {"$sum": "$current_quantity"}}},
        {"$sort": {"_id": 1}}
    ]))
    return render_template("inventory.html", rows=rows)


# ══ GUESTS (read-only from Events) ════════════════════
@app.route("/guests")
def guests():
    rows = list(db["Events"].aggregate([
        {"$unwind": "$guest_attendance"},
        {"$project": {
            "_id": 0,
            "event_name": 1,
            "name": "$guest_attendance.name",
            "email": "$guest_attendance.email"
        }},
        {"$sort": {"event_name": 1, "name": 1}}
    ]))
    return render_template("guests.html", rows=rows)


# ══ ANALYTICS ══════════════════════════════════════════
@app.route("/analytics")
def analytics():
    def mq(fn):
        try:
            rows = list(fn())
            for r in rows:
                if "_id" in r:
                    r["id"] = r.pop("_id")
            return rows
        except Exception as e:
            return [{"error": str(e)}]

    queries = [
        {
            "number": 1,
            "question": "What species require Full Sun and Low water?",
            "sql_text": "SELECT s.common_name, sun.requirement AS sun_req, water.requirement AS water_req\nFROM Species s, Sun_Requirement sun, Water_Requirement water\nWHERE s.sun_req = sun.req_id\n  AND s.water_req = water.req_id\n  AND sun.requirement = 'Full Sun'\n  AND water.requirement = 'Low'",
            "mongo_text": 'db["Species"].find({"requirements.sun": "Full Sun", "requirements.water": "Low"})',
            "result": mq(lambda: db["Species"].find(
                {"requirements.sun": "Full Sun", "requirements.water": "Low"},
                {"_id": 0, "common_name": 1, "requirements": 1}
            )),
        },
        {
            "number": 2,
            "question": "What species have never had seeds collected?",
            "sql_text": "SELECT common_name\nFROM Species\nWHERE species_id NOT IN (SELECT species_id FROM Batch)",
            "mongo_text": 'db["Species"].aggregate([\n  {$lookup:{from:"Batch",localField:"common_name",foreignField:"species",as:"batches"}},\n  {$match:{batches:{$size:0}}},\n  {$project:{_id:0,common_name:1}}\n])',
            "result": mq(lambda: db["Species"].aggregate([
                {"$lookup": {"from": "Batch", "localField": "common_name", "foreignField": "species", "as": "batches"}},
                {"$match": {"batches": {"$size": 0}}},
                {"$project": {"_id": 0, "common_name": 1}}
            ])),
        },
        {
            "number": 3,
            "question": "What is the current seed inventory, sorted alphabetically by common name?",
            "sql_text": "SELECT common_name, SUM(current_quantity) AS Quantity\nFROM Batch b, Species s\nWHERE b.species_id = s.species_id\nGROUP BY common_name\nORDER BY common_name",
            "mongo_text": 'db["Batch"].aggregate([\n  {$group:{_id:"$species",totalInventory:{$sum:"$current_quantity"}}},\n  {$sort:{_id:1}}\n])',
            "result": mq(lambda: db["Batch"].aggregate([
                {"$group": {"_id": "$species", "totalInventory": {"$sum": "$current_quantity"}}},
                {"$sort": {"_id": 1}}
            ])),
        },
        {
            "number": 4,
            "question": "How many batches and total seeds have been collected from each location?",
            "sql_text": "SELECT loc_name AS Location, COUNT(batch_id) AS Batches, SUM(start_quantity) AS 'Total Seeds'\nFROM Location l, Batch b\nWHERE l.location_id = b.collection_loc\nGROUP BY loc_name",
            "mongo_text": 'db["Batch"].aggregate([\n  {$group:{_id:"$collection_loc.name",batches:{$sum:1},totalSeeds:{$sum:"$start_quantity"}}},\n  {$sort:{totalSeeds:-1}}\n])',
            "result": mq(lambda: db["Batch"].aggregate([
                {"$group": {
                    "_id": "$collection_loc.name",
                    "batches": {"$sum": 1},
                    "totalSeeds": {"$sum": "$start_quantity"}
                }},
                {"$sort": {"totalSeeds": -1}}
            ])),
        },
        {
            "number": 5,
            "question": "What are the total volunteer hours logged per member?",
            "sql_text": "SELECT l_name, f_name, COUNT(batch_id) AS Count\nFROM Member, Batch\nWHERE collected_by = member_id\nGROUP BY l_name, f_name\nHAVING COUNT(batch_id) > (SELECT AVG(bc) FROM (SELECT COUNT(batch_id) AS bc FROM Batch GROUP BY collected_by) AS sub)",
            "mongo_text": 'db["Activities"].aggregate([\n  {$group:{_id:"$member",totalHours:{$sum:"$hours"}}},\n  {$sort:{totalHours:-1}}\n])',
            "result": mq(lambda: db["Activities"].aggregate([
                {"$group": {"_id": "$member", "totalHours": {"$sum": "$hours"}}},
                {"$sort": {"totalHours": -1}}
            ])),
        },
        {
            "number": 6,
            "question": "How many seed distributions has each member received?",
            "sql_text": "SELECT f_name, l_name, SUM(hours) AS Hours\nFROM Member m, Activity_log a\nWHERE m.member_id = a.member_id AND m.status = 'active'\nGROUP BY f_name, l_name",
            "mongo_text": 'db["Distribution"].aggregate([\n  {$group:{_id:"$member",distributions:{$sum:1},totalSeeds:{$sum:"$quantity"}}},\n  {$sort:{totalSeeds:-1}}\n])',
            "result": mq(lambda: db["Distribution"].aggregate([
                {"$group": {"_id": "$member", "distributions": {"$sum": 1}, "totalSeeds": {"$sum": "$quantity"}}},
                {"$sort": {"totalSeeds": -1}}
            ])),
        },
        {
            "number": 7,
            "question": "Who has received which species of seeds, and how many?",
            "sql_text": "SELECT f_name, l_name, common_name AS Species, SUM(quantity) AS 'Seeds Dispersed'\nFROM Member m, Species s, Distribution d, Batch b\nWHERE m.member_id = d.member_id AND s.species_id = b.species_id AND d.batch_id = b.batch_id\nGROUP BY f_name, l_name, common_name",
            "mongo_text": 'db["Distribution"].aggregate([\n  {$group:{_id:{member:"$member",species:"$species"},seedDispersed:{$sum:"$quantity"}}},\n  {$sort:{"_id.member":1}}\n])',
            "result": mq(lambda: db["Distribution"].aggregate([
                {"$group": {"_id": {"member": "$member", "species": "$species"}, "seedDispersed": {"$sum": "$quantity"}}},
                {"$sort": {"_id.member": 1}}
            ])),
        },
        {
            "number": 8,
            "question": "List all partner organizations with their contact information.",
            "sql_text": "SELECT p_name AS Partner, loc_name AS Location, loc_type AS Type\nFROM Partner p, Location l\nWHERE p.partner_id = l.partner_id",
            "mongo_text": 'db["Partners"].find({}, {_id:0, p_name:1, contact:1, address:1})',
            "result": mq(lambda: db["Partners"].find(
                {},
                {"_id": 0, "p_name": 1, "contact": 1, "address": 1}
            )),
        },
        {
            "number": 9,
            "question": "What are the 3 most popular events by attendance?",
            "sql_text": "SELECT event_name, COUNT(DISTINCT m.member_id) + COUNT(DISTINCT g.guest_email) AS 'Total Attendees'\nFROM Event e\nLEFT JOIN Event_member m ON e.event_id = m.event_id\nLEFT JOIN Event_guest g ON e.event_id = g.event_id\nGROUP BY event_name ORDER BY 2 DESC LIMIT 3",
            "mongo_text": 'db["Events"].aggregate([\n  {$project:{event_name:1,attendance:{$add:[{$size:"$guest_attendance"},{$size:"$member_attendance"}]}}},\n  {$sort:{attendance:-1}},{$limit:3}\n])',
            "result": mq(lambda: db["Events"].aggregate([
                {"$project": {
                    "event_name": 1,
                    "attendance": {"$add": [
                        {"$size": "$guest_attendance"},
                        {"$size": "$member_attendance"}
                    ]}
                }},
                {"$sort": {"attendance": -1}},
                {"$limit": 3}
            ])),
        },
        {
            "number": 10,
            "question": "Return a list of every guest and their email who has attended at least 1 event.",
            "sql_text": "SELECT DISTINCT guest_name AS Name, guest_email AS Email\nFROM Event_guest",
            "mongo_text": 'db["Events"].aggregate([\n  {$unwind:"$guest_attendance"},\n  {$project:{_id:0,name:"$guest_attendance.name",email:"$guest_attendance.email"}}\n])',
            "result": mq(lambda: db["Events"].aggregate([
                {"$unwind": "$guest_attendance"},
                {"$project": {"_id": 0, "name": "$guest_attendance.name", "email": "$guest_attendance.email"}}
            ])),
        },
    ]

    return render_template("analytics.html", queries=queries)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "false") == "true")
