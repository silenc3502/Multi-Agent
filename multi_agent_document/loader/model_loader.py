from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline
)

# Summarization 모델
SUMMARIZE_MODEL = "facebook/bart-large-cnn"
summarize_tokenizer = AutoTokenizer.from_pretrained(SUMMARIZE_MODEL)
summarize_model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZE_MODEL)
summarize_pipeline = pipeline(
    "summarization",
    model=summarize_model,
    tokenizer=summarize_tokenizer,
    framework="pt"
)

# QA/Instruction 모델
QA_MODEL = "google/flan-t5-base"
qa_tokenizer = AutoTokenizer.from_pretrained(QA_MODEL)
qa_model = AutoModelForSeq2SeqLM.from_pretrained(QA_MODEL)
qa_pipeline = pipeline(
    "text2text-generation",
    model=qa_model,
    tokenizer=qa_tokenizer,
    framework="pt"
)
