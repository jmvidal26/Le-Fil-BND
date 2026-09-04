import os
import ollama
import subprocess
import time
import spacy
import json
import sys
import os
venv_path = os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages')
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.append(venv_path)

try:
    from google import genai
except ImportError:
    import google.genai as genai
from dotenv import load_dotenv    
import socket






#============================================================#
#------------------------VERSION-0.00.0-----by JesVid.DEV----#
#============================================================#
#-------------------------PROtOTYPE_UI-----------------------#
#============================================================#
#============================================================#


#============================================================#
#-------------------------VARIABLES--------------------------#
#============================================================#

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# tha's load the spanish language

nlp=spacy.load("es_core_news_sm")
load_dotenv()

#============================================================#
#---------------------CONnECTION-FEATURE---------------------#
#============================================================#

def connect(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except socket.error:
        return False







#============================================================#
#----------------------AI_CHAT-FEATURE-----------------------#
#============================================================#

def agent_AI (message):
    global AI_score, instruction
    base = "Eres un asistente técnico experto."
    feedback_alert = " El usuario no está satisfecho, sé más breve." if AI_score < 105 else ""
    
    prompt_final = f"{base} {feedback_alert}\nREGLAS ADICIONALES:\n{instruction}\nUsuario: {message}"
    # that's convert the message in MINS and process the msj, but 
    doc= nlp(message.lower())

    #that process the message

    lemas= [token.lemma_ for token in doc]
    messages_for_ollama = [{'role': 'system', 'content': prompt_final}]


    try:
        #practice hashmaps
        respond=ollama.chat(model='gemma2:2b', messages=messages_for_ollama)
        respondA=respond['message']['content']

        return respondA
    
    except Exception as e:
        return f"fail with ollama model {str(e)}"

def agent_WIFI (message):
    global AI_score, instruction
    api_key = os.getenv("GEMINI_API_KEY")
    client=genai.Client(api_key=api_key)

    base = "Eres un asistente técnico experto."
    feedback_alert = " El usuario no está satisfecho, sé más breve." if AI_score < 105 else ""
    
    prompt_final = f"{base} {feedback_alert}\nREGLAS ADICIONALES:\n{instruction}\nUsuario: {message}"
    
    try:
        respond = client.models.generate_content(model="gemini-3-flash-preview",config={'system_instruction': prompt_final},contents=message)

        respond_text = respond.text

        return respond_text
    
    except Exception as e:
        return f"fail with gemini model {str(e)}"








#============================================================#
#----------------------MEMORY-FEATURE------------------------#
#============================================================#    
    
def memory_agent(user,respondAI):
    date = time.strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open("memory_agent.txt", "a", encoding="utf-8") as BaseD:
            BaseD.write(f'\n<{date}>  <USER>  {user}  <AI>  {respondAI}  <Score>  {AI_score}')
    except Exception as e:
        print(f"THERE IS/ARE A FAIL/S {e}")












#============================================================#
#----------------------RUN\TESTING_MODULE--------------------#
#============================================================#

if __name__ == "__main__":

    user = ""
    respondAI = "No request processed."
    if os.path.exists("ask.txt"):
        with open("ask.txt","r",encoding="utf-8") as f:
            user=f.read()
        wifi=connect()
        try:
            if not wifi:
                respondAI=agent_AI(user)
            elif wifi:
                respondAI=agent_WIFI(user)
            with open("response.txt","w",encoding="utf-8") as f:
                f.write(f"{respondAI}")
            with open("finished.txt","w",encoding="utf-8") as f:
                f.write(f"")
            memory_agent(user,respondAI)
            os.remove("ask.txt")
        except Exception as e:
            print(f"THERE IS/ARE A FAIL/S {e}")