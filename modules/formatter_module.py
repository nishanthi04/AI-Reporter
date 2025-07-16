def format_as_news_report(summary):
    """
    Formats the summarized text into a military-style wartime report.
    Args:
        summary (str): Summarized text.
    Returns:
        str: Formatted news report.
    """
    prompt = (
        f"⚔️ Wartime Report: \n\n'{summary}'\n\n"
        "🪖 Tactical Analysis Complete. Over and Out. 🫡"
    )
    return prompt

if __name__ == "__main__":
    # Test the formatter module
    sample_summary = "Hostilities escalated in the eastern region, with both sides reporting casualties."
    formatted_report = format_as_news_report(sample_summary)
    print(formatted_report)
