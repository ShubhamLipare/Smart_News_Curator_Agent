from transformers import pipeline

classifier=pipeline("zero-shot-classification")

categories=["Technology", "Finance", "Politics", "Health", "Sports"]

def classify_topic(text:str):
    return classifier(text,categories)