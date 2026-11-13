import speech_recognition as sr
import pyttsx3
from googletrans import Translator #google translate api
import asyncio

# initilalize text-to-speech engine
def speak(text, language='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    voices = engine.getProperty('voices')
    if language == 'en':
        engine.setProperty('voice', voices[0].id) #default english voice
    else:
        engine.setProperty('voice', voices[1].id) #fallback to anoter voice if avaliable

    engine.say(text)
    engine.runAndWait()

# speech to text, recognize spoken language (english)
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Please speak now in English...")
        audio = recognizer.listen(source)

    try:
        print("🎤 Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"✅ you said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ API Error: {e}")
    return ""

# translate text using google translate api
async def translate_text(text, target_language="es"): #default target language is spanish
    async with Translator() as translator:
        translation = await translator.translate(text, dest=target_language)
        return translation.text

# display language options for translation
def display_language_options():
    print("Available translation languages: ")
    print("1. Spanish (es)")
    print("2. French (fr)")
    print("3. German (de)")
    print("4. Italian (it)")
    print("5. Portuguese (pt)")
    print("6. Russian (ru)")
    print("7. Chinese (zh-CN)")
    print("8. Japanese (ja)")
    print("9. Korean (ko)")
    print("10. Arabic (ar)")
    print("11. Hindi (hi)")

    # user selects a language
    choice = input("Please select the target language number (1-11): ")
    language_dict = {
        "1": "es",
        "2": "fr",
        "3": "de",
        "4": "it",
        "5": "pt",
        "6": "ru",
        "7": "zh-CN",
        "8": "ja",
        "9": "ko",
        "10": "ar",
        "11": "hi"
    }

    return language_dict.get(choice, "es") #default to spanish if invalid input

# main function to combine all steps
async def main():
    # step 1: displau language and get users choice
    target_language = display_language_options()
    # step 2: speech_to_text (recognizing english speech)
    original_text = speech_to_text()

    if original_text:
        # step3: translate to selected target language
        translated_text = await translate_text(original_text, target_language=target_language)

        if translated_text:
            # step4: text-to-speech (translate output and speak it)
            speak(translated_text, language=target_language)
            print("✅translation spoken out!")   



if __name__ == "__main__":
    asyncio.run(main())