from fastapi import APIRouter, Depends

from ask.adapter.input.web.request.add_docs_request import AddDocsRequest
from ask.adapter.input.web.request.ask_rag_request import AskRAGRequest
from ask.adapter.input.web.request.ask_request import AskRequest
from ask.adapter.input.web.response.ask_response import AskResponse
from ask.adapter.output.repository.answer_repository_impl import AnswerRepositoryImpl
from ask.adapter.output.repository.question_repository_impl import QuestionRepositoryImpl
from ask.application.usecase.add_document_usecase import AddDocumentsUseCase
from ask.application.usecase.ask_question_usecase import AskQuestionUseCase
from ask.application.usecase.ask_rag_question_usecase import AskRAGQuestionUseCase
from ask.infrastructure.client.langgraph_agent import LangGraphAgent
from ask.infrastructure.client.rag_agent import RAGAgent
from utility.session_helper import get_current_user

ask_router = APIRouter()

@ask_router.post("/question", response_model=AskResponse)
def ask(
    request: AskRequest,
    user_id: int = Depends(get_current_user),
):
    usecase = AskQuestionUseCase(
        question_port=QuestionRepositoryImpl(),
        answer_port=AnswerRepositoryImpl(),
        agent=LangGraphAgent(user_id=user_id),
    )

    answer = usecase.execute(
        question_text=request.question,
        asker_id=user_id,
    )

    return AskResponse(answer=answer.content)

rag_agent = RAGAgent(chroma_persist_dir="chroma_db")
add_docs_usecase = AddDocumentsUseCase(agent=rag_agent)

@ask_router.post("/add-docs")
def add_docs(req: AddDocsRequest):
    rag_agent.add_documents(req.documents)
    return {"status": "ok", "added": len(req.documents)}

@ask_router.post("/rag-question", response_model=AskResponse)
def ask_rag(
    request: AskRequest,
    user_id: int = Depends(get_current_user)
):
    usecase = AskRAGQuestionUseCase(
        question_port=QuestionRepositoryImpl(),
        answer_port=AnswerRepositoryImpl(),
        agent=rag_agent
    )

    answer = usecase.execute(
        question_text=request.question,
        asker_id=user_id
    )

    return AskResponse(answer=answer.content)
