import os
from langchain_community.chat_message_histories import PostgresChatMessageHistory


class MemoryService:
    def __init__(self, session_id: str):
        self.session_id = session_id

        self.connection_string = os.getenv(
            "POSTGRES_URL",
            "postgresql://postgres:YOUR_PASSWORD@localhost:5432/rag_db"
        )

        self.history = PostgresChatMessageHistory(
            connection_string=self.connection_string,
            session_id=self.session_id
        )

    def get_history(self):
        return self.history

