import sounddevice as sd
import wavio
import numpy as np
import speech_recognition as sr
from spellchecker import SpellChecker


recording_data = []
is_recording = False

def callback(indata, frames, time, status):
    if status:
        print(status)
    global recording_data
    recording_data.append(indata.copy())

def start_recording():
    global recording_data, is_recording, stream
    recording_data = []
    is_recording = True
    stream = sd.InputStream(callback=callback, channels=1, samplerate=44100)
    stream.start()
    print("Recording started...")

def stop_recording(filename="recording.wav"):
    global is_recording, stream
    if is_recording:
        stream.stop()
        stream.close()
        is_recording = False
        print("Recording stopped.")
        audio_np = np.concatenate(recording_data, axis=0)
        wavio.write(filename, audio_np, 44100, sampwidth=2)
        return filename
    else:
        print("Not recording.")
        return None

def transcribe_audio(filename="recording.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="en")
            return text
        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError as e:
            return f"Error from speech recognition service: {e}"

# def spell_check(text):
#     spell = SpellChecker()
#     corrected = []
#     for word in text.split():
#         corrected.append(spell.correction(word) or word)
#     return ' '.join(corrected)

def full_process(filename="recording.wav"):
    transcribed = transcribe_audio(filename)
    # corrected = spell_check(transcribed)
    return  transcribed
