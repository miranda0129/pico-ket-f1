# -------------------------
# Display functions
# -------------------------
def strip_accents(text):
    replacements = {
        "á": "a",
        "à": "a",
        "ä": "a",
        "â": "a",
        "ã": "a",
        "å": "a",

        "é": "e",
        "è": "e",
        "ë": "e",
        "ê": "e",

        "í": "i",
        "ì": "i",
        "ï": "i",
        "î": "i",

        "ó": "o",
        "ò": "o",
        "ö": "o",
        "ô": "o",
        "õ": "o",

        "ú": "u",
        "ù": "u",
        "ü": "u",
        "û": "u",

        "ñ": "n",
        "ç": "c",

        "Á": "A",
        "À": "A",
        "Ä": "A",
        "É": "E",
        "È": "E",
        "Ö": "O",
        "Ü": "U",
        "Ñ": "N",
        "Ç": "C",
    }

    for accented, plain in replacements.items():
        text = text.replace(accented, plain)

    return text