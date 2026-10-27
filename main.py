from fastapi_offline import FastAPIOffline

app = FastAPIOffline()

def load_students():
    rows = []
    with open("data.csv") as f:
        lines = f.readlines()
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        name, score = line.split(",")
        rows.append({"name": name, "score": float(score)})
    return rows

@app.get("/")
def read_root():
    return {"message": "hello from ali cloud"}

@app.get("/students")
def get_students():
    return load_students()

@app.get("/stats")
def get_stats():
    students = load_students()
    total = 0
    best = students[0]
    for s in students:
        total = total + s["score"]
        if s["score"] > best["score"]:
            best = s
    return {"average": total / len(students), "count": len(students), "best": best}
