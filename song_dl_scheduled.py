from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import soundcard as sc
import soundfile as sf
from datetime import datetime
import threading
import schedule
import time
import os
import subprocess
import transcript  # Assure-toi que ce module est dans le même dossier ou installable

# Configuration globale
current_date = datetime.now().strftime("%d-%m-%Y")
SAMPLE_RATE = 48000  # [Hz]
DURATION = 8 * 60  # Durée d'enregistrement en secondes (8 minutes)
DELTA = 1  # Délai avant de cliquer sur lecture
BASE = "C:/Users/B/Documents/GitHub/citron-presse/"  # Répertoire de sortie

def record_audio():
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        data = mic.record(numframes=SAMPLE_RATE * DURATION)
        current_date = datetime.now().strftime("%d-%m-%Y")
        OUTPUT_FILE_NAME = f"{current_date}.wav"
        MP3_FILE_NAME = f"{current_date}.mp3"

        sf.write(file=BASE + OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

    # Convertir en MP3 avec ffmpeg
    subprocess.run(['ffmpeg', '-y', '-i', BASE + OUTPUT_FILE_NAME, BASE + MP3_FILE_NAME])

    # Générer et stocker le transcript
    topic = transcript.generate_daily_topic(OUTPUT_FILE_NAME, BASE=BASE)
    print("Daily Topic:", topic)
    transcript.store_daily_topic(topic, MP3_FILE_NAME, BASE=BASE)

    # Supprimer le fichier WAV après conversion
    os.remove(BASE + OUTPUT_FILE_NAME)

def run_script():
    try:
        print("Lancement du script à", datetime.now().strftime("%H:%M:%S"))
        # Lancer l'enregistrement audio dans un thread séparé
        audio_thread = threading.Thread(target=record_audio)
        audio_thread.start()

        # Lancer le navigateur
        driver = webdriver.Chrome()
        driver.get("https://www.rfj.ch/rfj/Accueil/RFJ-votre-radio-regionale.html")
        sleep(DELTA)
        driver.find_element(By.CSS_SELECTOR, ".manual-link > .fa-volume-up").click()
        sleep(DURATION)
        driver.close()

        # Attendre la fin de l'enregistrement audio
        audio_thread.join()
        print("Script terminé à", datetime.now().strftime("%H:%M:%S"))
    except Exception as e:
        print("Erreur pendant l'exécution du script:", e)

# Planification quotidienne à 11:48
schedule.every().day.at("11:48").do(run_script)

print("Scheduler démarré. Le script sera exécuté tous les jours à 11h48.")

# Boucle principale
while True:
    schedule.run_pending()
    time.sleep(30)  # Vérifie toutes les 30 secondes
