import os
import ollama
import sys
import os

venv_path = os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages')
if venv_path not in sys.path:
    sys.path.append(venv_path)

try:
    from google import genai
except ImportError:
    import google.genai as genai

from dotenv import load_dotenv    
import socket

#=============================================#
#------------EXTRAS_EXTRAS_EXTRAS-(O_O)-------#
#=============================================#










#=============================================#
#---------------SOCKET-CONNECTION-(-_-)-------#
#=============================================#

def connect(host="8.8.8.8", port=53, timeout=3):

    try:
        socket.setdefaulttimeout(timeout)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))

        return True
    
    except socket.error:
        return False
    










#=============================================#
#------------------LOCAL-AGENT-(-u-)----------#
#=============================================#

def local_agent (message):

    base         =   "Eres un agente de ia especializado en asistencia tecnica"
    history      =   ""
    final_prompt =  f"REGLAS: \n{base}\n HISTORIAL: \n{history}\n USUARIO: \n{message}"

    ollama_mssg  = [{'role': 'system', 'content': final_prompt}]

    try:

        model = ollama.chat(model= 'https://huggingface.co/Nguuma/security-slm-unsloth-1.5b', messages= ollama_mssg)

        response=model['message']['content']


        return response
    
    except Exception as e:
        print(f"FAIL WITH MODEL: {e}")










#=============================================#
#-----------------WIFI-AGENT-(^u^)------------#
#=============================================#

def wifi_agent (message):

#INITIALIZE

    api_key      = os.getenv("GEMINI_API_KEY")
    client       = genai.Client(api_key=api_key)

    base         =  "Eres un agente de ia especializado en asistencia tecnica"
    history      =  ""
    final_prompt = f"REGLAS: \n{base}\n HISTORIAL: \n{history}\n USUARIO: \n{message}"

    try:

        model_GM = client.models.generate_content(
        model    = 'gemini-3.1-flash-live-preview',
        config   = {'system_instruction'  : final_prompt},
        contents = message)

        response = model_GM.text

        return response
    
    except Exception as e:
        print(f"FAIL WITH GEMINI MODEL: {e}")











#=============================================#
#------------RUNNING AND DEBUGGING-(^n^)------#
#=============================================#

if __name__ == '__main__':

    user=""
    response= "NO REQUEST PROCESSED"

    if os.path.exists("ask.txt"):

        with open("ask.txt", 'r', encoding='utf-8') as f:
            user=f.read()
            
        wifi=connect()

        try:

            if not wifi: 
                response=local_agent(user)
            elif wifi:   
                response=wifi_agent(user)

            with open("response.txt","w",encoding="utf-8") as f:
                f.write(f"{response}")

            with open("finished.txt","w",encoding="utf-8") as f:
                f.write(f"")

            os.remove("ask.txt")

        except Exception as e:
            print(f"THERE IS/ARE A FAIL/S {e}")

    else:
        pass