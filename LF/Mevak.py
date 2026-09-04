import os
import psutil
import time
import asyncio
import random
import json
import spacy

#============================================================#
#-----------------------TALKING-FEATURE----------------------#
#============================================================#

async def Mevak():
    nlp=spacy.load("es_core_news_sm")
    if os.path.exists("ears.txt"):
        

#CHOOSE THE TOPIC OF THE CONVERSATION           
        choose=random.randint(0,2)
        if choose==0 and os.path.exists("chat_history.json"):
            user="Habale al usuario del ultimo tema"
        elif choose==0 and not os.path.exists("chat_history.json"):
            user="El usuario esta muy callado y si le hablas?"
        elif choose==1:
            if os.path.exists("multimodalA.json"):
                with open("multimodalA.json", "r",encoding="utf-8") as f:
                    modalaprove= json.load(f)
                    topic=random.choice(modalaprove)
            else:
                topic="mejora de el horario para una mejor vida cotidiana"
            user=f"Habla con el usuario sobre {topic}"
        elif choose==2:
            if os.path.exists("news.json"):
                with open("news.json", "r",encoding="utf-8") as f:
                    news= json.load(f)
            else:
                news="google"
            user=f"Habla sobre este tema: {news}"

            doc=nlp(user.lower())
            lemas= [token.lemma_ for token in doc]
            with open("ask.txt", "w", encoding="utf-8") as f:
                    f.write(" ".join(lemas))


if __name__=="__main__":
    clock=None
    sclock=None

    while not os.path.exists("ears.txt"):
        agent_actions()

    
    if os.path.exists("ears.txt"):
        if os.path.exists("eyes.txt"):
            os.remove("eyes.txt")
        asyncio.run(Mevak())
        if os.path.exists("ask.txt"):
            os.remove("ears.txt")