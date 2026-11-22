import json
import os
import re

from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from backend.app.models.query_bundle import QueryBundle
from backend.app.strategies import (
    DIRECT_RAG,
    PYTHON,
)

load_dotenv()


class QueryRouter:
    """
    LLM-based router that determines the execution strategy
    for a SINGLE standalone question.

    Responsibilities:
    - Decide whether semantic retrieval is sufficient.
    - Decide whether Python execution is required.

    It DOES NOT decide between Local Retrieval and Web Search.
    That decision is handled later using vector similarity.
    """

    def __init__(self):

        self.llm = ChatOllama(
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3.2:latest",
            ),
            temperature=0,
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are the routing engine of an Adaptive RAG system.

The input will ALWAYS be a SINGLE standalone question.

Your task is ONLY to decide whether answering the question requires:

1. DIRECT_RAG
2. PYTHON

DO NOT answer the question.
DO NOT explain the question.
Return ONLY valid JSON.

--------------------------------------------------

DIRECT_RAG

Use when semantic retrieval is sufficient.

Examples:

- What is TCP?
- Explain Gradient Descent.
- Define Deadlock.
- What is an Operating System?
- Who is the Prime Minister of India?
- What is the age of the Prime Minister of India?
- Compare TCP and UDP.
- Explain the difference between AWS and Azure.

--------------------------------------------------

PYTHON

Use when solving the question requires computation,
mathematical calculations, statistics,
data analysis, plotting, or executing Python code.

Examples:

- Calculate average marks.
- Plot a graph.
- Analyze a CSV.
- Compute the median.
- Find the correlation.
- Generate a histogram.
- Solve this equation.

--------------------------------------------------

Question

{question}

--------------------------------------------------

Return ONLY valid JSON.

{{
    "strategy": "DIRECT_RAG",
    "reason": "",
    "confidence": 0.95
}}
"""
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def route(
        self,
        query_bundle: QueryBundle,
    ) -> QueryBundle:

        response = self.chain.invoke(
            {
                "question": query_bundle.standalone_query,
            }
        )

        print("\n================ ROUTER =================")
        print(response)
        print("=========================================\n")

        try:

            match = re.search(
                r"\{[\s\S]*\}",
                response,
            )

            if match is None:
                raise ValueError(
                    "No JSON object found."
                )

            decision = json.loads(
                match.group()
            )

            strategy = (
                decision.get(
                    "strategy",
                    "",
                )
                .strip()
                .upper()
            )

            if strategy not in {
                DIRECT_RAG,
                PYTHON,
            }:
                print(
                    f"Unknown strategy '{strategy}'. "
                    "Falling back to DIRECT_RAG."
                )

                strategy = DIRECT_RAG

            query_bundle.strategy = strategy

            query_bundle.reason = decision.get(
                "reason",
                "Router fallback",
            )

            query_bundle.confidence = float(
                decision.get(
                    "confidence",
                    0.0,
                )
            )

        except Exception as e:

            print(f"Router Parsing Error: {e}")

            query_bundle.strategy = DIRECT_RAG
            query_bundle.reason = "Router fallback"
            query_bundle.confidence = 0.0

        print("\n=============== EXECUTION PLAN ===============")
        print(f"Strategy   : {query_bundle.strategy}")
        print(f"Reason     : {query_bundle.reason}")
        print(f"Confidence : {query_bundle.confidence:.2f}")
        print("==============================================\n")

        return query_bundle