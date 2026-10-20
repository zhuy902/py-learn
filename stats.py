total = 0
count = 0
best_name = ""
best_score = 0

with open("data.csv") as f:
    lines = f.readlines()

for line in lines[1:]:
    line = line.strip()
    if not line:
        continue
    name, score_text = line.split(",")
    score = float(score_text)
    total = total + score
    count = count + 1
    if score > best_score:
        best_score = score
        best_name = name

print("average:", total / count)
print("best:", best_name, best_score)
