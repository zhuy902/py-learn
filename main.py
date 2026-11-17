import os
from openai import OpenAI
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

@app.post("/students")
def add_student(name: str, score: float):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()
    return {"ok": True}

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

@app.post("/ask")
def ask(question: str):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个简洁的助手，回答控制在三句话以内。"},
            {"role": "user", "content": question},
        ],
    )
    answer = resp.choices[0].message.content
    return {"answer": answer}
