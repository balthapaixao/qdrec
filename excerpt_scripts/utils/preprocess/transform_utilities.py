import clean_text_utilities


def preprocess_text(text: str) -> str:
    """Preprocess text.
    Args:
        text: a string
    Returns:
        a string
    """

    text = clean_text_utilities.remove_special_characters(text)
    text = clean_text_utilities.remove_dash_n(text)
    text = clean_text_utilities.remove_lots_of_points(text)
    text = clean_text_utilities.remove_bad_chars(text)
    text = clean_text_utilities.spaced_letters(text)
    text = clean_text_utilities.dots_that_mess_segmentation(text)
    text = clean_text_utilities.remove_spaces(text)
    text = clean_text_utilities.join_words(text)
    text = clean_text_utilities.separate_words(text)
    text = clean_text_utilities.remove_page_breaker(text)
    text = clean_text_utilities.remove_special_characters(text)

    text = clean_text_utilities.clean_text(text)

    return text
