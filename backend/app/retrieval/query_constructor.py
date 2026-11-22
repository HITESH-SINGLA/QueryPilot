import os

from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from backend.app.memory.conversation_memory import ConversationMemory
from backend.app.models.query_bundle import QueryBundle

load_dotenv()


class QueryConstructor:
    """
    Constructs a standalone query by resolving references
    from the previous conversation.

    Examples
    --------
    User : Who is the President of India?
    User : What is her age?

    Standalone Query:
    What is the age of the President of India, Droupadi Murmu?
    """

    def __init__(
        self,
        conversation_memory: ConversationMemory,
    ):

        self.conversation_memory = conversation_memory

        self.llm = ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3.2:latest",
            ),
            temperature=0,
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
        You are a reference resolution engine.

        Your ONLY job is to resolve references in the latest user question.

        IMPORTANT

        Most questions DO NOT require any modification.

        If the latest user question is already self-contained,
        return it EXACTLY as written.

        Do NOT:

        - paraphrase
        - rewrite
        - summarize
        - simplify
        - change wording
        - change numbers
        - change names
        - change entities
        - change the user's intent
        - infer missing information

        The ONLY time you may modify the question is when it contains
        references that cannot be understood without the conversation.

        Examples of references:

        - he
        - she
        - him
        - her
        - they
        - them
        - it
        - this
        - that
        - these
        - those
        - previous one
        - continue
        - above
        - earlier
        - former
        - latter

        Examples

        Conversation

        User: Who is Bhuvan Bam?

        Current Question

        What is his age?

        Output

        What is the age of Bhuvan Bam?

        --------------------------------------------

        Conversation

        User: Plot these ages on a graph.

        Current Question

        Plot 10,20,30,40 on a graph

        Output

        Plot 10,20,30,40 on a graph

        --------------------------------------------

        Conversation

        User: Explain TCP.

        Current Question

        Explain UDP.

        Output

        Explain UDP.

        --------------------------------------------

        Conversation History

        {history}

        --------------------------------------------

        Current Question

        {question}

        --------------------------------------------

        Return ONLY the final question.
        """
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def construct(
        self,
        question: str,
    ) -> QueryBundle:

        history = self.conversation_memory.get_recent_history()

        standalone_query = self.chain.invoke(
            {
                "history": history,
                "question": question,
            }
        ).strip()
        print("=" * 80)
        print("Original Question:")
        print(question)

        print("\nConversation History:")
        print(history)

        print("\nStandalone Query:")
        print(standalone_query)
        print("=" * 80)

        print("\n================ QUERY CONSTRUCTOR ================")
        print(f"Original Query   : {question}")
        print(f"Standalone Query : {standalone_query}")
        print("===================================================\n")

        return QueryBundle(
            original_query=question,
            standalone_query=standalone_query,
        )