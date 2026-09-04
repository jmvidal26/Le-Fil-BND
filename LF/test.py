import os
import ollama
import subprocess
import time
import spacy
import json
import sys
import os



def agent_AI (message):
    base = "Eres un asistente técnico experto."
   
    prompt_final = f"{base} \nUsuario: {message}"
    # that's convert the message in MINS and process the msj, but 
    messages_for_ollama = [{'role': 'system', 'content': prompt_final}]


    try:
        #practice hashmaps
        respond=ollama.chat(model='https://huggingface.co/Nguuma/security-slm-unsloth-1.5b', messages=messages_for_ollama)
        respondA=respond['message']['content']

        return respondA
    
    except Exception as e:
        return f"fail with ollama model {str(e)}"

l=input("hh  ")
a=agent_AI(l)
print(a)