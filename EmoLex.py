'''
Program to split poems among each of the eight emotion categories
'''

import json
import pandas as pd
import os
from collections import defaultdict
from nrclex import NRCLex

import nltk
# nltk.download('punkt')

'''
nrclex python library is used instead of EmoLex dataset due to its speed bonus and simplicity
nrclex also uses the same dataset that we are creating
'''

# Creating EmoLex dataset if it does not already exist in project
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

# We have not used this emolex dataframe. We have used the nrclex library instead.
emolex = pd.read_csv("data/EmoLex.csv")
f = open("data/custom_poems.json", "r")
poems = json.load(f)
print("Number of poems:", len(poems))

emotion_list = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
poem_emotions = defaultdict(list)
missing = 0
missing_poems = []

for i, poem in enumerate(poems):
    score = defaultdict(int)
    id = poem["id"]
    content = poem["poem"]

    # Creating a dictionary with frequencies of each of the emotions associated with a poem
    emotion = NRCLex(content).affect_frequencies

    # Removing degree of positivity and negativity from the dictionary as we are only concerned with emotions
    emotion.pop("positive")
    emotion.pop("negative")

    if len(emotion) == 0:
        # Missing indicates a poem that does not pertain to any particular emotion
        # Models for all emotion categories use these poems for training
        missing += 1
        missing_poems.append(poem)
    else:
        max_val = max(emotion.values())
        if list(emotion.values()).count(max_val) > 6:
            missing += 1
            missing_poems.append(poem)
        elif list(emotion.values()).count(max_val) > 1:
            pass
        else:
            poem_emotions[max(emotion, key=emotion.get)].append(poem)
        # if max_val == 0:
        #     missing += 1
        # for item in emotion.items():
        #     if item[1] >= max_val:
        #         poem_emotions[item[0]].append(poem)

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

with open("data/missing.json", "w") as outfile:
    json.dump(missing_poems, outfile)

print("Total number of poems in all categories: ", tot)

