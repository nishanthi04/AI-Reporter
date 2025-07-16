import pyttsx3

def test_text_to_speech():
    try:
        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()

        # Set properties (optional)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

        # Get available voices and set one
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Use the first voice

        # Text to speak
        text = "This is a test of the text-to-speech module using pyttsx3."

        # Say and save the text
        print("Converting text to speech...")
        engine.say(text)
        engine.runAndWait()  # Wait for the speaking to finish

        print("Test successful!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test function
test_text_to_speech()
