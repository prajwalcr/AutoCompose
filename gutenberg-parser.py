import ndjson
import json

f = open("data/gutenberg-poetry-v001.ndjson", "r")

data = ndjson.load(f)
content = ""
for i, line in enumerate(data):
    content += line["s"] + "\n"
    if i%100000 == 0 and i != 0:
        print(f"{i} of {len(data)}")
poems = content.split(".\n")
lengths = []
waste = 0
print("Number of poems before filtering:", len(poems))
poems = list(map(lambda x: x+".", filter(lambda x: len(x.split("\n")) > 2, poems)))
print("Number of poems after filtering:", len(poems))
f.close()

res = []
for id, poem in enumerate(poems):
    res.append({"poem": poem, "id": id})

with open("data/custom_poems.json", "w") as outfile:
    json.dump(res, outfile)