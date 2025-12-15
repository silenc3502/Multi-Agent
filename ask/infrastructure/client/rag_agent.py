import os
from typing import List

from langchain_classic.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

import chromadb
from chromadb import PersistentClient
from chromadb.utils import embedding_functions


class RAGAgent:
    def __init__(self, chroma_persist_dir: str = "chroma_db"):
        self.persist_dir = chroma_persist_dir

        # OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

        # LLM
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # 최신 Chroma 로컬 영구 client
        self.client = PersistentClient(path=self.persist_dir)

        # 컬렉션 초기화/획득
        if "rag_collection" in [c.name for c in self.client.list_collections()]:
            self.collection = self.client.get_collection("rag_collection")
        else:
            openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )
            self.collection = self.client.create_collection(
                name="rag_collection",
                embedding_function=openai_ef
            )

        # Prompt 템플릿
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
다음 문서를 참고하여 질문에 답변하세요.
문서 내용:
{context}

질문:
{question}

친절하고 이해하기 쉽게 한국어로 답변해 주세요.
"""
        )

    def query_documents(self, question: str, n_results: int = 3) -> List[str]:
        results = self.collection.query(query_texts=[question], n_results=n_results)
        return results["documents"][0] if results["documents"] else []

    def generate_answer(self, question: str, context_texts: List[str]) -> str:
        context = "\n".join(context_texts) if context_texts else "관련 문서를 찾을 수 없습니다."
        chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        return chain.run(context=context, question=question).strip()

    def add_documents(self, texts: List[str]):
        if not texts:
            return

        ids = [str(i) for i in range(len(texts))]
        self.collection.add(documents=texts, ids=ids)
