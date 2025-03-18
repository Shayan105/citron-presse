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

# Generate the output file name with the current date
current_date = datetime.now().strftime("%d-%m-%Y")
OUTPUT_FILE_NAME = f"{current_date}.wav"  # file name.
MP3_FILE_NAME = f"{current_date}.mp3"  # MP3 file name.
SAMPLE_RATE = 48000  # [Hz]. sampling rate.

DURATION = 35
DELTA = 5

def record_audio():
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        # record audio with loopback from default speaker.
        data = mic.record(numframes=SAMPLE_RATE * DURATION)
        
        # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
        sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

    # Convert WAV to MP3 using ffmpeg
    subprocess.run(['ffmpeg', '-i', OUTPUT_FILE_NAME, MP3_FILE_NAME])

    # Delete the WAV file
    os.remove(OUTPUT_FILE_NAME)

def run_script():
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Start recording audio in a separate thread
    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()

    driver.get("https://www.rfj.ch/rfj/Accueil/RFJ-votre-radio-regionale.html")
    sleep(DELTA)
    driver.find_element(By.CSS_SELECTOR, ".manual-link > .fa-volume-up").click()
    sleep(DURATION)

    driver.close()

    # Wait for the audio recording to finish
    audio_thread.join()

# Schedule the script to run every day at 17:34 and 17:37 except on Saturdays and Sundays
def job():
    if datetime.now().weekday() < 5:  # Monday to Friday are 0-4
        run_script()

schedule.every().day.at("17:34").do(job)
schedule.every().day.at("17:59").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


