from fastapi import APIRouter, Depends

# 요청/응답 DTO
from ask.adapter.input.web.request.add_docs_request import AddDocsRequest
from ask.adapter.input.web.request.ask_rag_request import AskRAGRequest
from ask.adapter.input.web.request.ask_request import AskRequest
from ask.adapter.input.web.response.ask_response import AskResponse

# Repository 구현체
from ask.adapter.output.repository.answer_repository_impl import AnswerRepositoryImpl
from ask.adapter.output.repository.question_repository_impl import QuestionRepositoryImpl

# UseCase
from ask.application.usecase.add_document_usecase import AddDocumentsUseCase
from ask.application.usecase.ask_question_usecase import AskQuestionUseCase
from ask.application.usecase.ask_rag_question_usecase import AskRAGQuestionUseCase

# Agent
from ask.infrastructure.client.langgraph_agent import LangGraphAgent
from ask.infrastructure.client.rag_agent import RAGAgent

# 세션 헬퍼: 현재 로그인한 사용자 ID 가져오기
from utility.session_helper import get_current_user

# FastAPI 라우터 초기화
ask_router = APIRouter()


# -----------------------------------------------
# 일반 질문 처리 (LLM 단독 사용)
# -----------------------------------------------
@ask_router.post("/question", response_model=AskResponse)
def ask(
    request: AskRequest,  # 요청 바디에서 질문 내용 수신
    user_id: int = Depends(get_current_user),  # 로그인한 사용자 ID 가져오기
):
    # UseCase 초기화: 질문/답변 저장소 + LangGraphAgent
    usecase = AskQuestionUseCase(
        question_port=QuestionRepositoryImpl(),
        answer_port=AnswerRepositoryImpl(),
        agent=LangGraphAgent(user_id=user_id),
    )

    # 질문 처리
    answer = usecase.execute(
        question_text=request.question,
        asker_id=user_id,
    )

    # 응답 반환
    return AskResponse(answer=answer.content)


# -----------------------------------------------
# RAG Agent 및 AddDocumentsUseCase 초기화
# -----------------------------------------------
# RAG용 에이전트 (Chroma DB 연결)
rag_agent = RAGAgent(chroma_persist_dir="chroma_db")
# 문서 추가용 UseCase
add_docs_usecase = AddDocumentsUseCase(agent=rag_agent)


# -----------------------------------------------
# RAG용 문서 추가 엔드포인트
# -----------------------------------------------
@ask_router.post("/add-docs")
def add_docs(req: AddDocsRequest):
    """
    POST /user-ask/add-docs
    - 요청 예시:
      {
          "documents": ["문서1 내용", "문서2 내용"]
      }
    - Chroma DB에 문서 추가
    """
    # documents를 RAG 에이전트에 추가
    rag_agent.add_documents(req.documents)
    return {"status": "ok", "added": len(req.documents)}


# -----------------------------------------------
# RAG 기반 질문 처리 (검색 후 LLM 답변)
# -----------------------------------------------
@ask_router.post("/rag-question", response_model=AskResponse)
def ask_rag(
    request: AskRequest,  # 질문 내용
    user_id: int = Depends(get_current_user),  # 현재 사용자
):
    """
    POST /user-ask/rag-question
    - RAG 기반 답변 생성
    - Chroma DB에서 관련 문서 검색 후 LLM으로 답변
    """
    # RAG용 UseCase 초기화
    usecase = AskRAGQuestionUseCase(
        question_port=QuestionRepositoryImpl(),
        answer_port=AnswerRepositoryImpl(),
        agent=rag_agent
    )

    # 질문 처리
    answer = usecase.execute(
        question_text=request.question,
        asker_id=user_id
    )

    # 답변 반환
    return AskResponse(answer=answer.content)
