from backend.app.retrieval.llm_router import LLMRouter


router = LLMRouter()

questions = [
    # -------------------------------
    # Direct Retrieval
    # -------------------------------
    "What is TCP?",
    "Explain Gradient Descent.",
    "Define Operating System.",

    # -------------------------------
    # Recursive Retrieval
    # -------------------------------
    "Compare TCP and UDP.",
    "What are the advantages of REST over SOAP?",
    "Who is the manager of the team that held the meeting on Friday?",
    "Which customer bought the highest-selling product?",
    "Explain the complete compiler pipeline.",

    # -------------------------------
    # Web Search
    # -------------------------------
    "Latest AI news.",
    "Current CEO of Google.",
    "Weather today in Delhi.",
    "Who won yesterday's IPL match?",

    # -------------------------------
    # Python
    # -------------------------------
    "Calculate the average salary.",
    "Plot a histogram of marks.",
    "Find the median age.",
    "Analyze the uploaded CSV.",
]

for i, question in enumerate(questions, start=1):

    print("\n" + "=" * 80)
    print(f"Test Case {i}")
    print("=" * 80)

    print(f"Question : {question}")

    decision = router.route(question)

    print(f"Strategy   : {decision.strategy}")
    print(f"Reason     : {decision.reason}")
    print(f"Confidence : {decision.confidence}")