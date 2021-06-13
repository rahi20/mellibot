import json
import pandas as pd

datafile = open('data/intents.json')

intents = json.load(datafile)

dc = {
    "text" : [],
    "intent" : [],
    "responses" : []
}
for ele in intents['intents']:
    for pattern in ele['patterns']:
        dc["text"].append(pattern)
        dc["intent"].append(ele["tag"])
        dc["responses"].append(ele["responses"])

fulldata = pd.DataFrame.from_dict(dc)

fulldata.to_csv("data/intents.csv", index=False)