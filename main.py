import sqlite3
from fastapi_offline import FastAPIOffline

app = FastAPIOffline()

def load_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, score FROM students")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({"name": row[0], "score": row[1]})
    return result

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
