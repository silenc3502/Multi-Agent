import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# MODEL_NAME = "google/flan-t5-base"
MODEL_NAME = "facebook/bart-large-cnn"

def download_model_if_needed():
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    print(f"모델 다운로드 확인: {MODEL_NAME}")
    AutoTokenizer.from_pretrained(MODEL_NAME)
    AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    print("모델 준비 완료.")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

llm_pipeline = pipeline(
    "summarization",
    model=model,
    tokenizer=tokenizer,
    framework="pt"
)
