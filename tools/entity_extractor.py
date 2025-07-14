from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)

def extract_entities(text: str):
    return ner(text)
