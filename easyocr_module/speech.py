import pyttsx3
 
def speak_text(text, lang="en"):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties like rate and volume
    engine.setProperty('rate', 130)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    # Speak the text
    engine.say(text)
    engine.runAndWait()  # This is blocking, will wait until the speech is done
