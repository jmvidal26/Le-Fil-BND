import os
import psutil
import ollama

#============================================================#
#--------------------MONITORING-FEATURE----------------------#
#============================================================#

def detect():
    try:
        processes = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name']]
        os.makedirs("config", exist_ok=True)
        with open("config/distractions.txt", 'w', encoding="utf-8") as f:
            f.write("\n".join(processes))
            
        return True
    except Exception as e:
        return f"ERROR {e}"


def msg():
    if not os.path.exists("config/distractions.txt"):
        return ""

    with open("config/distractions.txt", "r", encoding="utf-8") as f:
        processes = [line.strip() for line in f if line.strip()]

    process_list_str = ", ".join(processes)
    
    message = (
        "Analiza la siguiente lista de procesos del sistema. "
        "Devuelve ÚNICAMENTE los nombres de los procesos (separados por línea) "
        "que sean aplicaciones de entretenimiento, juegos, redes sociales o distracciones. "
        "ELIMINA DE LA LISTA todo lo que sea del sistema operativo, drivers o herramientas de desarrollo:\n\n"
        f"{process_list_str}"
    )
    
    return message


def distrc(message):
    base = "Eres un asistente técnico experto."
    instruction = "Sé directo y preciso, responde solo con la lista filtrada, no uses emojis ni texto extra."
    
    prompt_final = f"{base}\nRules:\n{instruction}\n"
    
    ollama_mssg  = [{'role': 'system', 'content': prompt_final}]

    try:

        model = ollama.chat(model= 'https://huggingface.co/Nguuma/security-slm-unsloth-1.5b', messages= ollama_mssg)

        response=model['message']['content']


        return response
    
    except Exception as e:
        print(f"FAIL WITH GEMMA MODEL: {e}")

def arch(respond_text):
    os.makedirs("config", exist_ok=True)
    with open("config/distractions.txt", "w", encoding="utf-8") as f:
        f.write(respond_text)


if __name__ == "__main__":
    print("1. Escaneando procesos...")
    detect()
    
    print("2. Armando prompt...")
    ms = msg()
    
    print("3. Consultando a la IA para filtrar distracciones...")
    r = distrc(ms)
    
    print("4. Guardando lista filtrada...")
    arch(r)
    print("¡Proceso completado!")

