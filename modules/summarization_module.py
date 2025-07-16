from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    """
    Summarizes a single block of text.
    Args:
        text (str): Text to summarize.
    Returns:
        str: Summarized text.
    """
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Error in summarization"

def summarize_texts(text_dict):
    """
    Summarizes a batch of texts.
    Args:
        text_dict (dict): Dictionary with filenames as keys and texts as values.
    Returns:
        dict: Dictionary with filenames as keys and summaries as values.
    """
    summarized_texts = {}
    for image_name, text in text_dict.items():
        print(f"Summarizing text from {image_name}...")
        summarized_texts[image_name] = summarize_text(text)
    return summarized_texts

if __name__ == "__main__":
    # Test the summarization module
    sample_text = "This is a long article about an ongoing war. Hostilities escalated with both sides reporting heavy casualties. Talks have failed to resolve the conflict."
    summary = summarize_text(sample_text)
    print("--- Single Text Summary ---")
    print(summary)

    batch_texts = {
        "image1.jpg": "This is a news article discussing economic impacts of war.",
        "image2.jpg": "Another article focusing on peace talks and negotiations.",
    }
    batch_summaries = summarize_texts(batch_texts)
    print("--- Batch Summaries ---")
    for filename, summary in batch_summaries.items():
        print(f"{filename}: {summary}")
