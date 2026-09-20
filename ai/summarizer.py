from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

_tokenizer = None
_model = None


def get_summarizer():
    """
    Load the summarization model only when it is actually needed.
    """
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(
            "google/flan-t5-small"
        )

        _model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-small"
        )

    return _tokenizer, _model


def generate_summary(messages):
    if not messages:
        return "No conversation to summarize."

    conversation = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in messages
    )

    conversation = conversation[:2000]

    prompt = (
        "Summarize only the facts in this conversation. "
        "Do not add new information.\n\n"
        f"{conversation}\n\n"
        "Summary:"
    )

    tokenizer, model = get_summarizer()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        do_sample=False
    )

    return tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )