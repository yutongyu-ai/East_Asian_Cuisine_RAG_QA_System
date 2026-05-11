import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
#from langchain_openai import ChatOpenAI

# from reranker import rerank
from .retriever import RetrieveService
from ..llm.qwen import QwenLLM
from .history_store import MemoryService


def print_prompt(prompt):
    print("=" * 70)
    print(prompt.to_string())
    print("=" * 70)

    return prompt


class RagService():
    def __init__(self, session_id: str):
        self.retrieve_service = RetrieveService()
        self.memory = MemoryService(session_id=session_id)
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant specialized in East Asian cuisine."
                 "please answer shortly, reference:{context}"),
                MessagesPlaceholder(variable_name="history"),
                ("user", "please answer the user's question: {input}"),

            ]
        )
        self.chat_model = QwenLLM()
        # self.chat_model = ChatOpenAI(
        #     model="gpt-4o-mini",
        #     temperature=0
        # )

        self.chain = self.__get_chain()

    def format_document(self, docs: list[Document]):
        if not docs:
            return "No relevant information"
        formatted_str = ""
        for doc in docs:
            formatted_str += f":{doc.page_content}\n{doc.metadata}"
        return formatted_str


    def __get_chain(self):
        retriever = self.retrieve_service.get_retriever()

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": retriever | self.format_document,
                "history": lambda _: self.memory.history.messages
            } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        return chain

if __name__ == "__main__":
    rag = RagService(session_id='user_001')
    question = "what is last question?"
    answer = rag.chain.invoke(question)
    rag.memory.history.add_user_message(question)
    rag.memory.history.add_ai_message(answer)

    print(answer)
