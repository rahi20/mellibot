from keras.models import load_model
from tkinter import *
from tkinter import font
from tkinter import ttk
import random
import pickle
import time
import preprocess as pr
import numpy as np
import json
import os
import actions.actions as ac

model = load_model(os.path.join('saved_models_vars', 'bot_hypermodel.h5'))
classes = pickle.load(open(os.path.join('saved_models_vars','val_label_cor.pckl'), 'rb'))
data_file = open(os.path.join("data","intents.json"))
intents = json.loads(data_file.read())
rules = json.loads(open(os.path.join('data','rules.json')).read())

def predict_intent(msg, model):
    treshold = 0.25
    dd = np.array([pr.wordvec(msg)])
    pp = model.predict(dd)

    it = np.nditer(pp, flags=['c_index'])

    results = [[it.index,float(x)] for x in it if x>0.25]

    results = sorted(results, key=lambda x: x[1], reverse=True)

    return_intents = []
    for r in results:
        return_intents.append({"intent": classes.iloc[r[0]]['intent_label'], "probability": str(r[1])})

            #intent_label = classes.iloc[np.argmax(pp[0])]['intent_label']
    return return_intents

def getResponse(ints, intents_json, msg):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            #intents_file = open(os.path.join("data","intents.json"))
            #data = json.load(intents_file)
            method_name = rules.get(tag, None)
            if method_name is not None: 
                action_method = getattr(ac, method_name)
                result = action_method(msg)
            else :
                result = random.choice(i['responses'])
    return result

def chatbot_response(msg):
    ints = predict_intent(msg, model)
    res = getResponse(ints, intents, msg)
    return res


def send( msg):
    ChatLog.config(state = DISABLED)
    msg = msg
    EntryBox.delete(0, END)
        
    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You : " + msg + '\n\n')
        ChatLog.config(foreground="#010101", font=("Verdana", 12, font.BOLD))
            
        res = chatbot_response(msg)
        ChatLog.insert(END, "MelliBot : " + res + '\n\n')
            
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END) 

window = Tk()
window.title("Chat with MelliBot")
window.resizable(width = False, height = False)
window.configure(width = 470, height = 550, bg = "#e3e3e3")

ChatLog = Text(window,
            width = 20, 
            height = 2,
            bg = "#E3E3E3",
            fg = "#010101",
            font = "Verdana 13", 
            padx = 5,
            pady = 5)

ChatLog.config(state=DISABLED)
        
scrollbar = Scrollbar(window, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

labelBottom = Label(window,
                    bg = "#C4C7CC",
                                 height = 80)
          
labelBottom.place(relwidth = 1,
                rely = 0.825)
        
EntryBox = Entry(labelBottom,
                bg = "#E3E3E3",
                fg = "#010101",
                font="Verdana 13")
        
EntryBox.place(relwidth = 0.74,
                            relheight = 0.09,
                            rely = 0.008,
                            relx = 0.011)

SendButton = Button(
            labelBottom, 
            font=("Verdana",12,'bold'), 
            text="Send", 
            width=20, 
            bg="#43655A", 
            activebackground="#5D7D7C",
            fg='#E3E3E3',
            command = lambda : send(EntryBox.get()))
        #EntryBox = Text(window, bd=0, bg="white",width="29", height="5", font="Arial")

scrollbar.place(relheight = 1, relx = 0.974)
ChatLog.place(relheight = 0.825,
                            relwidth = 1, 
                            rely = 0.0)

SendButton.place(relx = 0.77,
                             rely = 0.014,
                             relheight = 0.075, 
                             relwidth = 0.22)

window.mainloop()
    
 