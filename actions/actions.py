import spacy
import pandas as pd
import os
import re

nlp = spacy.load("en_core_web_md")
endocrinos = pd.read_csv(os.path.join('data', 'endocrinos.csv')).fillna("Not found")
endoc_cities = endocrinos['city']

def find_word(msg, s1=endoc_cities):
    
    doc = nlp(msg)
    found_loc_flag = False
    city = ""
    for ent in doc.ents : 
        if ent.label_ == "GPE" : 
            city = ent.text
            found_loc_flag = True
    
    if not found_loc_flag:
        patterns = ["in\s*\w*", "in\s*the\s*city\sof\s*\w*", "in\s*the\scity\sof\s*\w*"]
        matched = []
        
        for pattern in patterns : 
            match_obj = re.findall(pattern, msg)
            if len(match_obj) != 0 :
                for word in match_obj : 
                    matched.append(word.split()[-1])
    else :
        matched = [city]
    if len(matched) != 0: 
        for i, word in enumerate(matched):
            if s1.str.contains(word, case=False).sum() >= 1 :
                found_loc_flag = True 
                indices = s1.str.contains(word, case=False)
                break
    """
    flag = False
    tokens = msg.split()
    indices = []
    for i, word in enumerate(tokens):
        if s1.str.contains(word, case=False).sum() >= 1 :
            flag = True 
            indices = s1.str.contains(word, case=False)
            break
   """    
    return found_loc_flag, word, s1[indices].index.values

def fetchendocrino(msg):
    flag, city, indices = find_word(msg)
    resp = "Nothing matched"
    if flag :
        matched = endocrinos.iloc[indices]
        resp = "Endocrinologists found : \n"
        for index, row in matched.iterrows():
            resp += """
            name : {0},
            sector : {1},
            Email : {2},
            Tel : {3},
            Address : {4},
            City : {5} 
            \n""".format(row['name'], row['sector'], row['email'], row['tel'], row["address"], city)
        
    return resp