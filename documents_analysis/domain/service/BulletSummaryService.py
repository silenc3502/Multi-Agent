from multi_agent_document.loader.model_loader import summarize_pipeline


class BulletSummaryService:
    async def summarize(self, text: str) -> str:
        prompt = f"Summarize the following text into 5 concise bullet points:\n\n{text}"

        # 실제 LLM 호출
        result = summarize_pipeline(prompt, max_length=250, min_length=50, do_sample=False)

        # 결과에서 summary_text 추출
        return result[0].get("summary_text", "")
