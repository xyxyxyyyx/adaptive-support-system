from transformers import pipeline

# load once (important)
summarizer = pipeline("summarization", model="google/flan-t5-small")


def generate_summary(messages):
    if not messages:
        return "No conversation to summarize."

    # combine chat into one text
    text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

    # safety limit (important or it crashes)
    text = text[:2000]

    result = summarizer(text, max_length=120, min_length=30, do_sample=False)

    return result[0]["summary_text"]