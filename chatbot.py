import speech_recognition as sr
import pyttsx3
from datetime import datetime

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Log file
log_file = "conversation_log.txt"


import os

def speak(text):
    print("Bot:", text)
    os.system(f'powershell -c "Add-Type –AssemblyName System.Speech; '
              f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')


def log_conversation(speaker, message):
    with open(log_file, "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {speaker}: {message}\n")


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)

            print("You said:", text)
            return text

        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."

        except Exception as e:
            return f"Error: {e}"


def get_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hello! Nice to meet you."

    elif "how are you" in user_input:
        return "I am doing great."

    elif "time" in user_input:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"

    elif "date" in user_input:
        return f"Today's date is {datetime.now().strftime('%d %B %Y')}"

    elif "bye" in user_input:
        return "Goodbye! Have a nice day."

    else:
        return "You said: " + user_input


print("===================================")
print("VOICE AND TEXT CHATBOT")
print("Type 'exit' to quit")
print("===================================")

speak("Hello, I am your chatbot.")

while True:

    mode = input("\nChoose Input Mode (text/voice): ").lower()

    if mode == "text":
        user_message = input("You: ")

    elif mode == "voice":
        user_message = listen()

    else:
        print("Invalid choice.")
        continue

    log_conversation("User", user_message)

    if user_message.lower() in ["exit", "bye"]:
        response = "Goodbye!"
        speak(response)
        log_conversation("Bot", response)
        break

    response = get_response(user_message)

    log_conversation("Bot", response)

    speak(response)

print("Conversation saved in conversation_log.txt")