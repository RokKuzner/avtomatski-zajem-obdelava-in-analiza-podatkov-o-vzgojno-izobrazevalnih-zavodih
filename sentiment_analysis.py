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

def chunk_text_with_weights(text: str, tokenizer, max_len: int = MAX_LEN):
    enc = tokenizer(
        text,
        add_special_tokens=False,
        return_attention_mask=False,
        return_token_type_ids=False,
    )
    ids = enc["input_ids"]

    if not ids:
        return [], []

    step = max_len - 2

    chunks = []
    weights = []

    for i in range(0, len(ids), step):
        chunk_ids = ids[i : i + step]
        if not chunk_ids:
            continue
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)
        chunks.append(chunk_text)
        weights.append(len(chunk_ids))

    return chunks, weights


def get_sentiment(text: str) -> float:
    """
    Returns a 0–100 sentiment score.
    """
    chunks, weights = chunk_text_with_weights(text, tokenizer, MAX_LEN)

    if not chunks:
        return 50.0  # neutral fallback for empty/invalid text

    results = analyzer(chunks, truncation=True, max_length=MAX_LEN)

    # Weighted average
    weighted_sum = 0.0
    total_weight = 0

    for res, w in zip(results, weights):
        score = label_match[res["label"]]
        weighted_sum += score * w
        total_weight += w

    return weighted_sum / total_weight if total_weight > 0 else 50.0