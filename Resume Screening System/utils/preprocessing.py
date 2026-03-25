import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


#  CLEAN TEXT
def clean_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    return text.strip()


# TOKENIZE + LEMMATIZE 
def preprocess_text(text):
    doc = nlp(text)

    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return " ".join(tokens)


# FULL PREPROCESS PIPELINE
def process_text(text):
    cleaned = clean_text(text)
    processed = preprocess_text(cleaned)
    return processed