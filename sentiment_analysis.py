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

MAX_LEN = 512

def chunk_text(text: str, tokenizer, max_len: int = MAX_LEN):
    enc = tokenizer(
        text,
        add_special_tokens=False,
        return_attention_mask=False,
        return_token_type_ids=False,
    )
    input_ids = enc["input_ids"]

    chunks = []
    step = max_len - 2

    for i in range(0, len(input_ids), step):
        chunk_ids = input_ids[i : i + step]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)

    return chunks

def get_sentiment(text):
    chunks = chunk_text(text, tokenizer, MAX_LEN)

    # Run on each chunk
    results = analyzer(chunks, truncation=True, max_length=MAX_LEN)

    scores = [label_match[r["label"]] for r in results]

    # Average
    return sum(scores) / len(scores)
