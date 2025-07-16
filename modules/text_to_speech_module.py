import pyttsx3

def text_to_speech(text, output_filename=None):
    """
    Converts text to speech and optionally saves it to an audio file.
    Args:
        text (str): The text to convert to speech.
        output_filename (str): Optional path to save the audio file (e.g., "audio_reports/report.mp3").
    """
    try:
        # Initialize pyttsx3
        engine = pyttsx3.init()
        # Adjust the speech rate (slower or faster speech)
        engine.setProperty('rate', 150)
        # Adjust the voice (choose one of the system voices)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Use the first voice in the system

        if output_filename:
            # Save speech to an audio file
            engine.save_to_file(text, output_filename)
            engine.runAndWait()
            print(f"Audio saved to {output_filename}")
        else:
            # Play the speech directly
            engine.say(text)
            engine.runAndWait()

    except Exception as e:
        print(f"Error in text_to_speech: {e}")

from modules.text_to_speech_module import text_to_speech

# Test string
sample_text = "This is a sample text being converted to speech. Delta Headlines AI is amazing!"
output_path = "test_audio.mp3"

# Convert text to audio and save it
text_to_speech(sample_text, output_filename=output_path)
