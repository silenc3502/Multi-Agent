import os
from typing import List

# LangChain LLM과 Prompt 템플릿
from langchain_classic.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# ChromaDB 관련
import chromadb
from chromadb import PersistentClient
from chromadb.utils import embedding_functions


class RAGAgent:
    """
    RAG (Retrieval-Augmented Generation) 에이전트 클래스.
    - 문서를 추가하고(query) 검색 후(answer) LLM으로 답변 생성.
    - 로컬 Persistent Chroma DB를 사용하여 문서 저장 및 검색.
    """

    def __init__(self, chroma_persist_dir: str = "chroma_db"):
        self.persist_dir = chroma_persist_dir

        # OpenAI Embeddings 초기화: 문서 벡터화에 사용
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

        # LLM 초기화: GPT 모델을 사용하여 자연어 답변 생성
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,  # deterministic 답변
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # 최신 Chroma 로컬 영구 client 초기화
        # PersistentClient는 로컬 경로에 DB를 유지하며, 재시작 후에도 데이터 유지
        self.client = PersistentClient(path=self.persist_dir)

        # 컬렉션 초기화/획득
        # "rag_collection"이 존재하면 가져오고, 없으면 생성
        if "rag_collection" in [c.name for c in self.client.list_collections()]:
            self.collection = self.client.get_collection("rag_collection")
        else:
            # OpenAI Embedding 함수를 컬렉션에 연결
            openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )
            self.collection = self.client.create_collection(
                name="rag_collection",
                embedding_function=openai_ef
            )

        # LLM 입력용 Prompt 템플릿
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
        """
        RAG 검색: 입력 질문과 관련된 문서 반환
        - question: 사용자 질문
        - n_results: 반환할 문서 수
        """
        results = self.collection.query(query_texts=[question], n_results=n_results)
        # documents 결과가 없으면 빈 리스트 반환
        return results["documents"][0] if results["documents"] else []

    def generate_answer(self, question: str, context_texts: List[str]) -> str:
        """
        검색된 문서를 기반으로 LLM 답변 생성
        - context_texts: query_documents에서 반환된 문서 리스트
        """
        # context가 없으면 안내 문구 사용
        context = "\n".join(context_texts) if context_texts else "관련 문서를 찾을 수 없습니다."
        chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        return chain.run(context=context, question=question).strip()

    def add_documents(self, texts: List[str]):
        """
        문서 추가: Chroma 컬렉션에 새로운 문서 등록
        - texts: 추가할 문서 문자열 리스트
        """
        if not texts:
            return  # 빈 리스트면 아무 동작도 하지 않음

        # 문서 ID를 간단히 인덱스로 생성
        ids = [str(i) for i in range(len(texts))]
        # 컬렉션에 문서 추가
        self.collection.add(documents=texts, ids=ids)
