import json
from datetime import datetime
from pathlib import Path


class ConversationMemory:
    """
    Stores and manages conversation history.

    Responsibilities:
    - Load conversation
    - Save conversation
    - Add user messages
    - Add assistant messages
    - Return recent conversation
    - Clear conversation
    """

    def __init__(
        self,
        memory_path: str = "backend/app/memory/conversation.json",
    ):

        self.memory_path = Path(memory_path)

        # Ensure directory exists
        self.memory_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Create file if it doesn't exist
        if not self.memory_path.exists():

            self.memory_path.write_text(
                "[]",
                encoding="utf-8",
            )

        self.messages = self.load()

    def load(self) -> list:

        try:

            with self.memory_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except (json.JSONDecodeError, OSError):

            print(
                "⚠️ Conversation history is corrupted. "
                "Starting with an empty conversation."
            )

            self.memory_path.write_text(
                "[]",
                encoding="utf-8",
            )

            return []

    def save(self) -> None:

        temp_path = self.memory_path.with_suffix(".tmp")

        with temp_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.messages,
                file,
                indent=4,
                ensure_ascii=False,
            )

        # Atomic replace
        temp_path.replace(self.memory_path)

    def add_user_message(
        self,
        message: str,
    ) -> None:

        self.messages.append(
            {
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        self.save()

    def add_assistant_message(
        self,
        message: str,
    ) -> None:

        self.messages.append(
            {
                "role": "assistant",
                "content": message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        self.save()

    def get_recent_history(
        self,
        max_messages: int = 10,
    ) -> str:

        history = self.messages[-max_messages:]

        return "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        )

    def clear(self) -> None:

        self.messages = []

        self.save()