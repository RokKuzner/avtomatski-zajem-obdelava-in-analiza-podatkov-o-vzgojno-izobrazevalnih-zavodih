from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "cjvt/sloberta-sentinews-sentence" #"tabularisai/multilingual-sentiment-analysis" #"EMBEDDIA/sloberta"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create a sentiment analysis pipeline
analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=-1)

label_match = {
    "neutral": 50,
    "negative": 0,
    "positive": 100
}

def get_sentiment(text):
    result = analyzer(text)

    return label_match[ result[0]["label"] ]
