# text_cleaning.py

# Egyptian Dialect Normalization Rules
EGYPTIAN_NORMALIZATION_MAP = {
    "عاوز": "أريد",
    "عايز": "أريد",
    "اعمل": "أنشئ",
    "عملت": "أنشأت",
    "حاجة": "",
    "وكده": "",
    "يعني": "",
    "بردو": "أيضاً",
    "أوي": "جداً",
    "دلوقتي": "الآن",
    "عشان": "بسبب",
    "ليه": "لماذا",
    "مش": "ليس",
    "كانت": "كانت",
    "فيها": "بها",
    "إيه": "ماذا",
    "إمتى": "متى",
    "إزاي": "كيف",
    "فين": "أين",
    "مين": "من",
    "يا ريت": "ليت",
    "كويس": "جيد",
    "وحش": "سيء",
    "بتاع": "خاص",
    "بتوع": "خاص بـ",
}

def normalize_egyptian_dialect(text):
    """ Normalize Egyptian dialect in the provided text. """
    words = text.split()
    normalized_words = [EGYPTIAN_NORMALIZATION_MAP.get(word, word) for word in words]
    return " ".join([w for w in normalized_words if w])

def preprocess_text(text):
    """ Preprocess the input text. """
    if not text:
        return ""
    
    # Basic cleaning
    text = text.strip()
    text = text.lower()
    
    # Dialect normalization
    text = normalize_egyptian_dialect(text)
    
    return text

# Example Usage
if __name__ == '__main__':
    sample_text = "اعمل برزنتيشن عن الذكاء الاصطناعي في الطب وكده عشان دلوقتي الموضوع ده مهم أوي"
    cleaned_text = preprocess_text(sample_text)
    print(f"Original: {sample_text}")
    print(f"Cleaned: {cleaned_text}")