import json
import pandas as pd
import os
from collections import defaultdict
from nrclex import NRCLex

import nltk
nltk.download('punkt')

if not os.path.exists("data/EmoLex.csv"):
    data = {"word":[], "emotion":[], "association":[]}

    f = open("data/NRC-Emotion-Lexicon.txt", "r")
    for line in f.readlines():
        cols = line.split()
        if len(cols) == 3 and cols[1] != "negative" and cols[1] != "positive":
            data["word"].append(cols[0])
            data["emotion"].append(cols[1])
            data["association"].append(cols[2])

    emolex = pd.DataFrame(data, columns=["word", "emotion", "association"])
    emolex.to_csv("data/EmoLex.csv", index=False)
    f.close()

emolex = pd.read_csv("data/EmoLex.csv")
f = open("data/Poems.json", "r")
poems = json.load(f)
print("Number of poems:", len(poems))

emotion_list = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
poem_emotions = defaultdict(list)
missing = 0

for i, poem in enumerate(poems):
    score = defaultdict(int)
    id = poem["id"]
    content = poem["poem"]

    emotion = NRCLex(content).affect_frequencies
    emotion.pop("positive")
    emotion.pop("negative")

    if len(emotion) == 0:
        missing += 1
    else:
        max_val = max(emotion.values())
        if max_val == 0:
            missing += 1
        for item in emotion.items():
            if item[1] >= max_val:
                poem_emotions[item[0]].append(poem)

    if i % 1000 == 0:
        print(i)

print("Number of Missing Poems:", missing)
f.close()

tot = 0
for i in emotion_list:
    print("Number of poems belonging to {} = {}".format(i, len(poem_emotions[i])))
    tot += len(poem_emotions[i])
    with open("data/"+i+".json", "w") as outfile:
        json.dump(poem_emotions[i], outfile)

print("Total number of poems in all categories: ", tot)