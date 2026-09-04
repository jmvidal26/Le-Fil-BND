import os
import psutil

    
#============================================================#
#-----------------------ACTIONS-FEATURE----------------------#
#============================================================#

def agent_actions():
    if os.path.exists("distractions.txt"):
        with open("distractions.txt","r",encoding="utf-8") as f:
            while True:
                process=f.read()          
                if EOFError:
                    break
                os.system(f"taskkill /F /IM {process}")